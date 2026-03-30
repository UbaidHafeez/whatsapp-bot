"""
=============================================================
  WhatsApp Islamic Post Sender - CLOUD VERSION
  For GitHub Actions (runs automatically at 7 PM daily)
=============================================================
"""

import os
import base64
import requests
import json
import logging
from datetime import datetime

# ──────────────────────────────────────────────
#  CONFIGURATION
# ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTS_FOLDER = os.path.join(BASE_DIR, "islamic_posts")
GROUPS_FILE = os.path.join(BASE_DIR, "groups.txt")
LOG_FILE = os.path.join(BASE_DIR, "bot_log.txt")
DB_FILE = os.path.join(BASE_DIR, "posts_db.json")

# Get credentials from environment variables (GitHub Secrets)
API_TOKEN = os.environ.get("ULTRAMSG_TOKEN", "")
INSTANCE_ID = os.environ.get("ULTRAMSG_INSTANCE", "")
API_ENABLED = bool(API_TOKEN and INSTANCE_ID)

# UltraMsg API URL
API_GATEWAY_URL = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/image" if API_ENABLED else ""

# ──────────────────────────────────────────────
#  LOGGER SETUP
# ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()  # Also print to console for GitHub Actions
    ]
)
log = logging.getLogger(__name__)


# ══════════════════════════════════════════════
#  1. IMAGE ENCODER
# ══════════════════════════════════════════════
def image_to_base64(image_path: str) -> str:
    """Convert image file to Base64 encoded string"""
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        log.info(f"✓ Encoded image: {os.path.basename(image_path)}")
        return encoded_string
    except Exception as e:
        log.error(f"✗ Failed to encode image: {e}")
        raise


# ══════════════════════════════════════════════
#  2. POST SCANNER
# ══════════════════════════════════════════════
def scan_posts() -> list:
    """Scan for valid post folders (skip sent_ folders)"""
    if not os.path.exists(POSTS_FOLDER):
        log.warning(f"Posts folder not found: {POSTS_FOLDER}")
        return []

    posts = []
    for folder in sorted(os.listdir(POSTS_FOLDER)):
        # Skip folders that start with "sent_"
        if folder.startswith("sent_"):
            continue
            
        folder_path = os.path.join(POSTS_FOLDER, folder)
        if not os.path.isdir(folder_path):
            continue

        urdu_img = os.path.join(folder_path, "urdu.jpg")
        eng_img = os.path.join(folder_path, "eng.jpg")

        if os.path.exists(urdu_img) and os.path.exists(eng_img):
            posts.append(folder)
            log.info(f"✓ Valid post: {folder}")
        else:
            log.warning(f"Skipping '{folder}' — missing urdu.jpg or eng.jpg")
    
    log.info(f"Detected {len(posts)} valid post(s): {posts}")
    return posts


# ══════════════════════════════════════════════
#  3. DATABASE MANAGER
# ══════════════════════════════════════════════
def load_db() -> dict:
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(db: dict):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4)

def get_next_unsent_post(db: dict, available_posts: list) -> str:
    for post in available_posts:
        if db.get(post, False) is False:
            return post
    return None

def mark_post_sent(db: dict, post_name: str):
    db[post_name] = True
    save_db(db)
    log.info(f"✓ Post '{post_name}' marked as sent.")


def rename_folder_sent(post_name: str):
    """Rename post folder to 'sent_postname' after sending"""
    old_folder = os.path.join(POSTS_FOLDER, post_name)
    new_folder = os.path.join(POSTS_FOLDER, f"sent_{post_name}")
    
    try:
        if os.path.exists(old_folder):
            os.rename(old_folder, new_folder)
            log.info(f"✓ Folder renamed: '{post_name}' → 'sent_{post_name}'")
    except Exception as e:
        log.error(f"✗ Failed to rename folder: {e}")


