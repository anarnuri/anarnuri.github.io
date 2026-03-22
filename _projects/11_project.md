---
layout: page
title: Browser document Q&A (Llama-3 + RAG)
importance: 1
category: Personal
related_publications: false
---

I built a **browser-based document assistant** to see how far I could push **private, session-local Q&A** over PDFs and text: chunking, embeddings, vector retrieval, and a **Llama-3–class** model for answers—without sending document content to a third-party app beyond the inference API I chose for the experiment.

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include video_if_exists.liquid path="assets/video/web_demo.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=false preload="auto" %}
    </div>
</div>
<div class="caption">
    Screen capture of the prototype: upload, question, and grounded-style answers over in-session documents.
</div>

**What I shipped**

- **Ingestion pipeline** — PDF/text handling with cleanup and chunking suitable for retrieval (LangChain-style orchestration, PyPDF, custom normalization).
- **Retrieval stack** — **M2-BERT** embeddings with **FAISS** for search over chunks; prompt assembly so the LLM works from retrieved context.
- **Reasoning layer** — **Llama-3-70B** via **Together AI** for answer generation in early iterations.
- **Hosting** — **AWS** serverless-style deployment with scaling in mind for bursty use.

**What I learned**

- End-to-end RAG is less about the headline model and more about **chunk boundaries**, **embedding quality**, and **failure modes** when retrieval misses.
- Keeping **sessions scoped** and **documents client/session-bound** is doable, but latency and cost trade-offs are real at moderate scale.

This was a **personal build** for practice and portfolio; it is not a product launch. A public demo URL may follow if I revisit hosting and terms of use.
