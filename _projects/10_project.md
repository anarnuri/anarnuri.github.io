---
layout: page
title: Automating Data Generation and AI Inference with myCobot 280 PI & iPhone App
category: Work
importance: 3
related_publications: false
---

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/real_labels.png" title="Automated Dataset Generation with myCobot 280 PI" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    The myCobot 280 PI robotic arm automates dataset creation by mimicking human hand movements. Cameras capture images of labels on motorized rewinders, simulating real-world motion. This setup reduces manual effort while ensuring consistency for object detection tasks. The companion iPhone app (demo below) runs on-device vision in the field—not only <strong>3D QR</strong> authentication, but also a live <strong>screen / display</strong> signal (laptops and monitors), where glare, moiré, and weak box-like boundaries made a standard detector a poor fit.
</div>

# Automated Dataset Generation, Object Detection, and Mobile Deployment

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include video_if_exists.liquid path="assets/video/app_demo.MP4" class="img-fluid rounded z-depth-1" controls=true autoplay=false %}
    </div>
</div>
<div class="caption">
    A demo video showcasing the app's functionality and results.
</div>

## Overview

As a **Machine Learning Engineer** at **Zortag**, I automated dataset generation, optimized object detection models, and shipped an **iPhone app for real-time inference**. Zortag’s 3D QR stack needs high-accuracy authentication; the same product flow also needed the phone to **know when a laptop or monitor screen** was in view. That second problem sounds simple, but in practice **screens are not “nice” detection targets**: large regions, uneven texture, glare, and moiré meant a **YOLO-style bounding-box model** we tried first kept **missing or jittering** on real hardware.

I addressed that with a **CLIP ViT-L/14@336 image encoder** feeding a **small MLP** for a **stable yes/no screen decision**, with frames streamed over **WebSockets**, **multi-crop inference at test time**, **EMA smoothing**, and a short **hysteresis window** so the UI did not flicker—end-to-end roughly **sub-second** behavior on live video. The robotics and QR pieces are what most people see first; the screen pathway was the parallel engineering thread that made the **whole authentication story** usable outside a lab.

**Key Components**:

- Robotic arm automation for scalable data collection
- YOLOv8 fine-tuning (99.84% accuracy) for QR / label tasks
- Synthetic data generation
- **iPhone app**: CoreML + SwiftUI, **QR inference** plus the **CLIP + MLP screen head** above (_video demo at the beginning_)

**Note**: Code and datasets are proprietary.

---

## Key Contributions

### 1. Robotic Automation & Dataset Generation

- Programmed **myCobot 280 PI** to capture multi-angle images of 3D QR codes via human-like motions.
- Motorized label rewinders simulated real-world movement, reducing manual effort by **90%**.

### 2. Model Optimization

- Fine-tuned **YOLOv8** for anomaly detection using hybrid real/synthetic data, achieving **99.84%** detection accuracy for **fake** 3D QR codes.
- Automated labeling pipelines eliminated manual annotation errors.

### 3. iPhone App for Inference

- Developed a **native iOS app** to run optimized **YOLOv8** (CoreML) for **3D QR** work on-device.
- Added **live screen / display detection** for field use: **CLIP + MLP** with streaming, multi-crop evaluation, and temporal smoothing so the app could trust the signal in uneven lighting.
- **Offline-capable** where the models allow it; **SwiftUI** UI aimed at operators in the field.

---

## Methodology

1. **Robotics**: Python/ROS-controlled arm trajectories with OpenCV-based image capture.
2. **ML Pipeline**:
   - Synthetic data augmentation (varied lighting/backgrounds).
   - YOLOv8 fine-tuning via **PyTorch** and **CoreML** conversion for **iOS**.
3. **Mobile Deployment**:
   - Optimized model for edge performance (**CoreML**).
   - **SwiftUI** frontend with camera integration.

---

## Results & Impact

- **Efficiency**: 90% faster data generation vs. manual methods.
- **Accuracy**: 99.84% detection under real-world conditions.
- **Deployment**: iPhone app enables field authentication without cloud dependency.

---

## Future Work

- Expand the training dataset to cover more real-world cases.
- Port to Android for broader adoption.
