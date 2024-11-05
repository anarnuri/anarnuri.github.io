---
layout: page
title: Carpooling App for Rush Hour - Hackathon Project
importance: 1
category: work
related_publications: false
---

## Carpooling App for Rush Hour - Hackathon Winner 🏆

This project was developed for [Transit Hackathon](https://transithack.az/) held in Baku, Azerbaijan. We were thrilled to win the hackathon with our innovative approach to tackling congestion in public transport during rush hours!

### Project Overview

Our idea was to create a **carpooling app** aimed at connecting people during peak hours. The app would allow users to order a single taxi that would take passengers to destinations close to one another. This project was inspired by the overcrowding in Baku’s public transportation system during rush hours, as well as a local practice where people manually arrange carpools without an app. Our app aims to make this process more efficient, accessible, and convenient.

### Key Innovation: The Routing Algorithm

The core of our project was a custom algorithm designed to generate optimized routes for taxis. Here’s how it works:

1. **Collect Destinations**: The algorithm begins by gathering the destinations of all users looking to carpool.
2. **Calculate Distances**: It then calculates the distances between each pair of destinations.
3. **Cluster Locations**: Based on these distances, the algorithm identifies neighboring locations and groups them into clusters.
4. **Generate Routes**: Each cluster then serves as a predefined route for a taxi, ensuring that the taxi route is optimized for destinations close to each other, reducing travel time and improving efficiency.

### Web-Based Visualization

To demonstrate our solution, we implemented a **web-based visualization** accessible [here](https://urbanhack-production.up.railway.app/). This visualization allows users to see the routing algorithm in action. We chose specific destinations for the demo to avoid continuously recalculating distances between random points, as this would consume our limited Google API tokens used for distance calculations.

### Why This Approach?

Our solution addresses a real need in Azerbaijan, where informal carpooling is already popular but lacks structure and technology. By formalizing and digitizing this process, our app could significantly reduce congestion in subways and public transport during peak hours.

### Hackathon Outcome

Thanks to our unique algorithm and clear understanding of local needs, we were awarded **first place** in the hackathon! 🎉

### Additional Resources

#### Presentation (PPTX)

You can download our project presentation [here](assets/presentations/hackathon-presentation.pptx).

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include video.liquid path="assets/video/hackathon-demo.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=true %}
    </div>
</div>
<div class="caption">
    A demo video showcasing the app's functionality and algorithm.
</div>

This project was an exciting blend of problem-solving, creativity, and teamwork, and winning the hackathon was a fantastic validation of our efforts. We’re excited to see how this idea could be developed further to improve urban transportation in Azerbaijan!
