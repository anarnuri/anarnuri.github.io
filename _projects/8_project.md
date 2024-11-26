---
layout: page
title: Path Generative Model Based on Conditional β-Variational Autoencoder for Four-Bar Mechanism Design
importance: 1
category: work
related_publications: false
---

## Overview

This paper introduces a novel methodology for the design of planar four-bar mechanisms using a Conditional β-Variational Autoencoder (cβ-VAE). The model is capable of generating diverse mechanism designs for a given coupler curve while allowing for user-defined constraints such as mechanism type. By integrating cross-attention and self-attention layers, the model effectively captures the interdependencies between mechanism parameters and coupler curves, providing a robust framework for mechanism synthesis.

[**Access the dataset on Kaggle**](https://www.kaggle.com/datasets/purwarlab/four-bar-coupler-curves)

---

## Key Contributions

1. **Innovative Neural Network Architecture**:

   - Incorporates cross-attention and self-attention layers for enhanced performance.
   - Introduces a unified representation for different four-bar mechanism types.

2. **Extensive Dataset**:

   - Includes RRRR, RRRP, and RRPR mechanism types with open and closed coupler curves.
   - Normalized for translation, rotation, and scale invariance.

3. **Metrics for Evaluation**:

   - Proposes hierarchical metrics to assess reconstruction quality, novelty, and diversity.

4. **Generative Capabilities**:
   - Produces multiple mechanism designs approximating a given coupler curve.
   - Allows for the exploration of the latent space to discover novel solutions.

---

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/beta_1.png" title="Overview of cβ-VAE Model" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
   This overview figure illustrates our proposed methodology. In the training phase, the model processes mechanisms by incorporat-
   ing them with their respective coupler curves and types, which serve as conditions, into an encoder. This process generates a latent vector.
   This vector, when reintegrated with the coupler curves and mechanism types (conditions), enables the decoder to recreate the original
   mechanism accurately. After the model is fully trained, it has the capability to navigate the latent space, allowing it to generate a variety
   of mechanisms tailored to specific coupler curves and mechanism types. For example, when provided with a particular curve (highlighted
   in the figure) and different mechanism types, the model can produce suitable mechanisms, as demonstrated in the output section of the
   figure.
</div>

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/beta_2.png" title="Overview of cβ-VAE Model" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Overview: The model integrates user-defined conditions into a cβ-VAE framework, enabling the generation of diverse mechanisms for desired coupler curves and mechanism types.
</div>

---

## Methodology

- **Model Architecture**:

  - Utilizes a cβ-VAE with cross-attention for condition integration and self-attention for mechanism prediction.
  - Combines latent vector representations with user-specified conditions.

- **Dataset**:

  - Comprises over 4 million mechanisms across three types (RRRR, RRRP, RRPR).
  - Each mechanism is represented as joint coordinates and a corresponding coupler curve.

- **Training**:
  - Conducted on a dataset split into 80% training and 20% testing.
  - Optimization of β values to balance reconstruction accuracy and latent space structuring.

---

## Results and Insights

1. **Reconstruction Quality**:

   - Dynamic Time Warping (DTW) was used to evaluate the similarity between input and generated coupler curves.
   - Best results achieved with β = 25, balancing accuracy and diversity.

2. **Novelty and Diversity**:

   - Novelty assessed using L2 norms between generated mechanisms.
   - Diversity ensured by evaluating the representation of all mechanism types in the results.

3. **Cognate Mechanisms**:
   - Unified algorithm enables the generation of cognates, expanding the solution space for mechanism design.

---

## Applications

- **Conceptual Design**:
  - Generates diverse mechanism designs, aiding early-stage exploration.
- **Optimization**:
  - Provides initial solutions that can be refined further.
- **Automation**:
  - Facilitates rapid generation of mechanism designs under specific constraints.

---

## Future Directions

This work lays the foundation for extending the approach to higher-order mechanisms, spatial linkages, and more complex kinematic tasks. Future research could also explore real-time applications and integration with other machine learning models for automated mechanism design.

[**Download the dataset here**](https://www.kaggle.com/datasets/purwarlab/four-bar-coupler-curves)
