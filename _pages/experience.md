---
layout: page
permalink: /experience/
title: Experience
nav: true
nav_order: 2
description: Robotics, simulation, and machine learning roles — industry and research.
---

Detailed timeline of my professional and research positions. For **portfolio-style write-ups**, see [Work]({{ '/projects/' | relative_url }}), [Research]({{ '/research-projects/' | relative_url }}), and [Personal projects]({{ '/personal-projects/' | relative_url }}).

---

## Richtech Robotics USA

**Robotics Engineer** · Dec 2025 – Present · Las Vegas, NV

- Ported **Richtech’s robot fleet** into **Isaac Sim** — **dual-arm manipulators with grippers** and **mobile robots without hands** — with consistent URDF/CAD import, collisions, and reusable USD workflows. **[Project →]({{ '/projects/13_project/' | relative_url }})**
- Built a **bimanual Rubik’s cube** task: right arm picks, **mid-air handoff** to left arm, place on table; **~2k episodes** via **Isaac Lab** multi-environment / vectorized generation; **π0.5** fine-tuning with **strong sim-to-real** on hardware. **[Project →]({{ '/projects/14_project/' | relative_url }})**
- Created a **packing-scene** synthetic dataset (similar bimanual platform) with a **deformable bag** in sim — high-difficulty soft / contact-rich manipulation; includes a polished **demo video** on the project page. **[Project →]({{ '/projects/15_project/' | relative_url }})**
- Implemented **VR teleoperation** for **dual arms** and a **hand gripper** to grip diverse objects and support data collection on real systems (**ROS** where needed). **[Project →]({{ '/projects/16_project/' | relative_url }})**
- Ongoing: **PhysX** tuning (contact, friction, deformables), **cuRobo**-style planning integration where applicable, **Blender** mesh prep for sim assets, and large-scale **imitation / policy-training** dataset tooling beyond the projects above.

---

## DL-RL

**Robotics Engineer Intern** · Apr 2025 – Dec 2025 · Brooklyn, NY

- Built **large-scale synthetic datasets** in **Isaac Sim** for the **SO-100** and **Trossen** arms using IK-driven rollouts, domain randomization, and multi-sensor pipelines; published datasets on [Hugging Face](https://huggingface.co/anurizada) (1k+ monthly downloads).
- Developed end-to-end **Isaac Sim / Omniverse** workflows: scene and physics setup, **USD** stage management, CAD/URDF integration, camera rigs, and **Replicator**-based auto-annotation for fully labeled synthetic data.
- Designed and ran robotics simulation tasks — manipulation, grasping, and pick-and-place — to validate policies before **real hardware** deployment.
- Fine-tuned **Gr00t** and **π0** models in **PyTorch** on synthetic and real data; closed-loop testing on the physical SO-100 arm with **90–100%** task success on benchmark routines.

**Project write-up:** [Benchmarking Gr00t & sim-to-real on the SO100 arm]({{ '/projects/12_project/' | relative_url }}).

---

## Stony Brook University

**Graduate Research Assistant** · Sep 2020 – Dec 2025 · Stony Brook, NY

- Designed and trained **multi-modal LLM-style models** with **Mixture-of-Experts (MoE)** for path synthesis, built from scratch with a hybrid **ViT + decoder** architecture; **CLIP**-style contrastive learning and Gaussian soft objectives, with ~**15%** accuracy gains over strong baselines at ~**200 ms** inference latency.
- Improved training efficiency with **Classifier-Free Guidance** and **LoRA** (~**30%** compute reduction); gradient tracking, adaptive clipping, and CLIP-aligned objectives for cross-modal consistency.
- Developed **β-VAE** and **graph-based VAE** models for structured latent representations supporting multi-modal generation and downstream reasoning.
- Co-authored **ASME JMD** work on a **3M-sample** planar linkage dataset for ML-driven path synthesis and **ASME JMR** work on **conditional β-VAE** path generative models for mechanism design.
- Ran systematic studies comparing **curve representations** (Fourier descriptors, wavelets, point coordinates, images) inside unified generative frameworks for four-bar coupler synthesis.
- Led end-to-end ML work: curation and preprocessing of **12M+** multi-modal samples; distributed training of **sub-1B** transformer models on **SLURM**-managed HPC; scaling experiments on cloud GPUs; **200+** experiments tracked with **PyTorch Lightning**, **Hugging Face**, and **Weights & Biases**.

---

## Zortag

**Computer Vision Engineer** · Aug 2024 – Aug 2025 · St. James, NY

- Fine-tuned **YOLOv11**, pushing detection accuracy toward **~100%** and cutting latency by replacing a two-step pipeline with a single optimized model.
- Automated **myCobot 280 PI** capture workflows (**~60%** less manual work, **~3×** labeling throughput) with automated **AWS S3** uploads for dataset growth.
- Shipped a real-time **iPhone QR** detector (**SwiftUI** + **CoreML**), containerized with **Docker** for scalable deployment.
- Built a **real-time screen/display detection** stack in the internal **`documents/screen_Detector`** path: **CLIP ViT-L/14@336** + **MLP** (YOLO was not sufficient for reliable screen boundaries in the wild), **WebSocket** streaming from the phone camera, **5-crop TTA**, **EMA** smoothing, and **3-frame hysteresis** for stable live inference under **~1 s** latency.
- Developed training utilities with **albumentations**, batched GPU feature extraction, stratified splits, and disk-level caching (**scikit-learn**, **PyTorch**) for fast iteration across classifier architectures.

**Related portfolio page:** [Dataset automation with myCobot & iPhone]({{ '/projects/10_project/' | relative_url }}).
