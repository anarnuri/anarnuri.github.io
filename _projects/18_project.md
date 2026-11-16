---
layout: page
title: "Gift-packing VLA: GPU suction cup, data iteration, π0.5 vs GR00T"
description: "A 7-DoF suction arm clearing 12-gift trays in sim. A vacuum suction cup as Warp kernels in Newton / Isaac Lab 3, three dataset generations driven by failure analysis, π0.6/π0.7 recipes on top of π0.5, and a GR00T N1.7 comparison on the same data."
img: assets/img/richtech/vla/thumb_policy.jpg
importance: 0
category: Work
featured: true
related_publications: false
---

<div class="row mt-3">
  <div class="col-sm mt-3 mt-md-0">
    {% include video_if_exists.liquid path="assets/video/richtech/vla/pi05_v2mix_tray.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=false muted=true novolume=true %}
  </div>
</div>
<div class="caption">
  Closed-loop rollout of my best π0.5 checkpoint (full fine-tune, third dataset generation) in the simulated packing cell, 8× speed. The policy sees two cameras and the joint state, outputs 32-step joint-target chunks plus a suction command, and clears all 12 gifts in 12 attempts, with no missed picks, in about 6 minutes of sim time. Nothing is scripted. Every motion comes from the policy.
</div>

# Gift-packing VLA

## Overview

At **Richtech** I own a vision–language–action (VLA) pipeline for a packing task. A **Realman RM75-B 7-DoF arm with a suction cup** (on our DEX mobile manipulator) picks gift boxes out of a cardboard tray (up to 12 gifts in two layers) and releases each one into a packing machine. It repeats until the tray is empty. The policy is **π0.5** (openpi), trained entirely on synthetic data that I generate in Isaac Sim / Isaac Lab.

The work splits into four threads. Each one fed the next:

1. **Making suction physical.** The stock simulator "suction" is a glue joint. I replaced it with a compliant tool and a seal model, then with a **vacuum suction cup written as GPU kernels** in Newton, which now runs inside **Isaac Lab 3**.
2. **Recording datasets at scale.** A LeRobot-format generator running as a fleet of headless Isaac workers, with labelled mistakes and recoveries.
3. **Iterating on data by breaking the model.** Train, evaluate on paired seeded trays, take the failures apart, and change the generator. I did three generations of this.
4. **Pushing past π0.5.** π0.6 and π0.7 weights aren't open, so I borrowed the parts of their recipes that live in data and conditioning. I also trained **GR00T N1.7** on the same data for a head-to-head comparison.

All results below are measured in simulation on the same evaluation harness. Unless stated otherwise, every comparison is paired: same seeded trays, same 24 tries per tray, and a 95% confidence interval on the difference.

---

## 1. Simulating a suction cup that can actually fail

### The problem with "suction" in simulators

Isaac Sim's surface gripper is not a force. It fires a ray from the cup, and if it hits a rigid body within `maxGripDistance`, it **welds** that body to the tool with a joint. Our first data generator used a 30&nbsp;mm grab distance and 10,000&nbsp;N break limits. In practice the cup **grabbed gifts from 3&nbsp;cm away and never dropped anything**. Across 6,830 recorded grasps, the cup stopped anywhere from 4&nbsp;mm inside the gift to 12&nbsp;mm above it, and in a 614-grasp sample not one actually touched the gift. A policy trained on that data learns to "switch suction on near a gift". That habit doesn't survive a real robot.

### Step 1: a compliant tool and a seal model (PhysX)

I split the real tool's STL into a housing and a **spring-loaded plunger on a sliding joint**. The spring numbers come from a scale measurement: 75&nbsp;N/m, 3&nbsp;N preload, 20&nbsp;mm stroke. I added a **seal check**: the plunger must be pushed in at least 2&nbsp;mm, a ray from the lip must find a surface within 2&nbsp;mm, the surface must be tilted less than a randomized 12–20°, and all of this must hold for 0.1–0.3&nbsp;s. Lip diameter, seal delay, tilt tolerance and lip stiffness are randomized per episode.

<div class="row mt-3">
  <div class="col-sm-7 mt-3 mt-md-0">
    {% include video_if_exists.liquid path="assets/video/richtech/vla/compliant_vs_rigid_airgrab.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=false muted=true novolume=true %}
  </div>
  <div class="col-sm-5 mt-3 mt-md-0">
    {% include figure.liquid loading="lazy" path="assets/img/richtech/vla/bench_results.png" class="img-fluid rounded z-depth-1" %}
  </div>
</div>
<div class="caption">
  Left: the arm stops 5&nbsp;mm short of the box. The compliant tool (blue) waits for real contact and never seals. The stock rigid tool (orange) "grabs" through the air. Right: a headless bench of the simulated spring against the hand measurement (8.8&nbsp;N in sim vs 7.8–9.8&nbsp;N on the scale at full press).
</div>

I also matched the arm itself. I streamed single-joint cosine sweeps to the real right arm, replayed them in Isaac over a grid of 36 stiffness/damping settings, and picked per-joint gains. Residual tracking error is about 0.1° RMS once the real command delay (around 20&nbsp;ms) is included.

This fixed _when_ a seal happens, but not _when it lets go_. Once sealed, the gift was still glued on.

### Step 2: a vacuum suction cup as GPU kernels (Newton + Warp)

To get drops, peels and partial seals, the holding force has to be a real force. I rebuilt the cup in **Newton** (the open-source GPU physics engine behind Isaac Lab 3) as a reusable module, one lesson at a time. Every physics step runs three **Warp kernels**, after contacts are found and before the solver:

| Kernel                | Threads         | What it does                                                                                                                                                                                             |
| --------------------- | --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ring_gap_kernel`     | one per contact | Is one side a lip-ring point of some cup? Keep the smallest gap per ring point (`atomic_min`).                                                                                                           |
| `ring_surface_kernel` | one per contact | Record _what_ each ring point is touching (gift, tray, machine).                                                                                                                                         |
| `pressure_kernel`     | one per cup     | Turn ring gaps into a leak area, integrate pump flow against leak flow into a cup pressure, drive a simulated vacuum switch, and apply equal and opposite forces and torques to the surface and the lip. |

The model, in physical terms:

- **The lip is a ring of 64 small spheres** on its own body. That body hangs from the plunger on a D6 joint with two soft tilt axes and an axial **bellows** squash axis. Sixteen points turned out to be blind to a 1&nbsp;mm seam: it fell between two points and the cup "sealed" perfectly. With 64 points the seam opens a 34&nbsp;mm² leak and nothing lifts.
- **Leak area → pressure.** Each ring point contributes (lip arc length × its gap, plus surface roughness that pressing closes up). Porous cardboard adds its own leak term. The pressure follows the mass of air: d(pV)/dt = RT·ṁ<sub>leak</sub> − p·Q<sub>pump</sub>. The leak is a compressible orifice flow that **chokes** past about 48&nbsp;kPa of vacuum. The air volume follows the bellows length, so a sealed bellows collapses and lifts the gift several millimetres on its own, like the real cup. Each 50&nbsp;µs pressure sub-step is solved implicitly (by bisection) because the equation is stiff near zero vacuum.
- **Seal hysteresis.** A lip gap opens in about 2&nbsp;ms and reseals in about 20&nbsp;ms, because rubber settles back slowly.
- **A vacuum switch** reports "sealed" above 25&nbsp;kPa and "open" below 20&nbsp;kPa. That's the only signal the robot logic and the policy see, just like the real seal sensor.

No thresholds decide the outcome. An edge grip, a hover 3&nbsp;mm short, or a rigid lip on a 10° surface all get zero vacuum because their leaks are huge, not because a rule says so.

<div class="row mt-3">
  <div class="col-sm mt-3 mt-md-0">
    {% include video_if_exists.liquid path="assets/video/richtech/vla/4b1_tilt20.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=false muted=true novolume=true %}
  </div>
  <div class="col-sm mt-3 mt-md-0">
    {% include video_if_exists.liquid path="assets/video/richtech/vla/4b2_tall.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=false muted=true novolume=true %}
  </div>
</div>
<div class="caption">
  Left: the cup meets the gift at 20°. A rigid lip lands only 5 of 16 points and never lifts. The bendable lip tilts to match, seals, and holds. Right: a 1&nbsp;mm seam across the gift. Sixteen ring points are blind to it. Sixty-four points see it, the leak is 34&nbsp;mm², and the vacuum never builds.
</div>

<div class="row mt-3">
  <div class="col-sm mt-3 mt-md-0">
    {% include video_if_exists.liquid path="assets/video/richtech/vla/4b4_lift.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=false muted=true novolume=true %}
  </div>
  <div class="col-sm mt-3 mt-md-0">
    {% include video_if_exists.liquid path="assets/video/richtech/vla/4b3_edge.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=false muted=true novolume=true %}
  </div>
</div>
<div class="caption">
  Left: fixed-volume cup vs bellows cup, arm standing still. When the pump comes on, the sealed bellows collapses and the gift jumps up to the cup (the air volume drops by about a third). Right: lip 3&nbsp;mm inside the gift edge. 43 of 64 points touch, but the open side leaks 37&nbsp;mm², so there's no vacuum, no tipping, and no lift.
</div>

<div class="row mt-3">
  <div class="col-sm mt-3 mt-md-0">
    {% include figure.liquid loading="lazy" path="assets/img/richtech/vla/4b3_vacuum.png" class="img-fluid rounded z-depth-1" %}
  </div>
  <div class="col-sm mt-3 mt-md-0">
    {% include figure.liquid loading="lazy" path="assets/img/richtech/vla/4b4_leak_laws.png" class="img-fluid rounded z-depth-1" %}
  </div>
</div>
<div class="caption">
  Left: cup vacuum over time for several cases. It only builds where the lip actually seals, and it vents within tens of milliseconds when the pump turns off. Right: how much vacuum a pump can hold against a leak under three leak laws. My first, incompressible law was optimistic at deep vacuum, so I replaced it with compressible, choking flow.
</div>

### Many cups at once

Because the seal logic is in kernels, one cup and a thousand cups are the same code. Each copy lives in its own Newton "world" with its own parameters (tilt, gift mass, lip size, pump), and a **CUDA graph** replays the whole frame with one launch (36&nbsp;ms → 10&nbsp;ms per frame). With the full bellows cup, **1,024 cups ran at about 1,100× real time** on a shared RTX 5090. I use this for parameter maps that show where the cup holds and where it fails. The same sweeps are how the remaining guessed parameters will be fitted to bench tests on the real tool (pull-off, tilt, build-up time).

<div class="row mt-3">
  <div class="col-sm mt-3 mt-md-0">
    {% include figure.liquid loading="lazy" path="assets/img/richtech/vla/6_shake_map.png" class="img-fluid rounded z-depth-1" %}
  </div>
  <div class="col-sm mt-3 mt-md-0">
    {% include figure.liquid loading="lazy" path="assets/img/richtech/vla/6_bench.png" class="img-fluid rounded z-depth-1" %}
  </div>
</div>
<div class="caption">
  Left: 256 cups in one simulation, each shaken at its own amplitude and frequency. With the bellows, drops start around 3&nbsp;g, well past where the plunger spring gives way. Right: time per frame stays nearly flat from 1 to 1,024 copies. Without batching, the GPU was mostly waiting on Python.
</div>

<div class="row mt-3">
  <div class="col-sm mt-3 mt-md-0">
    {% include video_if_exists.liquid path="assets/video/richtech/vla/ex_gantry.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=false muted=true novolume=true %}
  </div>
</div>
<div class="caption">
  The cup knows nothing about our scene. Any body on any robot becomes a cup in four lines. Here it's on a two-axis gantry: a box, a standing can and a ball get delivered, and a can lying on its side never seals, because a flat ring touches a cylinder at only two points.
</div>

### Into Isaac Lab 3

Isaac Lab 3.0 runs on Newton, but its surface grippers still only work with PhysX on the CPU. **The Newton cup removes that blocker.** I ported the packing cell to Isaac Lab 3 with several environments in one simulation, the GPU cup on the robot, and the same planner and obstacle model as the production generator. In these episodes nothing holds the gift except the vacuum force and lip friction. There's no glue joint anywhere. After a round of fixes (robot placement, a straight-line final approach into the machine, a planner obstacle for the target gift, contact stiffness), a validation batch placed **192 of 192 gifts across 16 full episodes**, with no gift lost from the cup and no missed seal.

<div class="row mt-3">
  <div class="col-sm mt-3 mt-md-0">
    {% include video_if_exists.liquid path="assets/video/richtech/vla/lab3_4envs_4x.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=false muted=true novolume=true %}
  </div>
</div>
<div class="caption">
  Four packing environments from one Isaac Lab 3 / Newton simulation, 4× speed. Each pane shows the overview camera and the wrist camera, plus a status strip: phase, live cup vacuum in kPa, vacuum switch, and gifts placed.
</div>

The datasets in the next section were recorded with the compliant tool and seal model in Isaac Sim, since the cup work and the data campaign ran in parallel. The Isaac Lab 3 cell with the GPU cup is the generator for the next dataset generation, where drops and peels finally become part of the training distribution.

---

## 2. Recording datasets

The generator is a single long scripted episode per Isaac process. A motion planner (cuRobo at first, then Lula with a cuRobo fallback) solves every leg, and the episode is written as a **LeRobot** dataset with:

- **Two training cameras** (workspace overview and the wrist Orbbec, 640×480), plus a third review-only camera.
- A **17-D state**: both arms' joints, the suction command, and a **seal-sensor** bit that means what the real sensor will mean. **Actions** are the next frame's joint targets plus the suction command.
- **A phase label on every frame.** Deliberate mistakes are labelled with **negative phases**: feints, air grabs, phantom descents onto empty spots, near misses, bumps. The recovery that follows gets a positive phase. That labelling is what makes the advantage conditioning in section 4 possible.

To scale it, I run the generator as a **fleet of headless workers** (about 30 on an 8× RTX PRO 6000 server, in Docker, plus local GPUs). Workers restart every few dozen episodes so generator fixes apply to new chunks, and **watchdogs** catch Kit start-up faults that would otherwise silently write episodes with state but no video. I added quality gates (mp4 count per episode, settle and tilt checks, no gift removed mid-scene), and every new profile goes through a smoke batch, a review page and a frame montage before a full build.

<div class="row mt-3">
  <div class="col-sm mt-3 mt-md-0">
    {% include figure.liquid loading="lazy" path="assets/img/richtech/vla/lula_episodes_sheet.jpg" class="img-fluid rounded z-depth-1" %}
  </div>
</div>
<div class="caption">
  Review montage from one generator build: grid trays, free layouts, latch escapes and failure-focused episodes, with all camera views. Montages like this caught a rendering "ghost" artifact and a mirrored tray layout within seconds.
</div>

---

## 3. Iterating on the data by finding the model's weak points

My working rule became: **when more training steps stop helping, the model is limited by its data, so go find out exactly which situations it hasn't seen.** Each generation below follows the same loop: train, evaluate on paired seeded trays, mine the event logs and rollouts for failure modes, and change the generator.

### Generation 1: cuRobo + glued suction (≈ 50k episodes, ≈ 48M frames)

π0.5 LoRA runs climbed from about 8 to about **10.5 gifts per tray** as I added recovery data. Then checkpoints from 30k to 100k steps all scored the same within noise. That was the signal to stop training and start diagnosing:

- **Losses were concentrated.** 83% of lost gifts came from about 17% of trays, where the robot repeated the same failure 15–20 times.
- **Knocked gifts triggered the loops.** Attempt success fell from 80% when nothing had moved to 33% once any gift was more than 6&nbsp;cm off its spot. The generator aborted any episode where a gift moved more than 5&nbsp;mm, so **training never showed a disturbed tray**.
- **Phantom descents were the top failure** (42–48% of failed attempts): the arm descended onto the spot where a gift _used to be_.
- **The model under-used vision.** I ran perturbation tests on training frames. Swapping both camera images for another episode's moved the predicted actions about 12°. Swapping the joint state moved them **73°**. With images swapped at the same arm pose, actions moved only about 27% of the way toward the new target. It had learned "gifts sit on the 2×3 grid" from arm pose and pick history.
- **The grasps weren't grasps.** This is where the glue-joint finding above came from.

### Generation 2: compliant cup + Lula (11.5k episodes, 15.2M frames)

Free gift layouts, real contact at the grasp, a consistent arm-posture preference, and labelled phantom and air-grab recoveries. I also switched from LoRA to a **full fine-tune**:

| Model                         | Gifts / tray | Trays cleared |
| ----------------------------- | ------------ | ------------- |
| Generation 1 best (LoRA 53k)  | 10.50        | 64%           |
| Generation 2, LoRA 52k        | 11.20        | 79%           |
| **Generation 2, full FT 22k** | **11.56**    | **88%**       |

A held-out flow-matching loss on newer episodes bottomed out around 10k steps for the full fine-tune and rose afterward, while training loss kept falling. So the next runs were made shorter rather than longer.

Then I broke the new model down again, and the failure picture had changed completely. **All 35 lost gifts came from lock-ups.** A single failure was rare (9.5% of attempts after a success). Recovery was the problem: the failure rate was 42% after one failure and 88% after three in a row. The lock-ups were **joint wind-up**. Attempts starting within 10° of a joint limit failed 78% of the time. 90% of "hover and stall" attempts had a joint pinned at its limit, in postures far from anything in the data. The old escape library didn't help: the policy's real failure postures were a median of 87° away from its nearest pose.

### Generation 3: the policy's own failure states (7.7k episodes, 14.7M frames)

New generator profiles aimed squarely at those weak points: **escapes that start from the policy's recorded lock-up postures**, near misses, bumps, leaning and standing gifts, gifts on the tray rim, and disturbed trays. I mixed it 80/20 with generation 2 and fine-tuned from the best checkpoint. To measure what actually changed, I added harder evaluation variants: jostled trays, and a **recovery eval** that teleports the arm into one of 474 lock-up postures harvested from earlier rollouts.

| Eval (paired)                        | Gen-2 full FT 22k | **Gen-3 mix, step 10k** | Difference                   |
| ------------------------------------ | ----------------- | ----------------------- | ---------------------------- |
| Standard trays (79), gifts / tray    | 11.56             | **11.78**               | +0.23 ± 0.37 (no regression) |
| Recovery eval (47), gifts / tray     | 2.83              | **7.21**                | **+4.38 ± 1.16**             |
| Escaped a lock-up start              | 61%               | **90%**                 |                              |
| Placed a gift on the first try after | 23%               | **54%**                 |                              |

The standard eval was already near its ceiling, so the gain shows up where it was aimed: getting out of the states that used to eat whole trays. A scripted return-to-home after repeated failures, an upper bound on what a planned reset could add, gave +0.68 ± 0.90 gifts per tray on the older model. The data fix now gets most of that from the policy itself.

---

## 4. Turning π0.5 toward π0.6 and π0.7

Physical Intelligence's newer models aren't open: π0.6 uses a bigger Gemma 3 backbone and action expert, and π0.7 is built on top of it. Their papers describe recipe changes that mostly live in **data and conditioning**, not in the weights. So I implemented those on π0.5:

- **RECAP-style advantage conditioning (π\*0.6).** π\*0.6 conditions the policy on a binary "advantage positive/negative" label and steers toward positive at inference. I feed an **advantage flag** into the model. It's labelled from the generator's negative phases instead of a learned value model, and the robot always runs with flag = good. I checked that it actually steers the model: on recorded mistake frames, flag = bad reproduced the recorded mistake on 110 of 140 frames, and flag = good reproduced the clean motion on 64 of 88 (both p ≤ 10⁻⁵). That's what makes it safe to train on mistakes at all. It worked clearly on phantom descents and only weakly on air grabs.
- **Capacity.** I can't load π0.6's larger backbone, so the closest lever was moving from LoRA to a full fine-tune. That gave +0.36 gifts per tray and 79% → 88% trays cleared at the same data.
- **Prompt expansion with dropout (π0.7).** π0.7 adds episode metadata (speed, quality, mistakes), subtask text, and per-field dropout to the prompt. I built a per-frame prompt from my dataset labels: target-gift position, whether a gift is held, current subtask (from the phase), speed tercile of that pick cycle, and a mistake flag. I used π0.7's dropout scheme (15% of all metadata at once, 5% per field, plus 20–50% on target and subtask). Results, honestly mixed:
  - With target, speed and mistake fields: 11.79 vs 11.29 gifts per tray for the baseline on the same trays. A positive difference, but not significant on that sample.
  - With no extra text at inference: 8.36. The model genuinely learned to use the metadata.
  - The named target was followed only about 29% of the time, and an "unwind the arm" subtask prompt after repeated failures did not make the arm unwind. Steerability through text isn't there yet at this data scale.
- **Planned next, from the same papers:** train on my own labelled evaluation rollouts (RECAP plus π0.7-style distillation of suboptimal data with metadata), short image history, and training-time real-time chunking before real-robot tests. I deliberately skipped world-model subgoal images (a 14B model) and knowledge insulation for now.

---

## 5. π0.5 vs GR00T N1.7 on the same data

To check whether the remaining failures are a model problem or a data problem, I trained **NVIDIA GR00T N1.7** on exactly the same generation 3 + 2 mix: 8 GPUs, frozen backbone, relative arm actions, 32-step horizon, and the advantage flag as a state key. I put GR00T behind the same websocket protocol the openpi policy server speaks, so it runs on the **identical evaluation harness**, same trays and same scoring.

<div class="row mt-3">
  <div class="col-sm mt-3 mt-md-0">
    {% include video_if_exists.liquid path="assets/video/richtech/vla/groot_tray.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=false muted=true novolume=true %}
  </div>
</div>
<div class="caption">
  GR00T N1.7 (step 50k), 8× speed, on the same tray and seed as the π0.5 video at the top of the page: 12 of 12 gifts in 12 attempts, in about 8.5 minutes of sim time versus about 6 for π0.5.
</div>

| Paired standard trays (first 11) | π0.5, gen-3 mix 10k | GR00T N1.7, 50k |
| -------------------------------- | ------------------- | --------------- |
| Gifts / tray                     | 11.91               | 11.82           |
| Trays cleared                    | 91%                 | 91%             |

**Preliminary: a tie so far** (−0.09 ± 0.41 gifts per tray, 11 paired trays). Note the asymmetry: π0.5 starts from my earlier fine-tunes, while GR00T starts from the base model with a new action head, which is why it got more steps (50k evaluated here vs 10k for π0.5). The full 80-tray, jostled-tray and recovery evaluations are running now. I'll update this section when they finish. An earlier, smaller comparison of GR00T and π0 on an SO-100 arm is [here]({{ '/projects/12_project/' | relative_url }}).

---

## What I took from this project

- **Fix the physics before you fix the policy.** A glued suction cup quietly taught the model a behaviour that can't exist on hardware. A seal model, then a pressure model, made the data honest.
- **Plateaus in steps are a data signal.** Every time extra training stopped helping, the answer was in the failure logs, and it was a different answer each generation.
- **Aim data at the policy's own failure states.** Generation 3 didn't move the standard score much, but it more than doubled the recovery score. Choosing evaluations that can separate models mattered as much as the data.
- **Borrowing recipes is cheaper than waiting for weights.** RECAP-style conditioning works on π0.5. π0.7-style metadata is promising but not free.

## Limitations

- Everything here is simulation. The suction cup still has guessed parameters (vacuum level, pump flow, bellows stiffness, lip softness) until bench tests on the real tool, and the policy hasn't been deployed on hardware in this form yet.
- The newest datasets predate the GPU cup, so the trained models have not yet seen physical drops and peels.
- The GR00T comparison is early and small. The text-conditioning results come from partial evaluations.

## Note on sharing

Scene assets, the robot model, datasets, exact hyperparameters and internal infrastructure stay internal. The numbers and clips above are what I'm comfortable sharing at portfolio level.

---

**Related:** [Robot dog jumping RL]({{ '/projects/19_project/' | relative_url }}) · [Packing scene with a deformable bag]({{ '/projects/15_project/' | relative_url }}) · [RL reach policy]({{ '/projects/17_project/' | relative_url }}) · [Bimanual Rubik's + π0.5]({{ '/projects/14_project/' | relative_url }}).
