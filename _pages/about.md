---
layout: about
title: About
permalink: /

profile:
  align: right
  image: prof_pic.jpeg
  image_circular: false # crops the image to make it circular
  more_info: >
    <p> PhD Candidate, Generative AI</p> 
    <p>+1 631 304 0554</p>
    <p>Brooklyn, NY 11230</p>

news: false # includes a list of news items
selected_papers: true # includes a list of papers marked as "selected={true}"
social: true # includes social icons at the bottom of the page
---

I'm **Anar**, a mechanical engineer turned machine learning researcher building AI systems that bridge digital and physical worlds. At Stony Brook University and Zortag, I create full-stack solutions that combine cutting-edge algorithms with real-world deployment:

- **🤖 Generative AI Design**: Developed a [Dual-Decoder Transformer](https://anarnuri.github.io/projects/9_project) that automates mechanism synthesis
- **📱 Mobile AI**: Built an [iPhone app](https://anarnuri.github.io/projects/10_project) with real-time YOLOv8 inference + robotic dataset automation (99.84% accuracy)
- **🔍 Document Intelligence**: Launched a [free RAG API](https://anarnuri.github.io/projects/11_project) using Llama-3-70B for instant document QA

My Ph.D. research focuses on **multi-modal generative models** for mechanical engineering. I specialize in taking projects from concept to production—whether that means:

- Architecting novel neural networks (transformers, VAEs, diffusion models)
- Optimizing training on HPC clusters
- Deploying to mobile/edge devices

Some of the models I’ve developed and deployed include a **transformer-based architecture** with a LLaMa2-inspired encoder and **diffusion-based decoder** for precise mechanism synthesis, a **conditional β-VAE** with Classifier-Free Guidance for controllable generation, a **graph-VAE** for representing structural relationships, and an **image-based VAE** paired with an MLP to bridge visual and geometric design spaces. I’ve also fine-tuned **Latent Diffusion Models** using **LoRA** and **quantization**, incorporating a **GNN-based tokenizer** to encode structured data for direct LLM input.

All of these models are optimized for real-time inference and some are deployed on [MotionGen](https://motiongen.io). This full-stack, hands-on approach reflects my engineering mindset: rigorous, resourceful, and deeply committed to building practical and reliable AI systems from the ground up.

One of my most significant contributions is the development of a **Dual-Decoder Transformer Model** for mechanism synthesis. This model processes coupler curve images and mechanism type embeddings to generate diverse and accurate designs. By leveraging two independent decoders, it efficiently predicts joint coordinates, making it a breakthrough in path synthesis for complex mechanisms.

To accelerate model training, I use **PyTorch Distributed Training** and **High-Performance Computing (HPC)** resources, enabling efficient training of large-scale generative architectures.

In addition to my research, I've created a **production-ready RAG API** that transforms document collections into queryable knowledge bases. This system combines:

- **Llama-3-70B** for intelligent question answering
- **FAISS vector search** with M2-BERT embeddings
- **AWS serverless infrastructure** for scalable deployment

The API delivers accurate, context-aware answers in **under 1.2 seconds** while maintaining strict data privacy - all available through a free tier for personal and academic use.

In addition to my research, I work as a **Machine Learning Engineer at Zortag**, where I program and automate the **myCobot 280 PI** robotic arm for dataset generation, simulating human-like motion to reduce manual effort. I’ve also fine-tuned object detection models like **YOLOv8**, improving accuracy and speeding up the data labeling pipeline. Recently, I **developed an iPhone app** that deploys my trained models for near real-time inference. This significantly improves practical deployment by enabling **instant QR code verification** and **real-time object detection** on mobile devices.

Feel free to explore my [website](https://anarnuri.github.io) to learn more about my projects and experiences. Whether you're here out of curiosity or looking to connect, I’m excited to share my journey with you!
