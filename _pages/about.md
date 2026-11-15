---
layout: about
title: About
permalink: /

profile:
  align: right
  image: prof_pic.jpeg
  image_circular: false
  more_info: >
    <p>Robotics Engineer · Ph.D., Mechanical Engineering / CS</p>
    <p>+1 631 304 0554</p>
    <p>Las Vegas, NV</p>

news: false
selected_papers: true
social: true
---

Hi, I’m **Anar** — I started in **mechanical engineering** and now work at the intersection of **robotics and machine learning**. On the robotics side I focus on **simulation (Isaac Sim / Isaac Lab 3, Newton)**, **custom GPU physics in Warp** (e.g. a vacuum suction cup), **PhysX-style contact and deformables**, **VR teleop**, **ROS integration**, **reward shaping for RL policies (PPO) for arms and quadrupeds**, and **vision–language–action** models (**π0.5**, **GR00T**) trained on large synthetic datasets and run on real hardware. On the learning side I work with **generative models** (VAEs, transformers, MoE), **large-scale data and HPC (SLURM)**, and **on-device vision** (**CoreML**, **SwiftUI**). My Ph.D. at **Stony Brook** centered on **mechanism synthesis** and **multi-modal generative models** for design and path modeling.

Outside the core robotics lane, I’ve shipped **document Q&A / RAG-style** prototypes (Llama-class models, retrieval, AWS), competed in **hackathons** (e.g. transit / urban tooling), and earlier did **mechanical design and simulation** (wind, structures, CAD). The CV-style timeline is on **[Experience]({{ '/experience/' | relative_url }})**.

## Featured projects

<div class="projects">
  <div class="row row-cols-1 row-cols-md-2">
    {% assign featured_projects = site.projects | where: "featured", true | sort: "importance" %}
    {% for project in featured_projects %}
      {% include projects.liquid %}
    {% endfor %}
  </div>
</div>

For portfolio depth: **[Work]({{ '/projects/' | relative_url }})**, **[Research]({{ '/research-projects/' | relative_url }})**, **[Personal projects]({{ '/personal-projects/' | relative_url }})**, **[Publications]({{ '/publications/' | relative_url }})**, and **[Hugging Face](https://huggingface.co/anurizada)**. I’m glad you’re here—**email** or **LinkedIn** work best if you want to connect.
