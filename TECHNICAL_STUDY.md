# Comprehensive Technical Study: KB_Transformer Architecture

**Project:** KB_Transformer  
**Version:** 2.0 (Hybrid Architecture)  
**Date:** November 29, 2025  
**Repository:** [Criscras13/KB_Transformer](https://github.com/Criscras13/KB_Transformer)

---

## 1. Executive Summary

The **KB_Transformer** is a specialized middleware solution designed to bridge the gap between a human-centric Knowledge Base (KnowBe4 Support) and AI agents (Google Gemini). 

Standard RAG (Retrieval-Augmented Generation) approaches often fail to capture the *visual* context of support documentation—screenshots, diagrams, and UI elements—which are critical for technical support. Furthermore, AI agents often struggle to distinguish between "content to read" (for internal reasoning) and "content to share" (for the user).

This project solves these problems through a novel **Hybrid Architecture** that creates a dual-layer knowledge graph:
1.  **The AI Layer (Mirror):** A GitHub-hosted, machine-readable mirror containing enhanced JSON data, extracted image metadata, and semantic topic indexes.
2.  **The User Layer (Source):** A strict pointer system that ensures all user-facing links resolve to the official, trusted vendor documentation.

---

## 2. Problem Statement & Evolution

### The Challenge
*   **Visual Blindness:** Standard text scrapers ignore `<img>` tags, leaving the AI blind to the UI elements described in screenshots.
*   **Context Loss:** Flattening a KB into text files destroys the hierarchy (Categories -> Sections -> Articles).
*   **Hallucination Risk:** If an AI reads a mirrored HTML file, it often cites that mirror URL to the user, leading to "broken" or "unofficial" looking links.

### The Evolution of the Solution
This project evolved through rigorous testing across multiple iterations:

*   **Phase 1: Direct Mirroring:** We initially cloned the Zendesk API structure (`api/v2/help_center`). While this preserved structure, the AI struggled to navigate raw JSON efficiently.
*   **Phase 2: HTML Wrappers:** We discovered that some AI browsers prefer HTML over JSON. We wrapped JSON data in `<pre>` tags within HTML files to make them "clickable" and readable by the AI's browsing tools.
*   **Phase 3: Image Indexing (The "Visual" Breakthrough):** We realized the AI needed to "see." We built a regex-based extractor to pull every image URL, its `alt` text, and its surrounding textual context into a searchable `image_index.json`.
*   **Phase 4: The Hybrid URL Strategy (Current State):** The final breakthrough was decoupling the *reading* URL from the *sharing* URL. We modified the data structure to include both:
    *   `html_url`: The GitHub mirror (for AI analysis).
    *   `source_url`: The official KnowBe4 link (for user citation).

---

## 3. Technical Architecture

### 3.1 The Data Pipeline

The system operates on a two-stage Python pipeline:

#### Stage 1: Ingestion (`data_transformer.py`)
*   **Function:** Fetches raw data from the source (KnowBe4) or local cache.
*   **Transformation:** 
    *   Sanitizes HTML content.
    *   Preserves the original `html_url` as `source_url`.
    *   Rewrites internal links to point to the GitHub mirror (keeping the AI inside the "walled garden" while reading).
*   **Output:** Standard JSON files in `articles/`.

#### Stage 2: Enhancement (`build_experimental_indexes.py`)
This is the core innovation engine. It processes the standard articles to create the **Experimental Layer**.

*   **Image Extraction Engine:**
    *   Scans article HTML for `<img>` tags.
    *   Extracts `src` and `alt` attributes.
    *   **Context Windowing:** Captures the text immediately preceding the image (e.g., "Click the **Save** button as shown below:") to give the AI semantic understanding of the image's purpose.
*   **Topic Modeling:**
    *   Instead of generic TF-IDF, it uses a hierarchical keyword extraction strategy based on **Article Title > Section Name > Category Name**.
    *   This creates a high-signal `topics` array for every article.
*   **Output:** Enhanced JSON/HTML files in `experimental/articles/` and the master indexes.

### 3.2 The File Structure (API Mimicry)

The project mimics the Zendesk API v2 structure to ensure compatibility with tools expecting standard help center data, but hosts it statically on GitHub Pages.

```text
api/v2/help_center/en-us/
├── articles/                  # Standard JSON data (Base Layer)
└── experimental/              # The AI-Optimized Layer
    ├── articles/              # Enhanced Articles (JSON + HTML Wrappers)
    │   ├── 12345.json         # Contains 'images' array & 'source_url'
    │   └── 12345.html         # Browser-friendly wrapper
    ├── articles.html          # Master Article Index (The Entry Point)
    ├── image_index.html       # Master Image Database
    └── topics_to_images.html  # Visual Search Engine (Topic -> Images)
```

---

## 4. Key Technical Components

### 4.1 The Hybrid URL Data Model
Every enhanced article strictly adheres to this schema:

```json
{
  "id": 46512157558163,
  "title": "Integrate Workato into Your KSAT Console",
  "url": ".../experimental/articles/46512157558163.json",      // AI Read Path
  "html_url": ".../experimental/articles/46512157558163.html", // AI Navigation Path
  "source_url": "https://support.knowbe4.com/hc/...",          // User Citation Path
  "images": [
    {
      "url": "https://s3.amazonaws.com/helpimg/...",
      "alt": "Screenshot of Workato integration...",
      "context": "Navigate to the Account Settings tab..."
    }
  ]
}
```

### 4.2 The "Visual Search" Index (`topics_to_images.html`)
This file acts as a reverse index. Instead of searching for articles, the AI searches for *visual concepts*.
*   **Query:** "Show me the dashboard."
*   **Lookup:** The AI browses `topics_to_images.html`, finds the "dashboard" key, and retrieves a list of specific Image IDs.
*   **Retrieval:** It then hits `image_index.html` to get the full metadata for those images.

### 4.3 The GEM System Prompt
The architecture is useless without the correct instruction set. The `GEM_SETUP.md` prompt is engineered to leverage this specific structure:
*   **Workflow A (Text):** Forces the AI to read `html_url` but cite `source_url`.
*   **Workflow B (Visual):** Forces the AI to use the `topics_to_images` index to answer visual queries.

---

## 5. Conclusion & Future Roadmap

The **KB_Transformer** successfully demonstrates that a static, GitHub-hosted mirror can provide a superior RAG experience compared to direct web browsing or vector databases, specifically for **technical support** use cases where visual context and official citations are paramount.

**Future Considerations:**
*   **Automated Sync:** Implementing a GitHub Action to run the pipeline daily.
*   **Vector Embeddings:** Adding a `embeddings.json` layer for semantic search beyond keyword matching.
*   **Multi-Language Support:** Expanding the `en-us` structure to support localized KBs.

---
*Generated by Antigravity for Chris Glandon*
