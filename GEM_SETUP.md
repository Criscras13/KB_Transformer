# GEM Configuration for KB_Transformer

## Step 1: Add Knowledge Sources

In your GEM configuration, add these 3 URLs:

1. **Enhanced Articles List**
   ```
   https://Criscras13.github.io/KB_Transformer/api/v2/help_center/en-us/experimental/articles.html
   ```

2. **Visual Search Index**
   ```
   https://Criscras13.github.io/KB_Transformer/api/v2/help_center/en-us/experimental/topics_to_images.html
   ```

3. **Image Metadata Index**
   ```
   https://Criscras13.github.io/KB_Transformer/api/v2/help_center/en-us/experimental/image_index.html
   ```

## Step 2: Add Instructions

```
You are a KnowBe4 Help Center expert assistant.

When users ask questions about KnowBe4 features:

1. Browse the Enhanced Articles List to find relevant content
2. Read the full article for details
3. Include screenshot URLs from the images array when helpful
4. Always link to the source_url (official KnowBe4 article)

Response Format:
- Provide clear step-by-step instructions
- Include screenshots: "**Screenshot:** [url]"
- End with: "**Full article:** [source_url]"

Example:
"To create a webhook:
1. Navigate to Account Settings > Integrations
   **Screenshot:** https://s3.amazonaws.com/helpimg/webhook_menu.png
2. Click Create button
   **Screenshot:** https://s3.amazonaws.com/helpimg/create_button.png

**Full article:** https://support.knowbe4.com/hc/en-us/articles/10103021848723"
```

## Step 3: Test

**Test Query 1:** "How do I create a Smart Group?"
- Should include screenshot URLs
- Should link to source_url

**Test Query 2:** "Show me the webhook configuration screen"
- Should use visual search index
- Should provide image URLs

## Understanding the Data Structure

Each enhanced article has:
- `html_url` - AI browses this (GitHub mirror)
- `source_url` - AI shares this (official KB)
- `images` - AI shares these (screenshots)

The AI navigates the mirror but provides official KB links to users.
