---
layout: page
title: "Teaching a robot dog to jump onto boxes (RL, in progress)"
description: "PPO in Isaac Lab for the MirrorMe BPX quadruped: from flat walking to a true running jump onto 70–80 cm boxes, one reward idea per round. Then realistic motors, a camera-only student, and a 3D-printed depth-camera mount."
img: assets/img/richtech/bpx/thumb_jump.jpg
importance: 0.5
category: Work
featured: true
related_publications: false
---

<div class="row mt-3">
  <div class="col-sm mt-3 mt-md-0">
    {% include video_if_exists.liquid path="assets/video/richtech/bpx/v8b_box70_slowmo.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=false muted=true novolume=true %}
  </div>
</div>
<div class="caption">
  Best policy so far: a true jump onto a 70&nbsp;cm box, 4× slow motion. All four feet leave the ground and the dog lands directly on top. There's no scrambling up the face and no front-paws-first mantle. Simulation only.
</div>

# Teaching a robot dog to jump onto boxes

## Overview

This is my current project. The goal is to get the **MirrorMe BPX quadruped** to run at a box and get on top of it, then move that skill toward the real robot. Training is **PPO (RSL-RL) in Isaac Lab** with 4,096 dogs in parallel. I started from MirrorMe's public flat-walking task and added an obstacle task, a terrain curriculum, evaluation tooling, and a long series of reward experiments.

Most of the work has been **reward design against shortcuts**. RL finds the cheapest behaviour the rules allow. Twice, the success numbers looked perfect while the video showed something I didn't want.

Where it stands:

- **Height-map policy:** 100% success on 10–70&nbsp;cm boxes, and 88–92% on an 80&nbsp;cm box, with an actual jump.
- **With realistic motors** (torque that fades with speed, plus command delay): 98–100% up to 70&nbsp;cm. 80&nbsp;cm is lost.
- **Camera-only student** distilled from that teacher: training now.
- **Depth-camera mount** for the real robot: designed, checked against the CAD, ready to print.

---

## Setup

- **Observation:** body angular velocity, gravity direction, velocity command, 12 joint angles and velocities, and the last action (45 numbers). For the box task I add a **height scan**: 17×11 ground-height rays covering 1.1&nbsp;m ahead and 0.5&nbsp;m behind. The scan is shifted forward because a centred scan would give less than a second of warning at 1&nbsp;m/s.
- **Action:** 12 joint-position offsets from the standing pose, tracked by a PD motor model at 50&nbsp;Hz. That's the same command type the BPX SDK accepts.
- **Terrain:** a grid of tiles where **row = difficulty** (box height). Each tile randomizes the box's distance from spawn (0.8–3&nbsp;m), its depth and its angle (±15°). If the box were always 1&nbsp;m away, the policy could learn "jump after one second" without ever looking at it.
- **Curriculum:** a dog that gets past the box moves up a row. One that covers less than 40% of the commanded distance moves down.

<div class="row mt-3">
  <div class="col-sm-7 mt-3 mt-md-0">
    {% include figure.liquid loading="lazy" path="assets/img/richtech/bpx/terrain_tiles.png" class="img-fluid rounded z-depth-1" %}
  </div>
  <div class="col-sm-5 mt-3 mt-md-0">
    {% include figure.liquid loading="lazy" path="assets/img/richtech/bpx/height_scan.png" class="img-fluid rounded z-depth-1" %}
  </div>
</div>
<div class="caption">
  Left: terrain tiles with randomized box distance, depth and angle. Right: the height-scan footprint, shifted forward so the dog sees the box coming.
</div>

The curriculum's average row is not a skill metric: dogs that clear the top row get sent to a random row, so even a perfect policy averages about row 5–6. So I wrote a **fixed-height evaluator**. It runs 40–50 dogs per box height on gap-free square boxes and reports success, falls, longest flight time, steps spent pushing on the box face, and "straddle" steps (front paws on top, hind feet still on the floor). Its contact timeline (which feet touch, every 20&nbsp;ms) is the most reliable proof of what the dog is actually doing.

---

## One idea per round

Each round started from the previous best checkpoint and usually trained two variants side by side, so I could see which change helped.

| Round | Change                                                                                                  | Result                                                                       | Lesson                                                                                                                                                                          |
| ----- | ------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| v1    | Box task, 5–30&nbsp;cm                                                                                  | Crashed at iteration ~550 with NaN                                           | One physics blow-up in 4,096 dogs poisons a whole PPO batch. I added a termination for blown-up dogs and a guard that zeroes non-finite rewards and observations, then resumed. |
| v1b   | Resumed with the guards                                                                                 | **100% on every row, 5–30&nbsp;cm, 0 falls**                                 | The pipeline works. The curriculum ceiling was the limit.                                                                                                                       |
| v2    | Boxes 10–70&nbsp;cm                                                                                     | 100% at 30–45&nbsp;cm, **5% at 10–15&nbsp;cm**                               | Catastrophic forgetting: the curriculum moved every dog up and nobody practised low boxes.                                                                                      |
| v3    | 25% of resets to a random row; looser posture penalties                                                 | 100% up to 55&nbsp;cm                                                        | Mixing fixes forgetting. The posture limits were capping height.                                                                                                                |
| v4    | Boxes up to 1.6&nbsp;m deep                                                                             | 100% to 70&nbsp;cm, but the video showed a **wall scramble**                 | The numbers said success. The behaviour wasn't what I wanted.                                                                                                                   |
| v5    | −1 per foot pushing on a vertical face                                                                  | Scrambling −40%, no jump                                                     | A penalty has to cost more than the shortcut gains.                                                                                                                             |
| v6    | Wall penalty −10 / −40                                                                                  | 100% to 70&nbsp;cm, **0 wall pushes**, front paws on top plus a hind-leg hop | The dose matters.                                                                                                                                                               |
| v7    | Approach speed 1–2&nbsp;m/s                                                                             | **100% to 70&nbsp;cm, 92% at 80&nbsp;cm**, a running jump                    | Change the situation so the behaviour you want becomes the efficient one.                                                                                                       |
| v8    | Penalty for the "mantle" pose (supporting front foot more than 25&nbsp;cm above a supporting hind foot) | **100% to 70&nbsp;cm, 88% at 80&nbsp;cm, 0 straddle steps**                  | Define the behaviour precisely, then price the alternatives.                                                                                                                    |

<div class="row mt-3">
  <div class="col-sm mt-3 mt-md-0">
    {% include video_if_exists.liquid path="assets/video/richtech/bpx/v4b_box70.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=false muted=true novolume=true %}
  </div>
  <div class="col-sm mt-3 mt-md-0">
    {% include video_if_exists.liquid path="assets/video/richtech/bpx/v7a_box80.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=false muted=true novolume=true %}
  </div>
</div>
<div class="caption">
  Left, v4: "100% success" on a 70&nbsp;cm box, achieved by scrambling up the face. Right, v7: a faster approach turns it into a running jump, here onto an 80&nbsp;cm box.
</div>

{% include figure.liquid loading="lazy" path="assets/img/richtech/bpx/v8b_box60_jump.png" class="img-fluid rounded z-depth-1" %}

<div class="caption">
  v8 on a 60&nbsp;cm box, frame by frame: approach, take-off, flight with all four feet in the air, and landing on top.
</div>

---

## Toward the real robot

The policies above get a perfect height map and motors that deliver 30&nbsp;Nm at any speed. Neither is true on the real BPX, so the next rounds remove those shortcuts one at a time.

**Realistic motors (v9).** Real motors lose torque as they spin up, and the motor bus adds delay. MirrorMe doesn't publish a torque–speed curve, so I bracketed it with two DC-motor models: 30&nbsp;Nm at stall falling to zero at 20&nbsp;rad/s (pessimistic) or 30&nbsp;rad/s (moderate), each with a random 0–20&nbsp;ms command delay. Both kept **98–100% on 10–70&nbsp;cm** with no scrambling or straddling. The 80&nbsp;cm jump dropped to 0% and 24%. So with realistic motors the limit sits between 70 and 80&nbsp;cm. I chose the pessimistic model as the teacher for the next step.

**Camera-only student (training now).** The real dog has no height scanner. It will have an **Orbbec Gemini 335L** depth camera. The student sees the 45 body readings plus a 48×32 simulated depth image from the camera's actual mount pose (25° down, 30&nbsp;Hz, 0.17–3&nbsp;m range, noise, 2% missing pixels), with an MLP + GRU for memory. It's distilled from the v9 teacher. The sim also carries the mount's 0.4&nbsp;kg and penalizes front hip roll beyond ±0.7&nbsp;rad, because past that the thigh can hit the camera (see below).

<div class="row mt-3">
  <div class="col-sm mt-3 mt-md-0">
    {% include figure.liquid loading="lazy" path="assets/img/richtech/bpx/cam_view_50cm.png" class="img-fluid rounded z-depth-1" %}
  </div>
</div>
<div class="caption">
  What the student sees: the simulated 48×32 depth input as the dog walks toward a 50&nbsp;cm box, from 0.3&nbsp;m to 2.6&nbsp;m into the run. The dark specks are dropped pixels.
</div>

### A depth-camera mount, designed from the CAD

To put that camera on the robot, I designed a two-part, 3D-printed bracket in parametric CadQuery. I worked only from MirrorMe's public STEP and URDF plus Orbbec's datasheet, because nobody had measured the real robot yet:

- **Fixing:** it bolts into the top T-slots of the two upper 2020 extrusion rails with four M5 drop-in T-nuts. I identified the rail profile from the STEP part names and measured the slot section in the CAD. No disassembly is needed.
- **Field of view:** I ray-cast from the depth optical centre against the robot meshes in the standing pose. At **25° down**, 0% of the image is occluded by the robot. The ground is visible from about 0.3&nbsp;m ahead out past 2&nbsp;m, and the top edge sits 5–9° above the horizon, so tall boxes stay in view. 30° lost too much of the box tops, and 20° lost the near ground.
- **Leg clearance:** I swept both front legs over the full URDF joint limits (6,825 configurations per leg). Clearance is 35&nbsp;mm in normal gait and 21&nbsp;mm up to 0.7&nbsp;rad of hip roll. At full abduction the thigh touches the camera, and moving the camera didn't fix that, so the controller and the sim both limit front hip roll instead.
- **Falls:** a frontal hit lands on the robot's metal handle and motors 19&nbsp;mm before the camera. A back-flip is the real exposure, so the printed base is designed as the fuse that fails before the frame or the camera.
- **Into the sim:** the camera pose (position plus quaternions in three conventions), the added mass, and the bracket as a collision body all feed straight into the Isaac Lab task above.

<div class="row mt-3">
  <div class="col-sm-7 mt-3 mt-md-0">
    {% include figure.liquid loading="lazy" path="assets/img/richtech/bpx/assembly_on_bpx_tilt25.png" class="img-fluid rounded z-depth-1" %}
  </div>
  <div class="col-sm-5 mt-3 mt-md-0">
    {% include figure.liquid loading="lazy" path="assets/img/richtech/bpx/fov_view_tilt25.png" class="img-fluid rounded z-depth-1" %}
  </div>
</div>
<div class="caption">
  Left: the bracket (orange) and camera (blue) on the BPX meshes, with the depth field of view. Right: the ray-cast depth view from the mount pose. No part of the robot is in frame.
</div>

---

## What I took from it so far

- **Always watch the video.** Twice, the evaluation said "success" while the behaviour was a scramble or a mantle.
- **Reward what you want and price the shortcuts.** Weak penalties just tax a shortcut. A strong enough one removes it. Sometimes changing the situation (approach speed) works better than another penalty.
- **Change one thing per variant** and test every variant on the same fixed-height benchmark.
- **Measure what the curriculum can't.** The average terrain level hid both forgetting and real progress. Fixed-height tests and contact timelines didn't.

## Limitations and next steps

- Everything is simulation so far. The camera student hasn't finished training, and nothing has run on the real robot.
- The motor models are bracketed guesses until I can measure the real actuators. The real jump height will probably be lower than in sim.
- Next: finish and evaluate the camera student, print and fit the mount, calibrate the camera extrinsics on the robot, and move toward hardware tests with conservative box heights.

---

**Related:** [Gift-packing VLA and GPU suction cup]({{ '/projects/18_project/' | relative_url }}) · [RL reach policy and reward shaping]({{ '/projects/17_project/' | relative_url }}).
