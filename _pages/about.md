---
layout: about
title: About
permalink: /

profile:
  align: right
  image: prof_pic.jpeg
  image_circular: false
  more_info: >
    <p>PhD Candidate, Generative AI</p>
    <p>+1 631 304 0554</p>
    <p>Brooklyn, NY 11230</p>

news: false
selected_papers: true
social: true
---

# About Me

Hi, I’m **Anar** — a mechanical engineer turned machine learning researcher working at the intersection of **robotics** and **generative AI**.  

I am pursuing my **Ph.D. at Stony Brook University**, where I design multi-modal generative models for mechanical design, and I work as a **Robotics Engineer at DL-RL**, where I bring these ideas to life on real robotic systems. My focus is building **end-to-end AI solutions** that move seamlessly from simulation and theory into deployment on robotic hardware.

At [DL-RL](https://anarnuri.github.io/projects/12_project/), I:  
- Generate **large-scale synthetic datasets** in Isaac Sim for the SO100 robotic arm, using inverse kinematics to create diverse training data. Published datasets on [Hugging Face](https://huggingface.co/anurizada).  
- Fine-tune **Gr00t-based control models** on both simulated and real-world data, deploying directly to the physical SO100 arm.  
- Run **closed-loop robotic experiments**, achieving **90–95% success rates** on pick and pick-and-place tasks, far exceeding baseline performance.  

---

### 🔬 Current Focus

My Ph.D. research explores **multi-modal generative models** for mechanism design — blending deep learning with classical kinematics. I develop neural architectures that synthesize mechanisms from scratch, combining domain-specific knowledge with modern generative AI.

Some highlights of my research include:  
- **🧠 Dual-Decoder Transformer** for [mechanism synthesis](https://anarnuri.github.io/projects/9_project/), generating coupler curves and predicting joint coordinates with high accuracy.  
- **📱 Mobile AI App** for [real-time object detection](https://anarnuri.github.io/projects/10_project/), deploying YOLOv8 on iPhone with automated robotic dataset generation (achieving 99.84% accuracy).  
- **📄 Document RAG API** powered by [Llama-3-70B](https://anarnuri.github.io/projects/11_project/), enabling fast, private document-based Q&A.  

---

### 🛠️ What I Build

My work blends **algorithm design** with **system engineering**, optimized for both research and deployment:  

- Custom neural architectures: transformers, VAEs, diffusion models  
- High-performance training on HPC clusters and distributed GPUs  
- Robotics pipelines spanning **simulation → training → deployment**  
- Edge-ready deployment on iOS, embedded systems, and robotic platforms  

Technologies I’ve engineered include:  
- A **Transformer model** with a LLaMa2-style encoder and decoder
- A **conditional β-VAE** with Classifier-Free Guidance for controllable generation  
- A **graph-VAE** for encoding structural relationships in mechanical linkages  
- An **image-based VAE** + MLP pipeline to connect visual and geometric design  
- Fine-tuned **Latent Diffusion Models** with **LoRA** and **quantization**  
- A **GNN-based tokenizer** that transforms structured data into LLM-ready input  

Many of these models are optimized for real-time inference and integrated into platforms like [MotionGen](https://motiongen.io).

---

### 🏢 Past Experience: Zortag

As a **Machine Learning Engineer at Zortag**, I worked on applied computer vision and edge AI systems, focusing on real-time performance and deployment:  

- Fine-tuned **YOLOv8** models, boosting detection accuracy from ~90% to nearly **100%** while reducing inference to milliseconds by streamlining a two-step pipeline into a single-step approach.  
- Automated the **myCobot 280 PI** robotic arm for dataset generation, reducing manual workload by 60% and tripling labeling speed through a custom data capture pipeline with automated AWS S3 integration.  
- Developed an **iPhone-based real-time QR detection system** using SwiftUI + CoreML, containerized via Docker for scalable iOS deployment.  

This role sharpened my expertise in **real-time computer vision, robotics-driven data pipelines, and mobile AI deployment**.

---

### 📚 More

Beyond robotics and design models, I also develop tools for **intelligent information systems**. One example is a **production-ready Retrieval-Augmented Generation (RAG) API** that turns document sets into responsive knowledge bases, built with:  

- **Llama-3-70B** for advanced QA  
- **FAISS** vector search + M2-BERT embeddings  
- **AWS serverless infrastructure** for scalable, secure deployment  

This system answers queries in under **1.2 seconds**, with strong data privacy guarantees, and is freely accessible for academic or personal use.  

---

Feel free to explore my [website](https://anarnuri.github.io) and [Hugging Face](https://huggingface.co/anurizada) to dive deeper into my work. Whether you're a fellow researcher, a potential collaborator, or just curious, I’m glad you’re here!