# ══════════════════════════════════════════════
#  4. GROUPS READER
# ══════════════════════════════════════════════
def load_groups() -> list:
    if not os.path.exists(GROUPS_FILE):
        log.error(f"groups.txt not found at: {GROUPS_FILE}")
        return []
    with open(GROUPS_FILE, "r", encoding="utf-8") as f:
        groups = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    log.info(f"Loaded {len(groups)} group(s): {groups}")
    return groups


# ══════════════════════════════════════════════
#  5. API SENDER
# ══════════════════════════════════════════════
def send_image_via_api(group_name: str, image_path: str, caption: str = "") -> bool:
    """Send image to WhatsApp group via UltraMsg API"""
    image_base64 = image_to_base64(image_path)
    
    api_url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/image"
    
    payload = {
        "token": API_TOKEN,
        "to": group_name,
        "image": image_base64,
        "caption": caption
    }

    try:
        log.info(f"Sending to API: {group_name} - {os.path.basename(image_path)}")
        
        response = requests.post(api_url, data=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("sent") == "true" or result.get("message") == "ok":
                log.info(f"✓ API sent successfully to '{group_name}'")
                return True
            else:
                log.error(f"✗ API error: {result}")
                return False
        else:
            log.error(f"✗ HTTP {response.status_code}: {response.text}")
            return False

    except Exception as e:
        log.error(f"✗ Request failed: {e}")
        return False


# ══════════════════════════════════════════════
#  6. MAIN JOB
# ══════════════════════════════════════════════
def daily_job_api():
    """Main job for GitHub Actions"""
    log.info("=" * 60)
    log.info(f"Cloud Bot Started — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.info("=" * 60)
    
    # Check API configuration
    if not API_ENABLED:
        log.error("❌ API credentials not configured!")
        log.error("Please set ULTRAMSG_TOKEN and ULTRAMSG_INSTANCE in GitHub Secrets")
        return
    
    # Scan for posts
    posts = scan_posts()
    if not posts:
        log.info("✅ No new posts to send")
        return
    
    # Load database
    db = load_db()
    
    # Get next unsent post
    post_name = get_next_unsent_post(db, posts)
    if not post_name:
        log.info("✅ All posts sent! Add new folders to continue.")
        return
    
    log.info(f"Selected post: '{post_name}'")
    
    # Load groups
    groups = load_groups()
    if not groups:
        log.error("No groups found. Aborting.")
        return
    
    # Prepare image paths
    post_folder = os.path.join(POSTS_FOLDER, post_name)
    urdu_img = os.path.join(post_folder, "urdu.jpg")
    eng_img = os.path.join(post_folder, "eng.jpg")
    
    # Track success/failure
    successful = []
    failed = []
    
    # Send to each group
    for group in groups:
        try:
            # Send Urdu image (NO caption)
            success_urdu = send_image_via_api(group, urdu_img, caption="")
            
            if success_urdu:
                # Send English image (NO caption)
                success_eng = send_image_via_api(group, eng_img, caption="")
                
                if success_eng:
                    successful.append(group)
                    log.info(f"✓ Both images sent to '{group}'")
                else:
                    failed.append(group)
                    log.warning(f"⚠️ English image failed for '{group}'")
            else:
                failed.append(group)
                log.warning(f"⚠️ Urdu image failed for '{group}'")
                
        except Exception as e:
            failed.append(group)
            log.error(f"✗ Error sending to '{group}': {e}")
    
    # Update database and rename folder
    if successful:
        mark_post_sent(db, post_name)
        rename_folder_sent(post_name)
        log.info(f"✅ Post '{post_name}' sent to {len(successful)} group(s)")
    else:
        log.error(f"❌ Post '{post_name}' was NOT sent to any group")
    
    if failed:
        log.warning(f"⚠️  Failed groups: {failed}")
    
    log.info(f"Cloud job complete — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.info("=" * 60)


# ══════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════
if __name__ == "__main__":
    daily_job_api()
