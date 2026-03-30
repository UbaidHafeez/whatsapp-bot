"""
WhatsApp Bot - Debug Version
Shows detailed error messages
"""

import os
import base64
import requests
import json
import logging
from datetime import datetime

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTS_FOLDER = os.path.join(BASE_DIR, "islamic_posts")
GROUPS_FILE = os.path.join(BASE_DIR, "groups.txt")
DB_FILE = os.path.join(BASE_DIR, "posts_db.json")

# Get credentials from environment
API_TOKEN = os.environ.get("ULTRAMSG_TOKEN", "")
INSTANCE_ID = os.environ.get("ULTRAMSG_INSTANCE", "")

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger(__name__)

def load_groups():
    """Load groups from file"""
    if not os.path.exists(GROUPS_FILE):
        log.error(f"❌ groups.txt not found!")
        return []
    
    with open(GROUPS_FILE, "r", encoding="utf-8") as f:
        groups = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    log.info(f"📱 Loaded {len(groups)} group(s): {groups}")
    return groups

def scan_posts():
    """Scan for unsent posts"""
    if not os.path.exists(POSTS_FOLDER):
        log.error(f"❌ Posts folder not found!")
        return []
    
    posts = []
    for folder in sorted(os.listdir(POSTS_FOLDER)):
        if folder.startswith("sent_"):
            continue
        
        folder_path = os.path.join(POSTS_FOLDER, folder)
        if not os.path.isdir(folder_path):
            continue
        
        urdu_img = os.path.join(folder_path, "urdu.jpg")
        eng_img = os.path.join(folder_path, "eng.jpg")
        
        if os.path.exists(urdu_img) and os.path.exists(eng_img):
            posts.append(folder)
            log.info(f"✅ Found post: {folder}")
        else:
            log.warning(f"⚠️ Skipping '{folder}' — missing images")
    
    log.info(f"📦 Detected {len(posts)} post(s): {posts}")
    return posts

def load_db():
    """Load database"""
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_next_unsent_post(db, posts):
    """Get next unsent post"""
    for post in posts:
        if db.get(post, False) is False:
            return post
    return None

def mark_post_sent(db, post_name):
    """Mark post as sent"""
    db[post_name] = True
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4)
    log.info(f"✅ Marked '{post_name}' as sent")

def rename_folder_sent(post_name):
    """Rename folder to sent_"""
    old_folder = os.path.join(POSTS_FOLDER, post_name)
    new_folder = os.path.join(POSTS_FOLDER, f"sent_{post_name}")
    
    try:
        if os.path.exists(old_folder):
            os.rename(old_folder, new_folder)
            log.info(f"✅ Renamed folder: {post_name} → sent_{post_name}")
    except Exception as e:
        log.error(f"❌ Failed to rename folder: {e}")

