---
layout: page
title: Research
permalink: /research-projects/
description: Ph.D. research, datasets, and generative models.
nav: true
nav_order: 5
horizontal: false
---

Ph.D.-aligned **mechanism synthesis**, datasets, and generative models. **Hackathons**, early builds, and independent tools are on **[Personal projects]({{ '/personal-projects/' | relative_url }})**. Industry portfolio work is under **[Work]({{ '/projects/' | relative_url }})**.

<div class="projects">
{% if site.enable_project_categories %}
  {% assign categorized_projects = site.projects | where: 'category', 'Research' %}
  {% assign sorted_projects = categorized_projects | sort: 'importance' %}
  {% if page.horizontal %}
  <div class="container">
    <div class="row row-cols-1 row-cols-md-2">
    {% for project in sorted_projects %}
      {% include projects_horizontal.liquid %}
    {% endfor %}
    </div>
  </div>
  {% else %}
  <div class="row row-cols-1 row-cols-md-3">
    {% for project in sorted_projects %}
      {% include projects.liquid %}
    {% endfor %}
  </div>
  {% endif %}
{% endif %}
</div>
