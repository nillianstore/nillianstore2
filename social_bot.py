import os
import json
import random
import requests
import frontmatter
import time
import sys
import subprocess
from pathlib import Path

# Configuration
SHOP_DIR = Path("./shop")
LOG_FILE = Path("./social_log.json")
BASE_URL = "https://www.nillianstore.com" 

# API Credentials (loaded from GitHub Secrets)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
IG_USER_ID = os.getenv("IG_USER_ID")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def run_git_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"Git Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git Error: {e.stderr}")
        return False

def sync_log_to_github():
    if not GITHUB_TOKEN:
        print("Skipping Git sync: GITHUB_TOKEN not found.")
        return

    print("\n--- Syncing Log to GitHub ---")
    
    # Configure Git locally for this run
    run_git_command('git config user.name "nillianstore-bot"')
    run_git_command('git config user.email "nillianstore@gmail.com"')
    
    # Add the log file
    run_git_command('git add social_log.json')
    
    # Check if there are changes to commit
    status = subprocess.run('git diff --cached --quiet', shell=True)
    if status.returncode == 0:
        print("No changes to commit.")
        return

    # Commit changes
    if run_git_command('git commit -m "Update social posting log [skip ci]"'):
        # Push using GITHUB_TOKEN
        repo_url = f"https://x-access-token:{GITHUB_TOKEN}@github.com/nillianstore/nillianstore2.git"
        run_git_command(f'git remote set-url origin {repo_url}')
        run_git_command('git push origin main')
        print("Successfully pushed to GitHub")
    else:
        print("Failed to commit changes")

