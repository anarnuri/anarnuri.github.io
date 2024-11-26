---
layout: page
title: A Dataset of 3M Single-DOF Planar 4-, 6-, and 8-Bar Linkage Mechanisms With Open and Closed Coupler Curves for Machine Learning-Driven Path Synthesis
importance: 1
category: work
related_publications: false
---

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/dataset.png" title="our image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Overview: the training phase and inference phase steps are bounded by green dash-dot lines and red dashed lines, respectively.
</div>


## Overview

This paper introduces a groundbreaking dataset containing nearly 3 million single-degree-of-freedom planar mechanisms, encompassing 4-bar, 6-bar, and 8-bar linkage mechanisms with both open and closed coupler curves. The study addresses a critical gap in the field of machine learning-driven path synthesis by presenting the first comprehensive dataset of this magnitude and diversity.

By offering a standardized evaluation framework with six key metrics — accuracy, novelty, diversity, robustness, computational efficiency, and scalability — this work sets a benchmark for comparing machine learning models for mechanism synthesis. Additionally, it proposes a novel pipeline using Variational Autoencoders (VAEs) combined with k-nearest neighbor (k-NN) searches to synthesize mechanisms, demonstrating the dataset's utility and effectiveness.

[**Access the dataset on Kaggle**](https://www.kaggle.com/datasets/purwarlab/four-six-and-eight-bar-mechanisms-with-curves)

---

## Key Contributions

1. **Comprehensive Dataset**:
   - Includes 4-bar mechanisms with revolute and prismatic joints and higher-order mechanisms (6-bar and 8-bar).
   - Encompasses open and closed curves, filling gaps in prior datasets like LINKS.

2. **Standardized Metrics**:
   - Proposes six evaluation metrics to objectively compare machine learning approaches in mechanism design.

3. **Innovative Methodology**:
   - Demonstrates the potential of VAEs to represent and synthesize diverse coupler curves.
   - Introduces latent space exploration to generate diverse solutions for a given input curve.

4. **Evaluation of Latent Space**:
   - Explores optimal latent dimensions for VAE models, concluding that a 10-dimensional latent space balances performance and efficiency.

5. **Real-World Applications**:
   - Validates the dataset’s practical relevance by testing it with novel coupler curves using an application like MotionGen.

---

## Dataset Highlights

- **Size**: ~3 million samples of 4-bar, 6-bar, and 8-bar mechanisms.
- **Structure**: Organized into folders containing normalized coupler curves and corresponding Cartesian coordinates.
- **Usability**: Includes scripts for loading and preprocessing data, adhering to FAIR principles (Findable, Accessible, Interoperable, Reusable).

---

## Methodology

1. **Dataset Generation**:
   - Uses a simulation algorithm capable of handling revolute and prismatic joints.
   - Mechanism filtering ensures practical designs by limiting extreme link ratios and joint overlaps.

2. **Variational Autoencoders**:
   - Trained on coupler curves embedded as 64x64 pixel images.
   - Maps curves to a latent space, enabling efficient retrieval of similar mechanisms.

3. **Evaluation Metrics**:
   - Analyzes accuracy, novelty, and diversity of generated mechanisms.
   - Assesses robustness against noisy and unseen data.

---

## Results and Insights

- **Accuracy**: A 10-dimensional latent space achieves optimal accuracy with minimal computational overhead.
- **Diversity**: Generated mechanisms span all types in the dataset, ensuring comprehensive representation.
- **Novelty**: Mechanisms generated exhibit significant variation, demonstrating the model's ability to synthesize innovative designs.
- **Robustness**: Maintains performance across noisy inputs and generalizes to unseen coupler curves.

---

## Future Directions

The study highlights potential expansions, including:
- Extending the dataset to include higher-order mechanisms (spherical and spatial).
- Integrating conditional VAEs to allow user-defined mechanism constraints.
- Adapting the approach to more complex motion generation problems.

---

## Applications

This dataset and methodology have broad applications in robotic path synthesis, automated design systems, and computational kinematics, paving the way for innovations in mechanism design.