def image_to_base64(image_path):
    """Convert image to base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def send_image(group_name, image_path, caption=""):
    """Send image via UltraMsg API"""
    
    log.info(f"📤 Sending to: {group_name}")
    log.info(f"🖼️ Image: {os.path.basename(image_path)}")
    
    # Check file exists
    if not os.path.exists(image_path):
        log.error(f"❌ Image file not found: {image_path}")
        return False
    
    # Check file size
    file_size = os.path.getsize(image_path) / (1024 * 1024)  # MB
    log.info(f"📊 Image size: {file_size:.2f} MB")
    
    if file_size > 5:
        log.error(f"❌ Image too large! Must be under 5MB")
        return False
    
    # Convert to base64
    image_base64 = image_to_base64(image_path)
    log.info(f"📝 Encoded image ({len(image_base64)} chars)")
    
    # API URL
    api_url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/image"
    
    # Payload
    payload = {
        "token": API_TOKEN,
        "to": group_name,
        "image": image_base64,
        "caption": caption
    }
    
    log.info(f"🔗 API URL: {api_url}")
    log.info(f"📮 Recipient: {group_name}")
    
    try:
        # Send request
        log.info(f"⏳ Sending...")
        response = requests.post(api_url, data=payload, timeout=30)
        
        log.info(f"📡 Response Status: {response.status_code}")
        log.info(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            log.info(f"📋 Result: {result}")
            
            if result.get("sent") == "true" or result.get("message") == "ok":
                log.info(f"✅ SUCCESS! Sent to {group_name}")
                return True
            else:
                log.error(f"❌ API Error: {result}")
                return False
        else:
            log.error(f"❌ HTTP Error {response.status_code}")
            log.error(f"📄 Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        log.error(f"❌ Timeout - API took too long to respond")
        return False
    except Exception as e:
        log.error(f"❌ Request failed: {e}")
        return False

def main():
    """Main function"""
    log.info("=" * 60)
    log.info("🤖 WhatsApp Bot - Debug Version")
    log.info("=" * 60)
    
    # Check credentials
    if not API_TOKEN or not INSTANCE_ID:
        log.error("❌ ERROR: API credentials not set!")
        log.error("❌ Please add ULTRAMSG_TOKEN and ULTRAMSG_INSTANCE to GitHub Secrets")
        return
    
    log.info(f"✅ API Token: {API_TOKEN[:10]}...")
    log.info(f"✅ Instance ID: {INSTANCE_ID}")
    
    # Load groups
    groups = load_groups()
    if not groups:
        log.error("❌ No groups found! Check groups.txt")
        return
    
    # Scan posts
    posts = scan_posts()
    if not posts:
        log.info("✅ No new posts to send")
        return
    
    # Load database
    db = load_db()
    
    # Get next unsent post
    post_name = get_next_unsent_post(db, posts)
    if not post_name:
        log.info("✅ All posts already sent!")
        return
    
    log.info(f"📮 Selected post: {post_name}")
    
    # Prepare paths
    post_folder = os.path.join(POSTS_FOLDER, post_name)
    urdu_img = os.path.join(post_folder, "urdu.jpg")
    eng_img = os.path.join(post_folder, "eng.jpg")
    
    log.info(f"🖼️ Urdu image: {urdu_img}")
    log.info(f"🖼️ English image: {eng_img}")
    
    # Check files exist
    if not os.path.exists(urdu_img):
        log.error(f"❌ Urdu image not found: {urdu_img}")
        return
    if not os.path.exists(eng_img):
        log.error(f"❌ English image not found: {eng_img}")
        return
    
    # Send to each group
    successful = []
    failed = []
    
    for group in groups:
        log.info("-" * 60)
        log.info(f"📱 Sending to: {group}")
        log.info("-" * 60)
        
        # Send Urdu
        success_urdu = send_image(group, urdu_img, caption="")
        
        if success_urdu:
            # Send English
            success_eng = send_image(group, eng_img, caption="")
            
            if success_eng:
                successful.append(group)
                log.info(f"✅ Both images sent to {group}")
            else:
                failed.append(group)
                log.warning(f"⚠️ English image failed for {group}")
        else:
            failed.append(group)
            log.warning(f"⚠️ Urdu image failed for {group}")
    
    # Summary
    log.info("=" * 60)
    log.info("📊 SUMMARY")
    log.info("=" * 60)
    
    if successful:
        log.info(f"✅ Success: {len(successful)} group(s)")
        for g in successful:
            log.info(f"   ✓ {g}")
        
        # Mark as sent
        mark_post_sent(db, post_name)
        rename_folder_sent(post_name)
    else:
        log.info(f"❌ Failed: {len(failed)} group(s)")
        for g in failed:
            log.info(f"   ✗ {g}")
    
    if failed:
        log.info("=" * 60)
        log.info("🔧 TROUBLESHOOTING TIPS:")
        log.info("=" * 60)
        log.info("1. Check phone number format: 923140839915 (no + or 0)")
        log.info("2. Check UltraMsg instance is connected")
        log.info("3. Check API credentials in GitHub Secrets")
        log.info("4. Check image size (must be under 5MB)")
        log.info("5. Check UltraMsg balance/limits")
    
    log.info("=" * 60)

if __name__ == "__main__":
    main()
