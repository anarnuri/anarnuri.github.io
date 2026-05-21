---
layout: page
title: "Iterating reward shape on an RL reach policy"
description: A PPO + diff-IK reach policy with obstacle avoidance — moved from a stuck ~18-mm plateau to roughly 5-mm position / 1° orientation by iterating heavily on reward shape. Intended to feed a VLA dataset pipeline that replaces scripted trajectories.
importance: 1
category: Work
related_publications: false
---

<div class="row mt-3">
  <div class="col-sm mt-3 mt-md-0">
    {% include video_if_exists.liquid path="assets/video/richtech/pick_place_rl_reach.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=false muted=true novolume=true %}
  </div>
</div>
<div class="caption">
  Short playback excerpt of the trained PPO policy on the <strong>staggered-curriculum (10I)</strong> checkpoint, reaching a randomized 6-DoF goal in the single-arm reach + obstacle-avoidance task (≈6&nbsp;mm position, ≈3° orientation — the best-balance variant from the campaign described below). Full sweep across 128 parallel environments available on request.
</div>

# Iterating reward shape on an RL reach policy

## Overview

At **Richtech**, I built a single-arm **reach + obstacle-avoidance policy** intended to sit underneath later VLA / dataset work — the idea being that a learned policy could eventually replace the scripted / cuRobo-planned motion stages that produce our synthetic data. Scripted trajectories are fine for regression tests, but they aren't a great training distribution for a generalist model. The policy needed to:

- Reach a **6-DoF goal pose** with roughly sub-cm position precision and degree-level orientation precision (the actual targets I ended up with are below).
- **Avoid a vertical obstacle** sitting in the most useful part of the workspace.
- Produce **smooth, mechanically healthy** motion — joints not pinned at the velocity cap, no wrist chatter, no visible suspension bob at policy bandwidth.
- Generalize across **a wide command-sampling box** rather than a single rehearsed trajectory.

Most of the calendar time on this went into iterating on **reward shape**, not PPO hyperparameters, so that's mostly what this writeup is about. A few sim-side fixes turned out to matter more than reward changes too, which I'll flag explicitly when they come up.

---

## Task setup

- **Robot**: bimanual Mobile DEX cell, one arm actuated (6 DoF), the other arm held at a static pose for now.
- **Action**: **delta-pose Cartesian** (3 + 3-axis-angle) → **Damped-Least-Squares IK** → joint-position target → PD controller. The IK target is clamped to soft joint limits before being handed to the actuator, which prevents the policy from commanding configurations it shouldn't.
- **Observation**: joint pos / vel for the actuated arm, current EE pose in the robot root frame, pre-computed delta-to-target, last action.
- **PPO**: standard on-policy stack (RSL-RL), 256/128/64 ELU MLPs, 4096 parallel environments, 6000–10000 iterations depending on variant.
- **Episode**: 6&nbsp;s — long enough that the policy spends the last ~4&nbsp;s **at the goal**, not racing toward it.

An early choice I think paid off was the **action space**: delta-pose IK instead of raw joint targets. With this action space the gradient of "move closer to goal" is geometric rather than learned, and the joint-limit clamp short-circuited a class of failure modes (singularities, wraparound) that I've seen hand-rolled IK actions produce. I didn't ablate this — could be that raw-joint-targets would have worked too with enough training — but it's the choice I'd repeat for a similar task.

---

## Iterating on reward shape

I kept a running log of every change with **what / why / result / verdict**. With ~15 reward variants over a couple of weeks, that log was the only way I could keep track of what I was actually comparing against — without it I'd have been re-running the same experiments under slightly different names.

### Multi-scale tracking, the first plateau

I started with a fairly standard pattern: a linear position-error penalty plus a stack of `1 − tanh(d / std)` bonuses at several `std` values, on the theory that one of the kernels would have a useful gradient at any given distance. Same shape for orientation. Plus the usual smoothness terms — `action_rate`, `joint_vel`, and an `ee_velocity_damping` cap that scales with distance.

Training drove position error from ~30&nbsp;cm down to **~1.8&nbsp;cm**, then stopped improving. Multiple reward variants — different obstacle weights, different smoothness curricula, even a goal-distribution filter — converged to roughly the same 17-19&nbsp;mm equilibrium. That consistency made me suspicious that the plateau wasn't a learning failure but something about the reward stack itself.

When I sat down and tabulated the kernel values across distance, the suspicion looked plausible:

| Distance | broad kernel | mid kernel | ultra-fine kernel |
|---|---|---|---|
| 5.0&nbsp;cm | 0.84 (saturated) | 0.46 (peak gradient) | 0.00 (dead) |
| **1.8&nbsp;cm** | **0.94 (saturated)** | **0.66 (falling)** | **0.0006 (dead)** |
| 0.5&nbsp;cm | 0.98 (saturated) | 0.90 (saturated) | 0.42 (alive) |

There's a **10× gap between the mid kernel (std=0.05) and the ultra-fine kernel (std=0.005)** with nothing in between. At ~1.8&nbsp;cm — where every run was getting stuck — all three position-tracking terms looked weak: the two broad ones are saturated (gradient ≈ 0), the ultra-fine one isn't awake yet. At the same time, the smoothness penalties were fully ramped. My reading was that the policy was trading the last bit of precision for smoothness, and the equilibrium happened to land in this gap. I can't prove it's the *only* explanation, but the next experiment was consistent with it.

### Threshold penalties: what broke the plateau (at least once)

The change that moved the number was conceptually small. I added a **non-saturating linear penalty** above a threshold:

> if the policy sits above 18&nbsp;mm of position error, it keeps paying a constant per-step cost — the only way to zero it out is to be inside the threshold.

The reasoning: smooth tanh kernels have gradient that vanishes near the goal; a linear penalty's gradient is constant (independent of distance) until the policy is inside the threshold, where it shuts off. The soft kernels still do the coarse approach; the threshold penalty pulls the policy through the last few mm.

Position error went from the stuck 18&nbsp;mm equilibrium to roughly 5&nbsp;mm in that one run. That's consistent with the gradient-gap reading from the table above, but it's also a single experiment — I'm not claiming it generalizes beyond this task.

### Greedy on one axis broke another

Applied to position only, orientation regressed: from ~1° to ~5°, because the policy seemed to contort the wrist into whatever configuration put the EE origin closest to the goal. `joint_vel_at_limit` jumped about 4× at the same time, which read as the policy hitting velocity caps trying to force itself into the position threshold.

I added a symmetric threshold penalty for orientation, calibrated so the per-step cost magnitudes were in the same ballpark. With both active, both metrics ended up inside their thresholds (pos ≈ 12&nbsp;mm, orn ≈ 0.87°). That was the first run where both numbers were inside spec at the same time — not the best on either axis individually, but the first that didn't sacrifice one for the other.

### Pareto trade-off (in this task, with this reward stack)

Tightening either threshold past a point seemed to come at the other axis's expense:

| Variant | pos_err | orn_err | notes |
|---|---|---|---|
| **10D** | 12.0&nbsp;mm | **0.87°** | best orientation precision |
| **10F** | **4.5&nbsp;mm** | 4.27° | best position precision |
| 10I | 6.0&nbsp;mm | 3.27° | first stable run with active orn pressure |
| 10N | 15.3&nbsp;mm | 1.38° | soft-kernel-driven regime, longer training |

Across the active frontier I roughly traded ~1&nbsp;mm of position for ~0.5° of orientation. Getting both 5&nbsp;mm *and* ~1° in the same run would have needed an orientation weight that destabilized training (see below). Whether that's a fundamental property of the task or just of this reward shape, I can't say from one campaign.

Two runs (Exp 10G / 10H) tried larger orientation weights from a cold start. Both collapsed mid-training: value function loss diverged, the policy never recovered. The same target weights were stable when I reached them via a staggered curriculum — start at a weight the policy could handle, let it find an attractor, then bump. My takeaway here is narrow: in this task, the weight value alone wasn't enough to predict stability — the starting condition relative to it mattered at least as much. Whether that generalizes to other reward stacks I haven't tested.

---

## Things that surprised me along the way

Four observations from this campaign that I'd at least *check for* on a similar task next time — not necessarily generalizable laws:

- **Penalising joint velocity at the actual saturation layer worked better than clamping the EE rate.** I first tried capping `rot_scale` at the action layer, which sounded tidier, but the IK Jacobian can amplify small EE deltas into large joint deltas near wrist singularities, so the cap didn't actually bound joint velocity. A soft barrier penalty in the 80%→100% band of the URDF velocity cap shifted the saturating joint from wrist to elbow (which has more effort capacity) and dropped the bad-episode fraction from ~33% to ~10%. n=1.

- **Suspension joint dynamics turned out to be a noise floor on EE precision.** Visual inspection of the "best" policy showed a few-mm vertical bob while the arm "held" pose. The prismatic suspension joint had `ω_n ≈ 5.6 Hz` with `ζ ≈ 0.88` — under-damped and well inside the 30 Hz policy bandwidth. Bumping stiffness 10× and damping 20× moved it to `ω_n ≈ 16 Hz`, overdamped. The same checkpoint then played back at ~80% inference success instead of 73%, with no policy retraining. I wouldn't claim "sim fixes always beat reward fixes," but on this run a sim-side change beat a campaign's worth of reward iteration on that particular metric.

- **Episode length wasn't a wall-clock knob, it was a reward knob.** I cut `episode_length_s` from 6 → 4 hoping to save training time. The policy converged to a worse local optimum — faster approach, more joint saturation, parked slightly short of the goal. My read: the last few seconds at the goal were where the sub-cm tanh kernel was doing useful work, so removing them shifted the equilibrium. Reverted within one training run.

- **Filtering "hard" goals at training time hurt deployment.** I added a filter excluding goals too close to the obstacle (which the policy was visibly backing off from). Training metrics looked great — orientation error dropped to 0.5°. Playback success regressed by 5 percentage points. The training and eval distributions diverged: the policy stopped practicing the cases that matter most at deployment. The fix is obvious in retrospect (filter both or neither), but I needed to see it fail to fully buy it.

---

## The ~80% playback ceiling

Across the twelve stable variants in this series, every 128-environment playback session landed at roughly 80% success. Training-time position error ranged 4.5–15.3&nbsp;mm and orientation 0.87–4.27° across those variants, but playback success barely moved. My best guess is that the remaining ~20% are a **task-difficulty floor** — goals inside or beside the obstacle footprint, goals near workspace boundaries, goals where the avoidance pose seems incompatible with the required orientation. I haven't proven that's all of them; I'd want to break the failure cases down by (init, goal) pair to be confident.

For the downstream use case (synthetic data for VLA training) the 80% is acceptable as-is: failed episodes get filtered at generation time, and the successful 80% have smooth motion, healthy joint velocities, and sub-cm to sub-mm precision on the easier goals. If the ceiling does turn out to be more about reward shape than task difficulty, that would be a follow-on project.

---

## Where this is heading

The downstream goal is to extend this kind of learned-motion policy into the [packing scene dataset]({{ '/projects/15_project/' | relative_url }}), where the current motion is cuRobo-planned. cuRobo gives kinematically correct trajectories but they're tightly clustered around the planner's preferences — my hypothesis (still to validate) is that a VLA fine-tuned on too-clean data is going to overfit to those preferences rather than the underlying task.

The trained reach policy in this writeup is the simplest building block. The in-progress extension is the same robot in the full packing scene, right-arm controlled, with a suction-gripper engagement stage added. The reward-shape decisions described above are what I'm reusing as the starting point — multi-scale tanh stack, threshold penalty for the last few mm, staggered curriculum for the orientation regularizers. Whether the playbook transfers cleanly or breaks in new ways is itself part of what the next project will tell me.

---

## What I took from this campaign (caveats included)

Hedged on purpose — these are observations on **one task** with **one reward stack family**, not laws.

- **Reward shape moved the needle far more than PPO hyperparameters did, here.** I didn't see a hyperparameter change that came close to the impact of (a) adding a non-saturating term above a threshold, or (b) fixing the suspension dynamics. That ordering might be specific to this task.
- **The plateau in this campaign looked like a gradient gap.** The 18&nbsp;mm floor across multiple variants matched where my kernel-saturation table predicted the gradient would be weakest, and a term that filled the gap moved the floor. I don't know whether *every* plateau is a gradient gap — that's a hypothesis worth checking next time, not a conclusion.
- **A non-saturating term above a threshold was the only thing I found that pulled the policy through the last few mm.** Tanh kernels by construction lose gradient near zero. If precision matters, I'd start by checking whether the reward has *any* term whose gradient stays alive near the goal.
- **A sim-side fix beat a reward iteration on this run.** 7 points of inference success from one stiffness/damping change is a lot. I take that as a reminder to scan the simulation for "is this dynamics actually what I want?" before assuming the policy is the bottleneck. Not a universal claim that sim always wins.
- **A running what / why / result / verdict log saved me from running the same experiment twice.** This is more about process than RL, but it's the thing I'd lift wholesale to any future campaign of this kind.

---

## Limitations & what I haven't proven

- I haven't shown that hitting **5&nbsp;mm AND 1° simultaneously** is impossible — only that I didn't reach it with the reward stack and command distribution I tried. Narrower command sampling, a recurrent policy, or a different reward structure could plausibly close that gap.
- The 80% playback ceiling is consistent with task-difficulty floor, but I haven't actually classified the 20% failures by cause. That's the diagnostic I'd run next.
- The reward-shape playbook above is what I'm reusing in the **packing-scene extension** — until that run finishes I can't say whether the playbook transfers or breaks on multi-stage tasks.

---

## Note on sharing

Specific reward weights, threshold values, curriculum schedules, and the underlying training infrastructure stay internal. What's in this writeup is the high-level reward-shape reasoning, the plateau diagnosis, and the trade-off pattern I observed — described at the level I'd be comfortable being wrong about. The clips above are approved for portfolio use.

---

**Related:** [Bimanual Rubik's + π0.5]({{ '/projects/14_project/' | relative_url }}) · [Packing scene dataset]({{ '/projects/15_project/' | relative_url }}) · [VR teleop]({{ '/projects/16_project/' | relative_url }}).
