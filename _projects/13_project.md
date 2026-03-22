---
layout: page
title: Company robot fleet in Isaac Sim
description: Migrated Richtech robots into Isaac Sim — bimanual arms, grippers, and mobile bases without manipulators.
importance: 4
category: Work
related_publications: false
---

## Overview

At **Richtech Robotics**, one of my first platform responsibilities was to stand up a **single, reliable simulation layer** for essentially **every robot the company ships or prototypes** — not just one cell or one SKU. The goal was straightforward to state and difficult to execute: **if it exists in hardware, it should exist in Isaac Sim** with the right kinematics, dynamics, collisions, and scene structure so downstream teams can generate data, debug controllers, and validate behaviors **before** tying up physical systems.

The scope deliberately mixed **high-DOF manipulation stacks** and **mobility-only platforms**:

- **Dual-arm cells with grippers** — full kinematic chains, tool frames, gripper limits, and contact geometry that must match CAD/URDF closely enough for imitation learning and policy evaluation.
- **Mobile bases without manipulators** — navigation-focused robots where the “sim value” is odometry, base–world interaction, and multi-robot layout rather than grasping.

This page is **text-first**: public demos on this site focus on **downstream manipulation and teleop projects** ([Rubik’s / π0.5]({{ '/projects/14_project/' | relative_url }}), [packing + deformable bag]({{ '/projects/15_project/' | relative_url }}), [VR teleop]({{ '/projects/16_project/' | relative_url }})).

---

## Motivation

Without a unified sim portfolio:

- **Every new policy or dataset experiment** risks a one-off URDF hack or a scene that only works on one engineer’s laptop.
- **Cross-team reproducibility** collapses — the same controller behaves differently depending on who imported the mesh last.
- **Sim-to-real debugging** becomes guesswork when collision margins, inertias, or joint ordering silently diverge from hardware.

A fleet-wide Isaac Sim baseline turns those problems into **engineering work you do once and version**, not tribal knowledge.

---

## What I built (technical scope)

### Asset import & fidelity

- **URDF and CAD-driven pipelines** for bringing mechanical data into sim: consistent link naming, joint axis directions, effort/velocity limits where available, and collision meshes that are **conservative enough** to avoid false negatives but **not so coarse** that free space disappears.
- **USD / stage organization** so scenes compose cleanly: robot instances, environments, sensors, and (where needed) **Replicator-style** hooks for later dataset work.

### Robot classes in the same framework

- **Bimanual + gripper systems** — independent arm chains, coordinated tool centers, and grasp frames that align with how policies expect to command actions.
- **Mobile robots without arms** — base models, footprint collisions, and sensor rigs appropriate to navigation and fleet scenarios, using the **same build conventions** as the manipulation line so teams don’t context-switch between two worlds.

### Physics and validation mindset

- Early emphasis on **stable contact** (reasonable friction/restitution, solver settings that don’t explode under manipulation loads).
- **Sanity checks** against hardware: joint travel, self-collision behavior, and gross motion parity — enough to trust sim for IL/RL iteration before spending nights on the real floor.

---

## Workflow integration

The fleet sim is not an art project; it is **infrastructure**:

- **Dataset generation** (vectorized Isaac Lab jobs, expert demos, domain randomization) assumes robots are **drop-in** from a maintained library.
- **Policy training** (e.g. π0-style stacks) assumes observation and action interfaces match between sim instances.
- **VR teleop and data collection** (see [VR project]({{ '/projects/16_project/' | relative_url }})) assume the same underlying models and frames as offline sim.

---

## Challenges (honest notes)

- **Heterogeneous hardware** means no single “golden” pipeline — mobile bases and dual-arm cells stress different parts of the stack (contact vs. rolling/slipping assumptions, different sensor sets).
- **CAD hygiene** varies by program phase; converting STL → sim-ready meshes (cleanup, materials, watertightness) is often the long pole, not pressing “import.”
- **Keeping parity over time** is the real job: when mechanical revs a bracket, sim must rev too, or policies silently train on the wrong geometry.

---

## Outcomes

- A **repeatable import + stage template** culture: fewer one-offs, more shared assets.
- **One simulation home** for both manipulation-heavy and mobility-only robots, so research and deployment engineering share vocabulary and file layout.
- Direct enablement of the **recorded projects** on this site — those videos sit on top of the same sim discipline described here.

---

## Future work

- Stronger **automated regression** (golden trajectories, contact probes, mesh diff alerts when CAD updates).
- Deeper **tuning guides** per robot class so new hires don’t rediscover solver settings.
- Optional **public-safe overview media** if the company approves a shareable clip — until then, this page stays descriptive.

---

**Related (with video):** [Rubik’s bimanual π0.5]({{ '/projects/14_project/' | relative_url }}) · [Packing + deformable bag]({{ '/projects/15_project/' | relative_url }}) · [VR teleop]({{ '/projects/16_project/' | relative_url }}).