def load_posted_history():
    if LOG_FILE.exists():
        with open(LOG_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_posted_history(product_id):
    history = load_posted_history()
    history.append(product_id)
    if len(history) > 50:
        history = history[-50:]
    with open(LOG_FILE, "w") as f:
        json.dump(history, f, indent=2)

def get_random_product(exclude_ids=None):
    if exclude_ids is None:
        exclude_ids = []
    products = list(SHOP_DIR.glob("*.md"))
    if not products:
        print("Error: No product files found in shop directory.")
        return None
        
    history = load_posted_history()
    available = [p for p in products if p.stem not in history and p.stem not in exclude_ids]
    
    if not available:
        print("All products in history. Resetting selection.")
        available = [p for p in products if p.stem not in exclude_ids]
    
    return random.choice(available) if available else None

def clean_image_path(image_path):
    if image_path.startswith("./"): image_path = image_path[2:]
    elif image_path.startswith("/"): image_path = image_path[1:]
    return f"{BASE_URL}/{image_path}"

def parse_product(file_path):
    post = frontmatter.load(file_path)
    title = post.get("title", "Check out our latest product!")
    description = post.content.strip()[:500]
    price = post.get("price", "")
    amazon_link = post.get("link", "") or post.get("amazonLink", "")
    
    image_urls = []
    if post.get("cover"): image_urls.append(clean_image_path(post.get("cover")))
    if post.get("images"):
        for img in post.get("images"):
            url = clean_image_path(img)
            if url not in image_urls: image_urls.append(url)
    
    return {
        "id": file_path.stem, "title": title, "description": description,
        "price": price, "link": amazon_link, "image_urls": image_urls
    }

def generate_content(product_data):
    prompt = f"Product: {product_data['title']}\nDetails: {product_data['description']}\nPrice: {product_data['price']}\nLink: {product_data['link']}\nCreate an engaging Instagram/Facebook post for Nillian Store (UAE). Include emojis and 10-15 hashtags. Format as JSON: {{\"caption\": \"...\", \"hashtags\": \"...\"}}"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }
    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        return json.loads(response.json()["choices"][0]["message"]["content"])
    except requests.exceptions.RequestException as e:
        print(f"GROQ API Error: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        raise

def post_to_instagram(image_urls, caption):
    try:
        if not image_urls: 
            print("Instagram: No images provided")
            return None
        url = f"https://graph.facebook.com/v18.0/{IG_USER_ID}/media"
        print(f"  → Instagram API URL: {url}")
        print(f"  → Image URLs: {image_urls}")
        print(f"  → Caption length: {len(caption)} chars")
        
        if len(image_urls) == 1:
            params = {
                "image_url": image_urls[0], 
                "caption": caption, 
                "access_token": META_ACCESS_TOKEN
            }
            print(f"  → Single image request params: image_url={image_urls[0][:50]}..., caption={len(caption)} chars")
            r = requests.post(url, data=params)
            r.raise_for_status()
            creation_id = r.json()["id"]
        else:
            child_ids = []
            for i, img_url in enumerate(image_urls[:10]):
                params = {
                    "image_url": img_url,
                    "is_carousel_item": "true", 
                    "access_token": META_ACCESS_TOKEN
                }
                print(f"  → Carousel item {i+1}: {img_url[:50]}...")
                r = requests.post(url, data=params)
                r.raise_for_status()
                child_ids.append(r.json()["id"])
            
            params = {
                "media_type": "CAROUSEL", 
                "children": ",".join(child_ids), 
                "caption": caption, 
                "access_token": META_ACCESS_TOKEN
            }
            r = requests.post(url, data=params)
            r.raise_for_status()
            creation_id = r.json()["id"]

        time.sleep(15)
        publish_url = f"https://graph.facebook.com/v18.0/{IG_USER_ID}/media_publish"
        r = requests.post(publish_url, data={"creation_id": creation_id, "access_token": META_ACCESS_TOKEN})
        r.raise_for_status()
        return r.json().get("id")
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Instagram API Error: {e.response.status_code if hasattr(e, 'response') and e.response else 'Unknown'} - {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                print(f"  ✗ API Response: {json.dumps(error_data, indent=2)}")
                # Check for expired token
                if error_data.get('error', {}).get('code') == 190:
                    print("\n  ⚠️  ACCESS TOKEN EXPIRED!")
                    print("  → Your META_ACCESS_TOKEN has expired.")
                    print("  → Get a new long-lived token from Facebook Developer Console:")
                    print("  → https://developers.facebook.com/tools/explorer")
                    print("  → Update the META_ACCESS_TOKEN secret in GitHub Settings")
            except:
                print(f"  ✗ Response Body: {e.response.text}")
        return None
    except Exception as e:
        print(f"  ✗ Instagram Error (Unexpected): {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def post_to_facebook(image_urls, caption):
    try:
        if not image_urls: 
            print("Facebook: No images provided")
            return None
        url = f"https://graph.facebook.com/v18.0/{FB_PAGE_ID}/photos"
        print(f"  → Facebook API URL: {url}")
        print(f"  → Image URL: {image_urls[0][:50]}...")
        print(f"  → Caption length: {len(caption)} chars")
        
        params = {
            "url": image_urls[0], 
            "message": caption, 
            "access_token": META_ACCESS_TOKEN
        }
        r = requests.post(url, data=params)
        r.raise_for_status()
        return r.json().get("id")
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Facebook API Error: {e.response.status_code if hasattr(e, 'response') and e.response else 'Unknown'} - {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                print(f"  ✗ API Response: {json.dumps(error_data, indent=2)}")
                # Check for expired token
                if error_data.get('error', {}).get('code') == 190:
                    print("\n  ⚠️  ACCESS TOKEN EXPIRED!")
                    print("  → Your META_ACCESS_TOKEN has expired.")
                    print("  → Get a new long-lived token from Facebook Developer Console:")
                    print("  → https://developers.facebook.com/tools/explorer")
                    print("  → Update the META_ACCESS_TOKEN secret in GitHub Settings")
            except:
                print(f"  ✗ Response Body: {e.response.text}")
        return None
    except Exception as e:
        print(f"  ✗ Facebook Error (Unexpected): {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def main():
    required = {
        "GROQ_API_KEY": GROQ_API_KEY,
        "META_ACCESS_TOKEN": META_ACCESS_TOKEN,
        "FB_PAGE_ID": FB_PAGE_ID,
        "IG_USER_ID": IG_USER_ID,
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        print(f"ERROR: Missing required secrets in GitHub: {', '.join(missing)}")
        print("\nPlease set these secrets in your GitHub repository:")
        print("1. Go to Settings > Secrets and variables > Actions")
        print("2. Add these secrets:")
        for secret in missing:
            print(f"   - {secret}")
        sys.exit(1)
    
    if not GITHUB_TOKEN:
        print("WARNING: GITHUB_TOKEN not found. Log syncing will be skipped.")

    failed_ids = []
    success = False

    for attempt in range(3):
        try:
            product_file = get_random_product(exclude_ids=failed_ids)
            if not product_file: 
                print("No products available to post.")
                break
            
            product_data = parse_product(product_file)
            if not product_data["image_urls"]:
                failed_ids.append(product_data['id'])
                print(f"Skipping {product_data['id']}: No images found")
                continue

            print(f"Generating content for: {product_data['title']}")
            ai_content = generate_content(product_data)
            full_caption = f"{ai_content['caption']}\n\n{ai_content['hashtags']}\n\nShop here: {product_data['link']}"
            
            print("Posting to Instagram and Facebook...")
            ig_id = post_to_instagram(product_data["image_urls"], full_caption)
            fb_id = post_to_facebook(product_data["image_urls"], full_caption)
            
            if ig_id or fb_id:
                save_posted_history(product_data["id"])
                print(f"✓ Successfully posted: {product_data['id']}")
                if GITHUB_TOKEN:
                    sync_log_to_github()
                success = True
                break
            else:
                failed_ids.append(product_data['id'])
                print(f"Failed to post {product_data['id']} to social media")
        except Exception as e:
            print(f"ERROR (attempt {attempt+1}/3): {str(e)}")
            if 'product_file' in locals() and product_file: 
                failed_ids.append(product_file.stem)

    if not success: 
        print("ERROR: Failed to post to social media after 3 attempts")
        sys.exit(1)
    
    print("\n✓ Social bot completed successfully!")

if __name__ == "__main__":
    main()
