"""
Phase 8: Image Metadata & Topic Indexing (Experimental)
Generates enhanced articles, image index, and topic index with HTML wrappers.
"""

import json
import os
import re
    'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
    'should', 'could', 'may', 'might', 'must', 'can', 'this', 'that',
    # UI/Common terms to ignore
    'image', 'picture', 'screenshot', 'display', 'displayed', 'showing', 'shows',
    'located', 'visible', 'click', 'button', 'icon', 'menu', 'select', 'enter',
    'type', 'field', 'tab', 'page', 'screen', 'window', 'left', 'right', 'top',
    'bottom', 'below', 'above', 'next', 'previous', 'user', 'interface', 'context',
    'panel', 'header', 'footer', 'sidebar', 'option', 'options', 'value', 'input',
    'text', 'box', 'list', 'item', 'link', 'url', 'http', 'https', 'www', 'com',
    'net', 'org', 'edu', 'gov', 'mil', 'int', 'info', 'biz', 'name', 'file',
    'folder', 'directory', 'path', 'drive', 'disk', 'data', 'database', 'table',
    'row', 'column', 'cell', 'record', 'entry', 'form', 'report', 'chart', 'graph',
    'plot', 'diagram', 'figure', 'map', 'plan', 'layout', 'structure', 'design',
    'style', 'format', 'color', 'size', 'width', 'height', 'length', 'weight',
    'position', 'location', 'area', 'region', 'zone', 'sector', 'part', 'portion',
    'segment', 'piece', 'bit', 'byte', 'kilobyte', 'megabyte', 'gigabyte', 'terabyte',
    'second', 'minute', 'hour', 'day', 'week', 'month', 'year', 'date', 'time',
    'now', 'then', 'when', 'where', 'why', 'how', 'what', 'who', 'whom', 'whose',
    'which', 'whichever', 'whatever', 'whenever', 'wherever', 'however', 'therefore',
    'thus', 'hence', 'so', 'because', 'since', 'as', 'if', 'unless', 'until', 'while',
    'although', 'though', 'even', 'just', 'only', 'also', 'too', 'very', 'much', 'many',
    'more', 'most', 'less', 'least', 'few', 'fewer', 'fewest', 'all', 'any', 'some',
    'none', 'no', 'yes', 'not', 'never', 'always', 'often', 'usually', 'sometimes',
    'rarely', 'seldom', 'perhaps', 'maybe', 'possibly', 'probably', 'likely', 'unlikely',
    'certainly', 'definitely', 'absolutely', 'really', 'truly', 'actually', 'fact',
    'truth', 'reality', 'world', 'life', 'death', 'birth', 'beginning', 'end', 'start',
    'stop', 'finish', 'complete', 'continue', 'pause', 'resume', 'restart', 'reset',
    'clear', 'delete', 'remove', 'add', 'create', 'make', 'build', 'construct', 'form',
    'shape', 'mold', 'cast', 'cut', 'paste', 'copy', 'move', 'go', 'come', 'stay',
    'leave', 'return', 'enter', 'exit', 'open', 'close', 'shut', 'lock', 'unlock',
    'block', 'unblock', 'allow', 'deny', 'permit', 'forbid', 'prohibit', 'ban',
    'restrict', 'limit', 'bound', 'confine', 'contain', 'include', 'exclude',
    'involve', 'consist', 'compose', 'comprise', 'constitute', 'represent', 'stand',
    'symbolize', 'signify', 'mean', 'indicate', 'suggest', 'imply', 'infer', 'deduce',
    'conclude', 'decide', 'determine', 'judge', 'assess', 'evaluate', 'estimate',
    'calculate', 'compute', 'measure', 'count', 'number', 'figure', 'digit', 'letter',
    'character', 'symbol', 'sign', 'mark', 'note', 'memo', 'record', 'log', 'journal',
    'diary', 'book', 'paper', 'document', 'file', 'folder', 'archive', 'library',
    'collection', 'set', 'group', 'batch', 'lot', 'bundle', 'pack', 'package', 'parcel',
    'box', 'case', 'crate', 'bin', 'bag', 'sack', 'container', 'vessel', 'holder',
    'carrier', 'transport', 'vehicle', 'car', 'truck', 'van', 'bus', 'train', 'plane',
    'ship', 'boat', 'bike', 'cycle', 'ride', 'drive', 'fly', 'sail', 'walk', 'run',
    'jog', 'hike', 'climb', 'swim', 'dive', 'jump', 'leap', 'hop', 'skip', 'dance',
    'sing', 'play', 'act', 'perform', 'work', 'labor', 'toil', 'job', 'task', 'duty',
    'role', 'function', 'purpose', 'goal', 'aim', 'target', 'objective', 'end',
    'result', 'outcome', 'effect', 'consequence', 'impact', 'influence', 'power',
    'force', 'energy', 'strength', 'might', 'ability', 'capacity', 'capability',
    'potential', 'possibility', 'opportunity', 'chance', 'luck', 'fortune', 'fate',
    'destiny', 'karma', 'kismet', 'doom', 'gloom', 'disaster', 'catastrophe',
    'tragedy', 'comedy', 'drama', 'story', 'tale', 'legend', 'myth', 'fable',
    'parable', 'allegory', 'metaphor', 'simile', 'analogy', 'comparison', 'contrast',
    'difference', 'similarity', 'likeness', 'resemblance', 'match', 'pair', 'couple',
    'twin', 'clone', 'copy', 'duplicate', 'replica', 'model', 'example', 'sample',
    'specimen', 'instance', 'case', 'illustration', 'demonstration', 'proof',
    'evidence', 'testimony', 'witness', 'judge', 'jury', 'trial', 'court', 'law',
    'rule', 'regulation', 'statute', 'ordinance', 'decree', 'order', 'command',
    'mandate', 'directive', 'instruction', 'direction', 'guide', 'guideline',
    'policy', 'procedure', 'process', 'method', 'technique', 'strategy', 'tactic',
    'plan', 'scheme', 'plot', 'conspiracy', 'secret', 'mystery', 'puzzle', 'riddle',
    'enigma', 'problem', 'issue', 'matter', 'affair', 'concern', 'worry', 'trouble',
    'difficulty', 'hardship', 'struggle', 'fight', 'battle', 'war', 'conflict',
    'clash', 'dispute', 'argument', 'debate', 'discussion', 'conversation', 'talk',
    'chat', 'speech', 'lecture', 'sermon', 'address', 'presentation', 'report',
    'statement', 'declaration', 'announcement', 'proclamation', 'message', 'note',
    'letter', 'email', 'memo', 'text', 'post', 'comment', 'review', 'feedback',
    'opinion', 'view', 'idea', 'thought', 'concept', 'notion', 'theory', 'hypothesis',
    'guess', 'hunch', 'feeling', 'emotion', 'sentiment', 'passion', 'desire', 'wish',
    'hope', 'dream', 'fantasy', 'imagination', 'creativity', 'innovation', 'invention',
    'discovery', 'exploration', 'adventure', 'journey', 'voyage', 'trip', 'tour',
    'travel', 'expedition', 'mission', 'quest', 'search', 'hunt', 'chase', 'pursuit'
}


