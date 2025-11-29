# KB_Transformer: Final Architecture Overview

This document confirms the architectural strategy for the **KB_Transformer** project, specifically the "Two-URL Strategy" designed to enable AI agents to provide visual context while directing users to official documentation.

## 1. The Core Strategy: "Two-URL System"

We distinguish between where the AI **reads** information and where the AI **sends** the user.

| URL Type | Field Name | Target | Purpose |
| :--- | :--- | :--- | :--- |
| **Navigation URL** | `html_url` | **GitHub Mirror** | **For the AI.** Contains the enhanced content (image descriptions, metadata) that the AI needs to "see" the article. |
| **Sharing URL** | `source_url` | **Official KnowBe4** | **For the User.** The official link the AI provides in its final answer, ensuring users always land on the trusted support site. |

---

## 2. The AI Workflow

1.  **NAVIGATE (Internal):**
    *   The AI browses the **GitHub Mirror** (`html_url`) to find the right Category, Section, and Article.
    *   *Example:* `https://Criscras13.github.io/KB_Transformer/.../articles/115015198248.html`

2.  **READ & ANALYZE (Internal):**
    *   The AI reads the **Enhanced Article** on the mirror.
    *   It sees the text content AND the `images` array (screenshots with descriptions).

3.  **RESPOND (External):**
    *   The AI constructs an answer for the user.
    *   It includes **Screenshot URLs** from the `images` array.
    *   It provides the **Official Link** (`source_url`) for the full article.
    *   *Example:* `https://support.knowbe4.com/hc/en-us/articles/115015198248-Smart-Groups-Use-Cases`

---

## 3. Data Structure Reference

### Article JSON (`articles.json` & individual files)

```json
{
  "id": 115015198248,
  "title": "Smart Groups Use Cases",
  
  // 1. AI NAVIGATES HERE (Mirror)
  "html_url": "https://Criscras13.github.io/KB_Transformer/api/v2/help_center/en-us/articles/115015198248.html",
  
  // 2. AI SHARES THIS (Official)
  "source_url": "https://support.knowbe4.com/hc/en-us/articles/115015198248-Smart-Groups-Use-Cases",
  
  // 3. AI SHARES THESE (Images)
  "images": [
    {
      "url": "https://s3.amazonaws.com/helpimg/smart_groups.png",
      "alt": "Smart Groups Dashboard",
      "description": "Screenshot showing the Smart Groups overview panel..."
    }
  ],
  
  "body": "To create a smart group... <a href='https://support.knowbe4.com/...'>Click Here</a>" 
  // Internal links in body ALSO point to Official Site
}
```

### Organizational JSON (`categories.json`, `sections.json`)

These files exist solely to help the AI navigate the structure. They point to the **Mirror** so the AI stays within the enhanced environment while browsing.

```json
{
  "id": 360002919913,
  "name": "Security Awareness Training",
  "html_url": "https://Criscras13.github.io/KB_Transformer/api/v2/help_center/en-us/categories/360002919913.html"
}
```
