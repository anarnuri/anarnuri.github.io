---
layout: page
title: Mechformer. A Dual-Decoder Transformer with RMSNorm and SwiGLU for Mechanism Synthesis
importance: 1
category: Projects
related_publications: false
---

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/transformer.png" title="Overview of double-decoder Transformer Model" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Overview: The enhanced double-decoder Transformer model processes coupler curve images and mechanism type embeddings to generate diverse mechanism designs. The encoder captures spatial features, while the dual decoders predict joint coordinates, leveraging improved normalization, gating mechanisms, and robust attention modules.
</div>

[**Access the Full Code on GitHub**](https://github.com/anarnuri/path_generation_transformer)

## Overview

Designing mechanisms that accurately follow complex trajectories (coupler curves) remains a foundational challenge in mechanical design and robotics. Traditional synthesis methods rely on solving analytical equations, which are:

1. **Computationally Intensive**: Especially for higher-order mechanisms with many joints.
2. **Single-Result Oriented**: Typically offering just one valid mechanism per coupler curve.
3. **Limited Flexibility**: Struggle to generalize to mechanisms with complex or novel configurations.

### Motivation for a Machine Learning Approach

This project introduces a **Dual-Decoder Transformer** model that reimagines the synthesis pipeline. By leveraging deep learning, we can automate the generation of diverse and complex mechanisms, speeding up design iterations and broadening the search space. Key features of the model include:

- **Coupler Curves as Images**: Trajectories are input as grayscale images, allowing the encoder to extract spatial features effectively.
- **Mechanism Type Conditioning**: Each mechanism type is embedded into a feature vector, enabling the model to tailor its outputs accordingly.
- **Coordinate Prediction**: Mechanisms are represented by Cartesian coordinates of joints, split into two independently predicted parts for clarity and control.

This model treats the mechanism as a sequence of tokens, where each token represents a joint in the mechanism. This tokenization approach allows the model to easily scale to mechanisms with a higher number of joints. Currently, the model can handle up to 20 joints, and its architecture is designed to accommodate even larger mechanisms by adjusting token length and model capacity. The modularity of the design, with independent decoders for each set of joint coordinates, further enhances scalability. As the number of joints increases, the model’s performance remains consistent, making it suitable for mechanisms of varying complexity without significant modifications. This scalability makes it a flexible solution for future applications that may involve more intricate mechanism designs.

## Key Enhancements

1. **RMSNorm for Stability**:
   - The model replaces standard LayerNorm with **RMSNorm**, which normalizes inputs based on their root mean square. This improves training stability and convergence speed.

2. **SwiGLU-inspired FeedForwardBlock**:
   - The feedforward block incorporates a **Swish-Gated Linear Unit (SwiGLU)** style mechanism: two parallel linear projections, where one is passed through a SiLU (swish) activation and multiplied element-wise with the other. This gating mechanism boosts expressiveness and non-linearity.

3. **Modular Attention Mechanism**:
   - The attention layers now include **dynamic masking** capabilities, ensuring flexible handling of variable-length sequences and proper autoregressive decoding when needed.

4. **Mixture of Experts (MoE) Integration**:

   - A MoE layer is included within the Transformer blocks to dynamically route information through multiple expert networks. This enables the model to specialize different parts of the network for various mechanism types and complexities, improving both flexibility and performance.

5. **Enhanced Input Processing**:
   - **Input Embeddings**: Raw coupler curve images are patch-embedded using a linear projection and scaled by the square root of the model’s dimensionality.
   - **Positional Encoding**: Sinusoidal positional encodings are precomputed and added to the embeddings, preserving sequence order.

6. **Better Initialization**:
   - All linear layers are initialized with **Xavier uniform initialization**, promoting stable gradient flow from the start of training.

7. **Clean Modular Design**:
   - Each component (embeddings, encoder, decoders, attention, normalization) is implemented as a separate, reusable module for ease of experimentation and future extension.

## Iterative Development Process

### Early Exploration

We began with a single-decoder Transformer adapted from NLP, but it quickly hit limitations:

- **Inadequate Generalization**: Struggled with mechanisms involving more than six joints.
- **Scalability Issues**: Larger models led to overfitting and diminishing returns.

### Key Architectural Shifts

- **RMSNorm Integration**: Replacing LayerNorm enhanced training consistency and reduced sensitivity to learning rate schedules.
- **Dual-Decoders**: Splitting predictions into two decoders provided modularity and improved performance on complex mechanism synthesis tasks.
- **Gated Feedforward Blocks**: Introducing SwiGLU-like structures allowed the model to model intricate joint relationships more effectively.

## Methodology

### Input

1. **Coupler Curve Images**:
   - Converted to patches and embedded using a linear layer.
2. **Mechanism Type Embeddings**:
   - Learned embeddings added to each patch sequence to condition the model.

### Model

- **Encoder**:
  - Processes combined embeddings, capturing spatial and contextual information.
- **Dual Decoders**:
  - Independently predict the two halves of the joint coordinate set, each with cross-attention to the encoder’s output.
- **Projection Layers**:
  - Map decoder outputs to 2D Cartesian coordinates.

### Training

- **Loss Function**:  
  Masked MSE loss handles padding efficiently:

   ```python
   def mse_loss(predictions, targets, mask_value=0.5):
       mask = ~(targets == mask_value).all(dim=-1)
       mask = mask.unsqueeze(-1).expand_as(predictions)
       masked_predictions = predictions[mask]
       masked_targets = targets[mask]
       loss = F.mse_loss(masked_predictions, masked_targets, reduction="mean")
       return loss
   ```

2. **Optimization**:

   - The model is trained using the Adam optimizer with a learning rate scheduler.

3. **Dynamic Causal Masking**:
   - Applied during decoding to ensure stepwise predictions.

---

## Inference Process

During inference, the model generates mechanism designs using a conditional greedy decoding approach:

1. **Encoding**:

   - The coupler curve image is encoded along with the mechanism type embedding.

2. **Decoding**:

   - Each decoder independently predicts its part of the mechanism, conditioned on the encoder's representation.

3. **Stopping Condition**:
   - Decoding halts when an End-of-Sequence (EOS) token is detected.

### Code Highlights for Inference

```python
def greedy_decode_conditional(model, source, mech_type, max_len, eos_token=torch.tensor([1.0, 1.0])):
    encoder_output = model.encode(source, None, mech_type)
    decoder_input_first = torch.zeros(1, 1, 2).to(device)
    decoder_input_second = torch.zeros(1, 1, 2).to(device)

    # Decoding for both decoders
    while decoder_input_first.size(1) < max_len // 2:
        ...
    while decoder_input_second.size(1) < max_len // 2:
        ...
```

---

## Applications

1. **Robotics**:

   - Generates diverse designs for robotic mechanisms, such as arms and grippers.

2. **Industrial Design**:

   - Facilitates rapid prototyping of mechanisms for manufacturing.

3. **Education**:
   - Provides a framework for teaching mechanism synthesis concepts using advanced machine learning techniques.

---

## Future Directions

1. **Intra-Type Diversity**:

   - Extend the model to generate multiple mechanisms within the same type.

2. **Optimization Frameworks**:

   - Integrate the model with optimization algorithms for real-time design applications.

3. **Explainability**:
   - Develop visualizations to interpret the model’s attention mechanisms and latent space.
