---
layout: page
title: Generating Diverse Planar Four-Bar Mechanisms with Conditional beta-VAE
importance: 1
category: work
related_publications: false
---

# Generating Diverse Planar Four-Bar Mechanisms with Conditional beta-VAE

## Introduction

Hey there! I’ve been working on a cool project that uses a Conditional beta-Variational Autoencoder (c-beta-VAE) to generate different types of four-bar mechanisms based on a given coupler curve. What makes our approach unique is the integration of cross- and self-attention layers within the VAE framework. This helps capture the complex relationships between mechanism parameters and coupler curves.

We also developed a unified way to represent four-bar mechanisms, whether they have revolute or prismatic joints. Our method uses a consistent set of joints to describe each mechanism type. To validate our model, we created a large dataset of both open and closed coupler curves.

## Our Approach

Traditional methods of mechanism synthesis have their limitations, like slow optimization and dependence on initial conditions. Our approach leverages machine learning to overcome these challenges. By using a deep generative model, we can predict mechanism parameters quickly and accurately.

Our model processes mechanisms represented by Cartesian coordinates of joints, along with their coupler curve and mechanism type. This creates a latent vector that, combined with initial conditions, allows the decoder to recreate the original mechanism. Once trained, the model can generate diverse mechanisms tailored to specific coupler curves and types.

## Evaluation

To measure the effectiveness of our model, we use three metrics:

1. **Reconstruction Quality**: How well the predicted coupler curves match the input curves.
2. **Novelty**: How different the generated mechanisms are from each other.
3. **Diversity**: The range of different types of mechanisms generated.

We focused on three types of four-bar mechanisms for our dataset:

1. **RRRR Mechanisms**: All revolute joints.
2. **RRRP Mechanisms**: One prismatic joint (slider-crank).
3. **RRPR Mechanisms**: One prismatic joint (inverted slider-crank).

## Contributions

Here’s a quick rundown of our main contributions:

1. Developed a novel methodology using a c-beta-VAE with attention layers.
2. Created a unified representation for different types of four-bar mechanisms.
3. Compiled an extensive dataset of coupler curves.
4. Introduced three metrics for evaluating our model.

## Conclusion

This project is a step forward in generating diverse and novel four-bar mechanisms. By leveraging deep generative models, we can create multiple solutions quickly and efficiently, aiding in the early stages of machine design.

Thanks for stopping by! Feel free to reach out if you have any questions or just want to chat about cool engineering stuff.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/figure_4.png" title="our image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    This figure outlines our approach. During training, the model processes mechanisms alongside their coupler curves and types as conditions through an encoder, resulting in a latent vector. When combined with the original conditions, this vector enables the decoder to accurately reconstruct the original mechanism. Once trained, the model navigates the latent space to generate diverse mechanisms tailored to specific coupler curves and types. For instance, given a highlighted curve and various mechanism types, the model produces suitable mechanisms, as shown in the figure's output section.
</div>

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/figure_5.png" title="our image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Our Conditional beta-VAE model operates as follows: Initially, the input mechanism's type and coupler curve conditions are processed through a multi-layer perceptron (MLP) to standardize their representations, denoted as y_t and y_c, to equal sizes. These standardized representations are then merged into a combined condition vector y using a cross-attention block. Simultaneously, the input mechanism's joint locations are transformed into a larger encoded vector e via another MLP to align dimensions with y. Both vectors are fed into a cross-attention block acting as an encoder for the Variational Autoencoder, generating a latent representation vector z for the input. This latent representation is combined with y and passed through a sequence of self-attention blocks, facilitating the prediction of an output mechanism that closely matches the input. During inference, the model uses the trained conditional-beta-VAE to sample within the latent space, ensuring that output mechanisms adhere to specified criteria, including desired coupler paths and mechanism types.
</div>
