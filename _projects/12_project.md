---
layout: page
title: 🔬 Benchmarking Gr00t & Sim-to-Real on the SO100 Arm
importance: 1
category: Projects
related_publications: false
---

# Benchmarking Open Control Models — Real-world Lessons from DL-RL

### **“Open-source control models promise plug-and-play robotics — but do they really work off the shelf?”**

At **DL-RL** I built an end-to-end pipeline to answer that exact question. We used the SO100 robotic arm, large synthetic datasets from Isaac Sim, and extensive fine-tuning and evaluation to measure how well open control models (e.g., **Gr00t**) actually perform in real-world deployment. The short answer: they can be powerful, but only when you understand how they were trained and when your fine-tuning, data, and evaluation are done carefully.

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include video.liquid path="assets/video/episode_000001.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=false %}
    </div>
</div>
<div class="caption">
    See the SO100 arm performing picking red cube task.
</div>

**Perfect for:**

- Robotics researchers studying **open-source action models**
- Teams evaluating open-source control models before production use
- Anyone building reproducible benchmarks and practical training guides

---

## Why this work matters

### 🔎 Benchmarking over hype

Many recently released control models are marketed as “off-the-shelf” solutions. Our work shows that realistic deployment requires more than downloading a checkpoint:

- **Hyperparameter sensitivity.** Getting robust behavior often depends heavily on fine-tuning choices (learning rate schedules, batch sizes, augmentation, regularization, etc.). Small differences in training recipe can lead to large differences in real-world performance.
- **Dataset coverage matters.** Models generalize well only when the training distribution reasonably covers the target tasks and edge cases. Rare motions, specific grasps, or unique environment lighting quickly reveal gaps.
- **Sim-to-real nuances.** High-fidelity simulation reduces the gap but does not eliminate it; evaluation on hardware is essential. We run closed-loop tests to catch failure modes that never appear in sim.
- **Reproducibility is non-negotiable.** To make benchmarking useful, we must publish training configs, random seeds, evaluation scripts, and dataset generation code — not just numbers.

Because of these realities, we treat this project as a **benchmarking and transparency effort**: not only to build a working system, but to document what actually works, what fails, and why.

---

## Lessons & insights (high level)

- Always version **datasets + generation scripts + training configs** together — models are meaningless without their data and recipe.
- Run **ablation studies** on key hyperparameters and augmentations; some “default” settings break under real hardware noise.
- Track metrics beyond task success (e.g., stability, recovery behavior, variance across seeds) to surface brittleness.
- Continuous dataset expansion (captured real imagery + sim variations) materially improves robustness when incorporated into fine-tuning.

---

## Achievements & deliverables

- Generated and published **large-scale synthetic datasets** for the SO100 arm (see Hugging Face). Datasets receive steady community downloads and are versioned for reproducibility. ([Hugging Face link placeholder](https://huggingface.co/anurizada)).
- **Fine-tuned Gr00t** on combined simulated + real data, then deployed and evaluated on the physical SO100 arm. Closed-loop experiments achieved **~90–95% success rates** on pick and pick-and-place tasks in our testbed.
- Built a complete benchmarking suite (data generation → training → hardware evaluation) and documented the **training recipes, hyperparameter sweeps, and failure cases**.
- Commitment to publication: we will release a **detailed benchmarking report** (code, configs, logs, and evaluation scripts) so the community knows what to expect from open control models and how to reproduce/improve our results.

---

## How to access our work

- Datasets and preliminary artifacts are available on [Hugging Face](https://huggingface.co/anurizada).
- The full benchmarking report, training configs, and evaluation scripts will be published alongside an open repository when the manuscript is released.

<div class="alert alert-success" role="alert">
  Our goal is to give researchers clear, reproducible guidance for using and evaluating open control models in real robots.
</div>

---

## My promise to researchers and practitioners

1. Publish **complete** recipes (data + config + code) so others can reproduce and extend our benchmarks.
2. Share **actionable guidance** — which hyperparameters matter, how to expand datasets, and how to interpret results on hardware.
3. Maintain the datasets and tools as an open resource to accelerate rigorous sim-to-real research.
