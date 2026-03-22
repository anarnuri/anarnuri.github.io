---
layout: page
title: "Bimanual Rubik's pick, handoff & π0.5 sim-to-real"
description: "~2k Isaac Lab episodes across parallel envs; π0.5 on mid-air handoff (right→left→place); strong real-robot results."
importance: 1
category: Work
related_publications: false
---

<div class="row mt-3">
  <div class="col-sm mt-3 mt-md-0">
    {% include video_if_exists.liquid path="assets/video/richtech/rubiks_sim_policy.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=false %}
  </div>
</div>
<div class="caption">
  Isaac Sim / Isaac Lab rollout: bimanual workspace, Rubik’s cube pick, mid-air handoff, and place. This clip is representative of the behaviors encoded in the synthetic dataset.
</div>

<div class="row mt-3">
  <div class="col-sm mt-3 mt-md-0">
    {% include video_if_exists.liquid path="assets/video/richtech/rubiks_real_robot.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=false %}
  </div>
</div>
<div class="caption">
  Real hardware after π0.5 fine-tuning: same task structure (pick → mid-air transfer → place), demonstrating that the policy survives contact noise, calibration drift, and timing effects that never appear in pure simulation.
</div>

# Bimanual Rubik’s manipulation: Isaac Lab data at scale, π0.5 fine-tuning, and real-robot execution

## Overview

This project is a **full-stack manipulation story** on a **dual-arm platform** at **Richtech**: learn a non-trivial, contact-rich behavior end-to-end from **large synthetic corpora**, then close the loop on **physical hardware** with a modern vision–language–action stack (**π0.5**).

The task is intentionally **structured but hard**:

1. **Right arm** grasps a **Rubik’s cube** from the workspace.
2. Performs a **mid-air handoff** to the **left arm** (coordination, timing, and grasp stability matter).
3. **Left arm** places the cube on the table to complete the episode.

The point is not “solve the puzzle” — it is to stress **bimanual sequencing**, **in-flight exchange**, and **repeatable success** under real-world variability.

---

## Why this task is a good benchmark

- **Single-arm pick-and-place** is a solved demo in many labs; **mid-air handoff** couples two independent contact chains — failures are abrupt and informative.
- **Cube geometry** is regular enough for repeatable grasps but unforgiving to alignment error.
- The behavior is **easy for humans to teleop or script as expert prior**, but **hard for policies** unless data coverage and sim fidelity are serious.

---

## Data generation (Isaac Lab)

**Engine:** **Isaac Lab** with a **vectorized / multi-environment** setup so generation is closer to “throughput engineering” than clicking through one scene.

**Scale:** on the order of **~2k episodes** for the training corpus used in the π0.5 fine-tuning iteration shown on hardware.

**What varies across episodes (high level):**

- **Initial cube and hand poses** within safe random ranges so the model sees diverse approach directions.
- **Scene and camera configuration** consistent with what the policy will see at deployment time (avoid training on viewpoints that never appear on the robot).
- **Timing and motion style** diversity when using scripted or expert-derived motions — brittleness often hides in “always the same tempo.”

**Operational focus:**

- Stable **physics** during grasp and handoff (contact not exploding, hands not ghosting through meshes).
- **Deterministic logging** of actions and observations so training debugging is possible weeks later.
- **Batch efficiency** — if generating data is slow, nobody iterates; parallel envs were central.

---

## Learning: π0.5 fine-tuning

**π0.5** is fine-tuned on the synthetic corpus (plus any curated real segments we blended in for gap closure — the exact mixture is part of the internal recipe).

**Training priorities:**

- **Alignment** between sim observation statistics and the real camera stream (even strong models fail if color/contrast/exposure distributions lie).
- **Temporal consistency** across the handoff segment — the policy must not “forget” the second arm during the exchange.
- **Regularization** so success is not memorized narrow corridors of initial conditions.

---

## Sim-to-real evaluation

Hardware evaluation is **non-negotiable** here: the handoff is exactly where **small sim errors** become **large real failures**.

**What we looked for beyond binary success:**

- **Variance across seeds / sessions** — a policy that works once is not a product.
- **Recovery** after minor slippage — does the chain stall or adapt?
- **Contact sounds and wrench signatures** (informal) — catching grasps that “look” fine in video but are mechanically marginal.

**Qualitative outcome:** after iteration, **real-robot runs matched the qualitative reliability** we expected from the best sim rollouts — not pixel-identical motion, but **stable task completion** under normal lab disturbance.

---

## Results & impact (inside Richtech)

- A **reusable bimanual data recipe** — not a one-off Jupyter notebook, but a generation layout other tasks can fork.
- Proof that **mid-air handoff** can be carried by **π0.5-class policies** when data volume and sim hygiene are treated as first-class.
- A **template for reporting**: sim clips + hardware clips side-by-side, same task graph, easy for leadership and collaborators to audit.

---

## Lessons learned

- **Mid-air phases** need **extra data mass** compared to static grasps — the manifold of valid states is thinner.
- **Finger / gripper compliance** in hardware shows up as **timing noise**; sim must exaggerate slightly or real will undercut you.
- **Episode length discipline** matters — padding with useless stationary frames dilutes the handoff signal.

---

## Limitations & future work

- Broader **lighting and background randomization** if the cell moves from lab bench to customer floor.
- Explicit **failure recovery policies** (handoff misses, partial drops).
- Tighter **quantitative scoreboard** (success vs. attempts, time-to-completion) for regression testing after each CAD rev.

---

## Note on sharing

Implementation details, exact configs, and some visuals are **company-internal**. This page documents **what was built and why** at a depth similar to my public research projects; the videos above are cleared for the portfolio.

---

**Related:** [Fleet Isaac Sim migration]({{ '/projects/13_project/' | relative_url }}) · [Packing + deformable bag]({{ '/projects/15_project/' | relative_url }}) · [VR teleop]({{ '/projects/16_project/' | relative_url }}).
