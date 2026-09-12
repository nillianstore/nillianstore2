import os
import json
import random
import requests
import frontmatter
from datetime import datetime
from pathlib import Path
import re

# Configuration
SHOP_DIR = Path("./shop")
POSTS_DIR = Path("./posts")
BLOG_LOG_FILE = Path("./blog_log.json")

# API Credentials
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def load_blog_history():
    if BLOG_LOG_FILE.exists():
        with open(BLOG_LOG_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_blog_history(product_id):
    history = load_blog_history()
    history.append(product_id)
    with open(BLOG_LOG_FILE, "w") as f:
        json.dump(history, f)

def get_random_product():
    products = list(SHOP_DIR.glob("*.md"))
    # Products already covered by an existing blog post (image or amazon link reference).
    # File-based check (not just blog_log.json) so the bot never re-blogs a covered product.
    posted = set()
    for pf in POSTS_DIR.glob("*.md"):
        posted.update(re.findall(r'(?:img/|amazon\.ae/dp/)(B0[A-Z0-9]{8})', pf.read_text(encoding="utf-8")))
    available = [p for p in products if p.stem not in posted]
    if not available:
        return None
    return random.choice(available)

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = text.strip('-')
    return text

def generate_blog_content(product_data):
    prompt = f"""
    You are an expert SEO copywriter for 'Nillian Store', a boutique shop in the UAE.
    
    Product Title: {product_data['title']}
    Product Description: {product_data['description']}
    Price: {product_data['price']}
    Amazon Link: {product_data['link']}
    
    Task: Create a high-quality, SEO-optimized blog post focusing on this product.
    
    Requirements:
    1. Catchy Title: Include emojis and UAE context (e.g., Dubai, Abu Dhabi, 2025).
    2. Meta Description: A compelling summary for search engines.
    3. Tags: 10-15 relevant SEO tags (UAE home decor, gift ideas, etc.).
    4. Content: 
       - Introduction about UAE lifestyle/home decor trends.
       - A detailed section about the product.
       - Use bold text for emphasis.
       - Include a "Why It Works" section with bullet points.
       - Include a "Perfect for" section.
       - A final thought/conclusion.
    
    Format the output as JSON:
    {{
        "title": "...",
        "description": "...",
        "tags": ["tag1", "tag2", ...],
        "intro": "...",
        "product_section": "...",
        "why_it_works": ["point1", "point2", ...],
        "perfect_for": "...",
        "conclusion": "..."
    }}
    """
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }
    
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    response.raise_for_status()
    return json.loads(response.json()["choices"][0]["message"]["content"])

def create_blog_file(product_data, ai_content):
    slug = slugify(ai_content['title'])
    date_str = datetime.now().strftime("%Y-%m-%d")
    file_name = f"{slug}.md"
    file_path = POSTS_DIR / file_name
    
    # Ensure tags include 'post' for Eleventy and sanitize tags
    import html as _html
    def _sanitize_tag(t):
        if not t:
            return ''
        t = _html.unescape(str(t))
        t = t.replace('’', "'").replace('`', "'")
        # Remove problematic filename characters and slashes/backslashes
        t = re.sub(r'[#\?\/\\]', '', t)
        t = t.strip()
        return t

    tags = ai_content.get('tags', []) or []
    tags = [_sanitize_tag(t) for t in tags]
    # Filter empties and limit to a reasonable number for frontmatter
    tags = [t for t in tags if t][:15]
    if 'post' not in tags:
        tags.append('post')
    
    # Construct the Amazon Button HTML - Wrapped in centered container
    amazon_button = f"""
<div style="text-align: center; margin: 1.5rem 0;">
  <a
    href="{product_data['link']}"
    target="_blank"
    rel="noopener"
    class="btn btn-lg px-4"
    style="background: #ff9900; color: #000; border: none; font-weight: 600; text-decoration: none; display: inline-block;">
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-cart me-2" viewBox="0 0 16 16">
      <path d="M0 1.5A.5.5 0 0 1 .5 1H2a.5.5 0 0 1 .485.379L2.89 3H15.5a.5.5 0 0 1 .491.592l-1.5 8A.5.5 0 0 1 13.991 12H4.5a.5.5 0 0 1-.491-.408L3.1 6.379 1.485 1.5H.5a.5.5 0 0 1-.5-.5z"/>
      <path d="M4 14a2 2 0 0 0 2 2h5a2 2 0 0 0 2-2V5H4v9z"/>
    </svg>
    Buy on Amazon.ae
  </a>
</div>
"""

    # Handle multiple images (up to 3)
    image_html_list = []
    for i, img_path in enumerate(product_data['images'][:3]):
        image_html_list.append(f"""
<div style="text-align:center; margin: 1.5rem 0;">
  <img src="{img_path}" alt="{product_data['title']} - Image {i+1}" style="max-width:100%; height:auto; border-radius:8px; box-shadow:0 4px 12px rgba(0,0,0,0.08);">
</div>
""")

    # Sanitize frontmatter title/description
    safe_title = ai_content.get('title', '').replace('"', '\\"').replace('\n', ' ').strip()
    safe_description = ai_content.get('description', '').replace('"', '\\"').replace('\n', ' ').strip()
    
    # Sanitize tags for frontmatter
    safe_tags_list = []
    for tag in tags:
        safe_tag = tag.replace('"', '\\"')
        safe_tags_list.append(f'  - "{safe_tag}"')
    safe_tags_str = "\n".join(safe_tags_list)

    # Construct the Markdown content
    content = f"""---
title: "{safe_title}"
description: "{safe_description}"
cover: {product_data['images'][0] if product_data['images'] else ''}
date: {date_str}
tags:
{safe_tags_str}
layout: layouts/post.njk
permalink: /posts/{slug}/
---

**{ai_content['title']}**

{ai_content['intro']}

---

**[ {product_data['title']} ](https://www.nillianstore.com/shop/{product_data['id'].lower()}/)**

{ai_content['product_section']}

> 💡 *Why It Works*:  
{chr(10).join([f"> - {point}" for point in ai_content['why_it_works']])}

👉 **Perfect for**: {ai_content['perfect_for']}

{image_html_list[0] if len(image_html_list) > 0 else ''}

<!-- Buy Button -->
{amazon_button}

{image_html_list[1] if len(image_html_list) > 1 else ''}

{image_html_list[2] if len(image_html_list) > 2 else ''}

---

**✨ Final Thought**

{ai_content['conclusion']}
"""
    
    with open(file_path, "w") as f:
        f.write(content.strip() + "\n")
    
    return file_name

def main():
    if not GROQ_API_KEY:
        print("Missing GROQ_API_KEY.")
        return

    try:
        product_file = get_random_product()
        if product_file is None:
            print("Every shop product already has a blog post. Nothing to do.")
            return
        post = frontmatter.load(product_file)
        
        # Get all images from frontmatter
        images = []
        if post.get("cover"):
            images.append(post.get("cover"))
        if post.get("images"):
            for img in post.get("images"):
                if img not in images:
                    images.append(img)
            
        # Get Amazon link - check both 'link' and 'amazonLink'
        amazon_link = post.get("link") or post.get("amazonLink") or ""
            
        product_data = {
            "id": product_file.stem,
            "title": post.get("title", ""),
            "description": post.content.strip()[:500],
            "price": post.get("price", ""),
            "link": amazon_link,
            "images": images
        }
        
        print(f"Generating blog for: {product_data['title']}")
        ai_content = generate_blog_content(product_data)
        
        file_name = create_blog_file(product_data, ai_content)
        save_blog_history(product_data['id'])
        
        print(f"Successfully created blog post: {file_name}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
