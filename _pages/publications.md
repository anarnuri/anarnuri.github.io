---
layout: page
permalink: /publications/
title: Publications
nav: true
nav_order: 2
---

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