def generate_html_wrapper(json_data, title="Data"):
    """Generate HTML wrapper for JSON data (matching production pattern)."""
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
</head>
<body>
    <pre>{json.dumps(json_data, indent=2)}</pre>
</body>
</html>"""


def load_image_captions():
    """Load image_captions.json."""
    if not IMAGE_CAPTIONS_FILE.exists():
        print(f"ERROR: {IMAGE_CAPTIONS_FILE} not found!")
        return None
    with open(IMAGE_CAPTIONS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_images_from_html(html_content, image_captions):
    """Extract images with descriptions from HTML (single-quoted attributes)."""
    if not html_content:
        return []
    
    # Unescape HTML entities (&lt; to <, etc.) since article bodies are HTML-escaped
    html_content = html.unescape(html_content)
    
    images = []
    position = 0
    
    # Updated pattern to match single-quoted HTML attributes
    img_pattern = re.compile(r"<img[^>]+src='([^']+)'[^>]*>", re.IGNORECASE)
    
    for match in img_pattern.finditer(html_content):
        position += 1
        url = match.group(1)
        description = image_captions.get(url, "")
        
        context_start = max(0, match.start() - 200)
        context_text = html_content[context_start:match.start()]
        context = extract_context(context_text)
        
        images.append({
            "url": url,
            "alt": description,
            "position": position,
            "context": context
        })
    
    return images


def extract_context(text_snippet):
    """Extract meaningful context from surrounding text."""
    text = re.sub(r'<[^>]+>', '', text_snippet).strip()
    
    step_match = re.search(r'(Step \d+[:\-\s]+[^<.]+)', text, re.IGNORECASE)
    if step_match:
        return step_match.group(1).strip()
    
    sentences = text.split('. ')
    if sentences:
        return sentences[-1].strip()[:100]
    return ""


def extract_keywords(text):
    """Extract keywords from text."""
    if not text:
        return []
    text = re.sub(r'<[^>]+>', '', text)
    # Only allow alphabetic characters for topics to avoid "10103021848723" etc.
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text)
    return words


def extract_topics(article_title, section_name, category_name, image_descriptions=None):
    """Generate topic keywords from high-value metadata only."""
    topics = set()
    
    # Priority 1: Article Title (High value)
    topics.update(extract_keywords(article_title))
    
    # Priority 2: Section & Category (Context)
    if section_name:
        topics.update(extract_keywords(section_name))
    if category_name:
        topics.update(extract_keywords(category_name))
        
    # NOTE: Intentionally NOT using image_descriptions for topics anymore
    # to avoid "bag of words" noise. Descriptions are still available
    # in the 'images' array for full-text search if needed.
    
    # Filter topics
    final_topics = set()
    for t in topics:
        t_lower = t.lower()
        if t_lower not in STOP_WORDS and not t.isdigit():
            final_topics.add(t_lower)
            
    return sorted(list(final_topics))


def load_section_and_category_mapping():
    """Load sections and categories for metadata."""
    sections_file = BASE_DIR / "sections.json"
    categories_file = BASE_DIR / "categories.json"
    
    section_map = {}
    category_map = {}
    
    if sections_file.exists():
            'url': enhanced_article['url'],
            'html_url': enhanced_article['html_url'],
            'image_count': len(images),
            'topics': topics[:10]
        })
        
        # Build image index
        for img in images:
            image_id = f"{article_id}_{img['position']}"
            image_index[image_id] = {
                'url': img['url'],
                'description': img['alt'],
                'article_id': article_id,
                'article_title': article.get('title', ''),
                'article_url': enhanced_article['url'],
                'article_html_url': enhanced_article['html_url'],
                'category': category_name,
                'section': section_name,
                'topics': topics,
                'position_in_article': img['position'],
                'context': img['context']
            }
    
    print(f"\nCompleted: {article_count} articles processed, {total_images} images indexed")
    return image_index, articles_list, EXPERIMENTAL_DIR


def build_topic_index(image_index):
    """Build topic-to-images reverse index using image IDs only."""
    topic_index = defaultdict(list)
    
    for image_id, metadata in image_index.items():
        for topic in metadata['topics']:
            topic_index[topic].append(image_id)
    
    return dict(sorted(topic_index.items()))


def save_with_html(data, filename, title):
    """Save JSON and HTML wrapper."""
    json_file = EXPERIMENTAL_DIR / f"{filename}.json"
    html_file = EXPERIMENTAL_DIR / f"{filename}.html"
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(generate_html_wrapper(data, title))
    
    size_kb = json_file.stat().st_size / 1024
    print(f"  {filename}.json: {size_kb:.1f} KB")
    print(f"  {filename}.html: Created")
    return json_file, html_file


def main():
    """Main execution flow."""
    print("=" * 60)
    print("Phase 8: Image Metadata & Topic Indexing (Experimental)")
    print("=" * 60)
    print()
    
    print("Loading image_captions.json...")
    image_captions = load_image_captions()
    if not image_captions:
        return
    print(f"  Loaded {len(image_captions)} image descriptions\n")
    
    print("Loading section and category mappings...")
    section_map, category_map = load_section_and_category_mapping()
    print(f"  Loaded {len(section_map)} sections, {len(category_map)} categories\n")
    
    image_index, articles_list, exp_articles_dir = process_articles(
        image_captions, section_map, category_map
    )
    
    if not image_index:
        print("ERROR: No images found")
        return
    print()
    
    print("Saving articles list...")
    save_with_html(articles_list, "articles", "Enhanced Articles List")
    print()
    
    print("Saving image index...")
    save_with_html(image_index, "image_index", "Image Index")
    print()
    
    print("Building and saving topic index...")
    topic_index = build_topic_index(image_index)
    print(f"  Generated {len(topic_index)} topics")
    save_with_html(topic_index, "topics_to_images", "Topic Index")
    print()
    
    print("=" * 60)
    print("EXPERIMENTAL INDEXING COMPLETE")
    print("=" * 60)
    print(f"Enhanced articles: {exp_articles_dir}")
    print(f"Indexes: {EXPERIMENTAL_DIR}")
    print()


if __name__ == "__main__":
    main()
