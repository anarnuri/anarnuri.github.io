---
layout: page
title: VR teleoperation for dual arms & hand gripper
description: VR stack to command both arms and a hand-style gripper—natural grasping on diverse objects for data collection and testing.
importance: 3
category: Work
related_publications: false
---

<div class="row mt-3">
  <div class="col-sm mt-3 mt-md-0">
    {% include video_if_exists.liquid path="assets/video/richtech/vr_dual_arm_hand.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=false muted=true novolume=true %}
  </div>
</div>
<div class="caption">
  VR-driven teleoperation: operator controls **both arms** and a **hand-style gripper** on real hardware. The clip highlights natural grasping on heterogeneous objects and the kind of fast iteration loop that is painful to replicate with script-only interfaces.
</div>

# VR teleop as a product-grade interface for bimanual hardware

## Overview

**Scripted trajectories** are perfect for regression tests and repeatability. They are **terrible** for exploring the long tail of grasps humans perform without thinking.

At **Richtech**, I implemented a **VR teleoperation stack** that lets an operator **drive two arms** and a **dexterous / hand-style gripper** on **physical robots**, with enough polish that the system is useful for:

- **Demonstration collection** for imitation learning (fast “show the robot” loops).
- **Edge-case probing** before policies exist (what if the object is thinner, offset, or occluded?).
- **Controller bring-up** when ROS graphs and low-level drivers need a human in the loop.

This project is the **human I/O layer** sitting beside the sim datasets ([Rubik’s]({{ '/projects/14_project/' | relative_url }}), [packing]({{ '/projects/15_project/' | relative_url }})) and the fleet sim foundation ([fleet migration]({{ '/projects/13_project/' | relative_url }})).

---

## Motivation

Traditional teach pendants and joint-space sliders do not match **task-space intent**:

- Operators think in **poses, contacts, and affordances**, not “joint 4 +0.03 rad.”
- **Bimanual coordination** is cognitively serial on a keyboard — in VR it can be parallel.
- **Hand grippers** with multiple modes (pinch, power, hook) need **continuous intuitive input**, not discrete GPIO toggles.

VR is not magic; it is a **latency-sensitive control problem**. The engineering is making it **safe, repeatable, and logged**.

---

## System design (high level)

### Input → command path

- **VR poses and button/gesture events** mapped to **arm Cartesian targets** or **incremental deltas** (mode-dependent).
- **Gripper commands** synthesized from hand pose + digital actions — supporting **discrete primitives** (pinch vs. spread) where the hardware requires it.
- **Rate limiting and workspace fences** so a tracking glitch does not become a wrench spike.

### Integration

- **ROS**-aligned bridges where the existing robot stack expects topics/services.
- **Calibration discipline**: headset frame, base frame, and arm bases must agree or teleop feels “swimmy” and operators lose trust in minutes.

### Operator experience goals

- **Low cognitive load** for common grabs — if teleop is exhausting, nobody collects data.
- **Clear mode indicators** (which arm is “armed,” which gripper mode is live).
- **Logging hooks** for later IL — timestamps, command streams, and (when available) camera frames associated with motion segments.

---

## What this unlocked internally

- **Faster iteration** on hardware bring-up than waiting for full policy training cycles.
- **Human priors** for tasks that are annoying to script (deformable starts, awkward re-grasps).
- A **shared language** between research and deployment: “try it in VR first” replaces ad-hoc Python one-offs.

---

## Challenges (real ones)

- **Latency**: VR-to-robot loops must stay inside what operators perceive as “direct control.”
- **Safety**: even with fences, **human reflex + machine inertia** requires conservative defaults and e-stops.
- **Hardware heterogeneity**: not every end-effector accepts the same abstract gripper API — adapters are part of the work.

---

## Lessons learned

- **Trust beats features** — a boring, stable teleop mode beats a flashy one that glitches.
- **Session logging is not optional** if IL is the consumer of demonstrations.
- **Calibration time is cheaper** than debugging “mysterious” failures later.

---

## Limitations & future work

- **Haptic feedback** is still limited on many headsets — force-closure cues remain visual.
- **Automated segmentation** of “good” vs. “abort” trajectories from long VR sessions.
- **Two-operator protocols** if tasks truly need simultaneous independent intent (rare but real).

---

## Note on sharing

Control graphs, exact topic names, and safety parameters are **internal**. The demo above is cleared for external portfolio use.

---

**Related:** [Fleet Isaac Sim]({{ '/projects/13_project/' | relative_url }}) · [Rubik’s π0.5]({{ '/projects/14_project/' | relative_url }}) · [Packing + deformable bag]({{ '/projects/15_project/' | relative_url }}).
