---
layout: page
title: Automating Data Generation and AI Inference with myCobot 280 PI & iPhone App
importance: 1
category: Projects
related_publications: false
---

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/real_labels.png" title="Automated Dataset Generation with myCobot 280 PI" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    The myCobot 280 PI robotic arm automates dataset creation by mimicking human hand movements. Cameras capture images of labels on motorized rewinders, simulating real-world motion. This setup reduces manual effort while ensuring consistency for object detection tasks. A companion iPhone app (shown below) enables real-time model inference in the field.
</div>

# Automated Dataset Generation, Object Detection, and Mobile Deployment

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include video.liquid path="assets/video/app_demo.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=true %}
    </div>
</div>
<div class="caption">
    A demo video showcasing the app's functionality and results.
</div>

## Overview

As a **Machine Learning Engineer** at **Zortag**, I automated dataset generation, optimized object detection models, and deployed an **iPhone app for real-time inference**. Zortag’s 3D QR code technology demands high-accuracy authentication, and this project integrated robotics, computer vision, and mobile development to streamline the pipeline.

**Key Components**:

- Robotic arm automation for scalable data collection
- YOLOv8 fine-tuning (99.84% accuracy)
- Synthetic data generation
- **iPhone app** for on-device model inference (_video demo at the beginning_)

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

- Developed a **native iOS app** to run optimized YOLOv8 models on-device.
- Features:
  - Real-time QR code detection via camera
  - Offline-capable inference (CoreML)
  - User-friendly UI for field authentication

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
