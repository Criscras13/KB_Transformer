# KB_Transformer

KnowBe4 Help Center API with AI-enhanced image enrichment for internal use.

## Purpose

Enable AI agents to:
1. Browse enhanced articles with image URLs
2. Share official KnowBe4 article links with users
3. Provide clickable screenshot links

## Example GEM Response

> To create a webhook:
> 
> 1. Go to Account Settings > Integrations
>    **Screenshot:** https://s3.amazonaws.com/helpimg/webhook_menu.png
> 
> 2. Click "Create" button
>    **Screenshot:** https://s3.amazonaws.com/helpimg/create_button.png
> 
> **Full article:** https://support.knowbe4.com/hc/en-us/articles/10103021848723

---

## API Structure

### Standard Endpoints
- Categories: `/api/v2/help_center/en-us/categories.html`
- Sections: `/api/v2/help_center/en-us/sections.html`
- Articles: `/api/v2/help_center/en-us/articles.html`

### Enhanced Endpoints (For GEM)
- Enhanced Articles: `/api/v2/help_center/en-us/experimental/articles.html`
- Visual Search: `/api/v2/help_center/en-us/experimental/topics_to_images.html`
- Image Index: `/api/v2/help_center/en-us/experimental/image_index.html`

---

## Article Structure

Each enhanced article contains:

```json
{
  "id": 123,
  "title": "How to Create Webhooks",
  "html_url": "https://Criscras13.github.io/KB_Transformer/.../123.html",
  "source_url": "https://support.knowbe4.com/hc/en-us/articles/123-How-to-Create-Webhooks",
  "images": [
    {
      "url": "https://s3.amazonaws.com/helpimg/webhook.png",
      "alt": "AI description of screenshot",
      "position": 1
    }
  ]
}
```

- **html_url** - AI browses this (GitHub mirror with images)
- **source_url** - AI shares this (official KnowBe4 article)
```bash
update-data.bat
```

**Linux/Mac:**
```bash
./update-data.sh
```

**What it does:**
1. Fetches categories, sections, articles from KnowBe4 API
2. Adds source_url to all 1,004 articles
3. Builds experimental indexes with image enrichment

**Then deploy:**
```bash
git add .
git commit -m "Update data"
git push origin main
```

---

## Statistics

- **Articles:** 1,004 (all with source_url + images)
- **Images:** 3,519 AI-described screenshots
- **Topics:** 640 searchable keywords
- **Size:** ~86 MB

---

## Project Structure

```
KB_Transformer/
├── data_transformer.py              # Adds source_url field
├── build_experimental_indexes.py    # Builds enhanced indexes
├── image_captions.json              # AI descriptions cache
├── site_src/
│   └── static/api/v2/help_center/en-us/
│       ├── categories/              # Standard (nav only)
│       ├── sections/                # Standard (nav only)
│       ├── articles/                # Standard (with source_url)
│       └── experimental/            # Enhanced (with images)
```

---

## Related Projects

- **Project 1:** [API_testing](https://github.com/Criscras13/API_testing) (Foundation)
- **Project 2:** [API_image_testing](https://github.com/Criscras13/API_image_testing) (Enhancement)
