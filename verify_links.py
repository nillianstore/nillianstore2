import frontmatter
from pathlib import Path
import re

POSTS_DIR = Path("./posts")
SHOP_DIR = Path("./shop")

# Load all shop files and create a mapping
shop_links = {}
for shop_file in SHOP_DIR.glob("*.md"):
    post = frontmatter.load(shop_file)
    product_id = shop_file.stem
    amazon_link = post.get("amazonLink", "")
    shop_links[product_id] = amazon_link

# Check blog posts
issues = []
for blog_file in POSTS_DIR.glob("*.md"):
    post = frontmatter.load(blog_file)
    content = post.content
    
    # Find image references to identify which product it's about
    img_matches = re.findall(r'/img/(B0[A-Z0-9]{8})', content)
    if not img_matches:
        continue
    
    product_id = img_matches[0]
    expected_link = shop_links.get(product_id, "NOT FOUND")
    
    # Find the button link
    button_match = re.search(r'href="(https://www\.amazon\.ae/dp/B0[A-Z0-9]{8})', content)
    if not button_match:
        continue
    
    actual_link = button_match.group(1)
    
    if expected_link and expected_link != actual_link:
        issues.append({
            "blog": blog_file.name,
            "product_id": product_id,
            "expected": expected_link,
            "actual": actual_link
        })

if issues:
    print(f"Found {len(issues)} mismatches:\n")
    for issue in issues:
        print(f"Blog: {issue['blog']}")
        print(f"  Product ID: {issue['product_id']}")
        print(f"  Expected: {issue['expected']}")
        print(f"  Actual: {issue['actual']}")
        print()
else:
    print("All blog posts have correct Amazon links!")
