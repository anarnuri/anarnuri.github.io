---
layout: page
title: Interactive Digital Transformation and Simulation of n-Bar Planar Linkages using Deep Neural Networks
importance: 1
category: Projects
related_publications: false
---

## Interactive Digital Transformation and Simulation of $n$-Bar Planar Linkages using Deep Neural Networks

This paper introduces a new method using deep neural networks for the interactive digital transformation and simulation of $n$-bar planar linkages, which consist of revolute and prismatic joints, based on hand-drawn sketches. Instead of relying solely on computer vision, our approach combines topological knowledge of linkage mechanisms with the outcomes of a convolutional deep neural network. This creates a framework for recognizing hand-drawn sketches.

We generate a dataset of synthetic images that resemble hand-drawn sketches of linkage mechanisms. Next, we fine-tune a state-of-the-art deep neural network to detect discrete objects using building blocks that represent joints and links in various positions, sizes, and orientations within these sketches. We then conduct a topological analysis on the detected objects to construct a kinematic model of the sketched mechanisms. The results demonstrate the effectiveness of our algorithm in handling hand-drawn sketches and converting them into digital representations. This has practical implications for improving communication, analysis, organization, and classification of planar mechanisms.

### Introduction

During the product design process, sketching plays a pivotal role in effectively conveying and visualizing ideas. Within engineering design teams, designers frequently create kinematic sketches of mechanisms to aid in the brainstorming process. The automated detection of critical components in linkage mechanisms, including pivot type and location, link dimensions, and interconnection patterns, has the potential to facilitate various tasks such as transferring a mechanism from a sketch to computer simulation software, digitally cataloging and classifying existing designs, and generating similar mechanisms for concept development.

This paper introduces a framework for the automated and real-time digital conversion of hand-drawn sketches depicting planar linkage mechanisms. The approach involves training a specialized deep Convolutional Neural Network (CNN) using a synthetic database of linkage sketches. The trained CNN exhibits the capability to detect multiple objects within an image, providing bounding boxes and class probabilities for each detected object. These bounding boxes are subsequently adaptively resized in preparation for the subsequent topology analysis phase, which determines joint and link types, connections, link dimensions, and pivot locations. The final output is presented in the form of an adjacency matrix, as well as tables detailing links and joints.

### Synthetic Image Generation of Sketches

Training a CNN-based object detector requires a large number of input images, which in our case would be a dataset of hand-drawn planar linkage sketches. Unfortunately, there are no such datasets available. One way of generating a dataset would be extracting images of mechanisms from textbooks, patents, and the internet or asking people to sketch bar mechanisms and upload them; however, this method would be very time-consuming and not yield enough training images needed to retrain an object detector. Thus, we introduce an automated method for generating images of $n$-bar linkages by writing a script, which uses Scribble library for simulating hand-drawn shapes. Using our script, we generated 18,000 training, 2,000 validation, and 6,500 testing images in less than an hour. Our script provides annotation automatically as well.

The training dataset consisted of black and white images depicting different parts of bar linkages, such as fixed and free revolute joints, links, and prismatic joints, some of which are connected. This work assumes that since most people use a pencil and a white paper to draw sketches, there is no need to train the detector on colored images. However, real-life images of sketches might be colored and backgrounds might not be perfectly white. To ensure our model performs well in those cases, we made additional testing datasets: with colored backgrounds, with colored strokes on a white background, a mix of colored backgrounds and strokes, and different stroke thicknesses. The results showed that the color of a sketch and thickness levels of 1 to 3 do not make any difference; however, thickness of 4 and higher decreases the detection accuracy.

The dataset must cover as many ways of drawing a planar $n$-bar linkage as possible; i.e., different locations of fixed and free joints, their orientation, type, quantity, etc. The dataset is accessible via the following link: [Kaggle Dataset](https://www.kaggle.com/datasets/anarnurizada/n-bar-mechanisms).

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/figure_1.jpg" title="our image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Overview: A CNN Object Detector is trained with a set of synthetic hand-drawn sketches of mechanisms, which are not required to be valid mechanisms. During testing, users input a sketch of a bar linkage (one of the test mechanism sketches). The CNN outputs bounding boxes and labels around detected objects. The output bounding boxes are resized  and  connections between the joints and links are determined. If there are any prismatic joints present, we find links along which sliders move. Using the information about the location of joints and their connections with links, the linkage geometry is determined and presented in joint-link tables and adjacency matrix.
</div>

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/figure_2.jpg" title="everyone image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Top row left to right: colored stroke on white background, colored background with black stroke, mix of colored background and stroke, black and white sketch with stroke 6. Bottom row left to right: stroke thickness 1, 3, 4, 5.
</div>
