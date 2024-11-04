---
layout: page
permalink: /publications/
title: Publications
nav: true
nav_order: 2
---

## My Publications

Welcome to my publications page! Here, you’ll find a selection of research articles and papers that I’ve authored, covering topics in Machine Learning, Mechanical Engineering, Robotics, and beyond. Each entry includes a link to the full text, if available, and a brief summary of the work.

### Journal Articles

<div class="publications">
  <ul>
    {% bibliography --query @Article %}
  </ul>
</div>

### Conference Papers

<div class="publications">
  <ul>
    {% bibliography --query @inproceedings %}
  </ul>
</div>
