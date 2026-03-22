---
layout: page
title: Personal projects
permalink: /personal-projects/
description: Hackathons, early builds, and independent tools.
nav: true
nav_order: 6
horizontal: false
---

**Hackathons**, demos, and side projects. Ph.D.-aligned listings are on **[Research]({{ '/research-projects/' | relative_url }})**; industry portfolio items on **[Work]({{ '/projects/' | relative_url }})**.

<div class="projects">
{% if site.enable_project_categories %}
  {% assign categorized_projects = site.projects | where: 'category', 'Personal' %}
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
