---
layout: page
title: Packing scene dataset with deformable bag simulation
description: Synthetic packing data on a Richtech-class bimanual setup; highlights soft-body / bag physics for contact-rich manipulation.
importance: 2
category: Work
related_publications: false
---

<div class="row mt-3">
  <div class="col-sm mt-3 mt-md-0">
    {% include video_if_exists.liquid path="assets/video/richtech/packing_deformable_bag.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=false %}
  </div>
</div>
<div class="caption">
  Primary camera: packing scene with a <strong>deformable plastic bag</strong> interacting with the environment and grippers. This is the “hard mode” sibling to rigid-object pipelines — contacts move, slip, and reform in ways cuboid meshes never do.
</div>

<div class="row mt-3">
  <div class="col-sm mt-3 mt-md-0">
    {% include video_if_exists.liquid path="assets/video/richtech/packing_deformable_bag_alt.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=false %}
  </div>
</div>
<div class="caption">
  Alternate viewpoint: same task family, different framing — useful for verifying that behavior is not a <strong>camera artifact</strong> and for future multi-view training.
</div>

# Packing under deformation: synthetic data when the world is soft

## Overview

While the [Rubik’s / handoff project]({{ '/projects/14_project/' | relative_url }}) stresses **rigid-body precision** and **bimanual timing**, this project asks a different question:

> What happens when the manipulated object is **not** a rigid part — when it is a **bag-like deformable** that folds, buckles, and settles under gravity and contact?

At **Richtech**, I built a **synthetic packing dataset** on a **bimanual manipulation stack** similar to other company cells. The novelty is not “two arms move” — it is that the **dominant modeling error** in the scene is **soft-body / thin-shell behavior**, which is historically where simulation teams lose weeks.

---

## Motivation

**Rigid sim is lying to you** in subtle ways when the task is packing, kitting, or bag manipulation:

- **Contact patches move** as material relaxes; static friction models tuned on cubes go stale.
- **Self-contact** (bag against bag, lip folding under finger pads) explodes solver work if meshes are sloppy.
- Policies trained only on rigid proxies **overfit to impossible dynamics** — they expect the world to stop moving when the gripper stops.

If we want IL/RL to survive **warehouse-style** tasks, we need datasets where **deformation is first-class**, not a post-hoc texture trick.

---

## Technical approach

### Scene composition

- **Bimanual cell** with the same control and observation conventions as other Richtech sim tasks (so engineers can reuse tooling).
- **Packing primitives**: support surface, target container or staging region, and clutter tuned to expose **grasp affordances** without impossible cages.
- **Deformable bag asset** with mesh resolution and material parameters chosen to be **expensive but honest** — under-meshed bags jitter; over-meshed bags never ship data.

### Physics tuning loop

Iterative work across:

- **Bending stiffness / damping** — too stiff reads as rigid plastic; too soft reads as cloth soup.
- **Friction between bag and fingers** — where most “I grasped it but it slipped” stories come from.
- **Solver substeps and iteration counts** — trading wall-clock against penetration artifacts.
- **Stability under parallel data generation** — a scene that works in UI but diverges at batch scale is a failed pipeline.

### Dataset intent

The dataset supports behaviors like:

- **Pinch and transport** of a deformable object through constrained openings.
- **Re-grasp and re-orient** when the first squeeze collapses the bag asymmetrically.
- **Placement** where the final support condition is **not** a single point contact — the bag spreads.

---

## Why this pairs with the rigid bimanual benchmark

- **Rigid handoff** teaches **coordination**; **deformable packing** teaches **contact distribution management**.
- Together they bracket what retail and logistics customers actually mean by “manipulation.”
- Training on **both** reduces the odds that a policy’s sim prior is **literally the wrong constitutive model**.

---

## Results & engineering outcomes

- A **repeatable deformable packing stage** that survives overnight generation batches.
- **Two reference camera streams** (see videos above) for debugging and for future multi-view models.
- Internal confidence that **cloth-like failures** are being seen **in sim before hardware**, not discovered after a customer demo.

---

## Lessons learned

- **Deformables punish bad collision margins** harder than rigid assemblies — invest in mesh cleanup early.
- **Camera placement** matters more than people admit; a viewpoint that hides self-contact will hide training bugs.
- **Quantitative metrics** (penetration depth, solver step count, success flags) need dashboards — eyeballing MP4s does not scale.

---

## Limitations & future work

- Richer **material identification** (different bag thicknesses, printed logos, moisture effects) if customers demand SKU-level diversity.
- **Hardware validation loop** on the same task graph — sim-first is necessary, not sufficient.
- Automated **mesh regression tests** when CAD updates a crimp or a seam length.

---

## Note on sharing

Specific material parameters, internal meshes, and throughput numbers stay **company-internal**. The clips above are approved for this portfolio.

---

**Related:** [Fleet Isaac Sim]({{ '/projects/13_project/' | relative_url }}) · [Rubik’s π0.5]({{ '/projects/14_project/' | relative_url }}) · [VR teleop]({{ '/projects/16_project/' | relative_url }}).
