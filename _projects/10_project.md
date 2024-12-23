---
layout: page
title: Automating data generation using myCobot 280 PI
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
    The myCobot 280 PI robotic arm automates the dataset creation process by mimicking human hand movements. Equipped with cameras, the arm captures images of labels attached to two motorized label rewinders. These rewinders simulate real-world motion by dragging and rewinding labels as the robotic arm adjusts its camera angles and positions. This setup not only reduces manual effort but also ensures consistency and efficiency in dataset generation for object detection tasks.
</div>

# Automated Dataset Generation and Object Detection Optimization with myCobot 280 PI

## Overview

As part of my role as a **Machine Learning Engineer** at **Zortag**, I spearheaded the automation and optimization of dataset creation and object detection processes. Zortag specializes in creating **highly secure 3D QR codes**, a groundbreaking technology aimed at revolutionizing authentication, traceability, and counterfeit prevention across industries.

The project involved integrating cutting-edge robotics and computer vision technologies to streamline data generation, enhance model performance, and improve overall pipeline efficiency. By programming and automating a robotic arm and leveraging advanced object detection models, this initiative significantly reduced manual effort and increased the robustness of Zortag’s machine learning solutions.

**Note**: The code and the dataset for this project are private and not publicly available due to the proprietary nature.

---

## Key Contributions

1. **Automation with Robotic Arm**:

   - Programmed and automated the **myCobot 280 PI robotic arm** to capture images of Zortag's 3D QR codes.
   - Designed motion sequences mimicking human-like behavior, ensuring consistent and comprehensive image capture from multiple angles.
   - Reduced manual effort, enabling the team to scale dataset creation without compromising quality.

2. **Model Fine-Tuning**:

   - Fine-tuned **YOLOv8**, a state-of-the-art object detection model, on a newly generated dataset of Zortag's QR codes.
   - Improved object detection accuracy from 90% to near **99.84%**, showcasing expertise in optimization and real-world deployment.
   - Enhanced the model’s ability to detect and differentiate intricate patterns within Zortag's 3D QR codes.

3. **Synthetic Data Generation**:

   - Developed a **synthetic dataset** of "fake" Zortag 3D QR codes to supplement real-world data.
   - Applied data augmentation and generative techniques to create a diverse dataset that improved model robustness and generalization.
   - Ensured models performed reliably in varied and challenging environments, reducing dependency on physical data collection.

4. **Streamlined Labeling Pipeline**:
   - Automated the dataset labeling process, eliminating the need for manual input.
   - Reduced human error and improved efficiency by implementing automated annotations, enabling faster iterations in model training.

---

## Methodology

1. **Robotic Arm Programming**:

   - Utilized Python and ROS (Robot Operating System) to design motion paths and automate image capture.
   - Integrated the robotic arm with cameras and lighting systems to optimize image quality for machine learning.

2. **Object Detection Model Optimization**:

   - Used **PyTorch** to fine-tune YOLOv8 on a mix of real and synthetic data.
   - Employed techniques such as hyperparameter tuning, transfer learning, and augmented training.

3. **Pipeline Automation**:
   - Simulated various lighting conditions, rotations, and backgrounds to train models for real-world robustness.
   - Built an end-to-end automated pipeline for data collection, labeling, and model training using tools like OpenCV and custom scripts.
   - Established a feedback loop to iteratively improve model performance based on validation results.

---

## Results and Impact

- **Increased Efficiency**: Automated processes reduced dataset creation time by over **90%**, freeing up resources for other critical tasks.
- **Near-Perfect Accuracy**: Fine-tuned YOLOv8 achieved nearly **100% detection accuracy**, surpassing initial benchmarks.
- **Scalable Solutions**: The combination of synthetic and real-world data enhanced model generalization, enabling deployment across diverse scenarios.
- **Enhanced Security**: The robust object detection pipeline directly contributes to Zortag’s mission of providing secure and reliable authentication solutions.

---

## Applications

- **Authentication and Traceability**:
  - Strengthened Zortag’s ability to verify genuine products and prevent counterfeiting.
- **Industrial Automation**:
  - Demonstrated the potential of robotics in automating repetitive tasks with high precision.
- **Custom AI Solutions**:
  - Set a precedent for integrating machine learning and robotics in real-world applications.

---

## Future Directions

- **Edge Deployment**:
  - Optimize object detection models for deployment on edge devices, enabling real-time QR code authentication in the field.

This project showcases how the intersection of robotics and machine learning can drive innovation, efficiency, and reliability in critical industries.
