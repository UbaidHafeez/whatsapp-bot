"""
=============================================================
  WhatsApp Islamic Post Sender via REST API
  Author: Auto-generated
  Description: Sends images via WhatsApp Gateway API (Base64)
               Bypasses UI entirely - immune to DOM changes
=============================================================
"""

import os
import base64
import requests
import json
import logging
import time
import schedule
from datetime import datetime

# Try to import easyocr for language detection
try:
    import easyocr
    OCR_AVAILABLE = True
    ocr_reader = None
except ImportError:
    OCR_AVAILABLE = False
    log = logging.getLogger(__name__)
    log.warning("easyocr not installed - will use filename-based detection")
    log.warning("Install with: pip install easyocr")

# ──────────────────────────────────────────────
#  CONFIGURATION
# ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTS_FOLDER = os.path.join(BASE_DIR, "islamic_posts")
GROUPS_FILE = os.path.join(BASE_DIR, "groups.txt")
LOG_FILE = os.path.join(BASE_DIR, "bot_log.txt")
DB_FILE = os.path.join(BASE_DIR, "posts_db.json")

# Import API credentials from config file
try:
    from api_config import ULTRAMSG_TOKEN, ULTRAMSG_INSTANCE, ULTRAMSG_ENABLED, USE_ULTRAMSG
    API_TOKEN = ULTRAMSG_TOKEN
    INSTANCE_ID = ULTRAMSG_INSTANCE
    API_ENABLED = ULTRAMSG_ENABLED and USE_ULTRAMSG
except ImportError:
    API_TOKEN = "YOUR_API_TOKEN_HERE"
    INSTANCE_ID = "YOUR_INSTANCE_ID"
    API_ENABLED = False

# UltraMsg API URL
API_GATEWAY_URL = "https://api.ultramsg.com/" + INSTANCE_ID + "/messages/image" if API_ENABLED else ""

# ──────────────────────────────────────────────
#  LOGGER SETUP
# ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)


# ══════════════════════════════════════════════
#  1. OCR LANGUAGE DETECTOR
# ══════════════════════════════════════════════
def get_ocr_reader():
    """Initialize OCR reader (only once)"""
    global ocr_reader
    if ocr_reader is None and OCR_AVAILABLE:
        log.info("Loading AI OCR models for language detection...")
        ocr_reader = easyocr.Reader(['ur', 'en'], verbose=False)
        log.info("✓ OCR models loaded")
    return ocr_reader


def identify_urdu_and_english_images(folder_path: str) -> tuple:
    """
    Automatically detect which image is Urdu and which is English using AI OCR.
    Returns: (urdu_image_path, english_image_path)
    """
    # Get all image files
    images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    if len(images) != 2:
        log.warning(f"Expected 2 images, found {len(images)}")
        return None, None

    # If already named correctly, use them
    if 'urdu.jpg' in images and 'eng.jpg' in images:
        log.info("✓ Images already named correctly")
        return os.path.join(folder_path, 'urdu.jpg'), os.path.join(folder_path, 'eng.jpg')

    img1_path = os.path.join(folder_path, images[0])
    img2_path = os.path.join(folder_path, images[1])

    log.info(f"🔍 Analyzing images with AI OCR to detect Urdu/English...")

    # Use OCR to detect language
    reader = get_ocr_reader()

    if reader:
        # OCR detection
        res1 = reader.readtext(img1_path, detail=0)
        res2 = reader.readtext(img2_path, detail=0)
        text1 = " ".join(res1)
        text2 = " ".join(res2)

        # Count Urdu characters (Arabic script)
        ur_chars1 = sum(1 for c in text1 if '\u0600' <= c <= '\u06FF')
        ur_chars2 = sum(1 for c in text2 if '\u0600' <= c <= '\u06FF')

        log.info(f"  Image 1: {ur_chars1} Urdu characters")
        log.info(f"  Image 2: {ur_chars2} Urdu characters")

        # Image with more Urdu characters is Urdu
        if ur_chars1 > ur_chars2:
            urdu_file, eng_file = img1_path, img2_path
            log.info("✓ Image 1 is Urdu, Image 2 is English")
        else:
            urdu_file, eng_file = img2_path, img1_path
            log.info("✓ Image 2 is Urdu, Image 1 is English")

        # Rename files for consistency
        temp_u = os.path.join(folder_path, "temp_ur.jpg")
        temp_e = os.path.join(folder_path, "temp_en.jpg")
        os.rename(urdu_file, temp_u)
        os.rename(eng_file, temp_e)
        os.rename(temp_u, os.path.join(folder_path, "urdu.jpg"))
        os.rename(temp_e, os.path.join(folder_path, "eng.jpg"))

        log.info(f"✓ Renamed images to urdu.jpg and eng.jpg")
        return os.path.join(folder_path, 'urdu.jpg'), os.path.join(folder_path, 'eng.jpg')
    else:
        # Fallback: assume alphabetical order (first is English, second is Urdu)
        log.info("OCR not available - using filename order")
        sorted_images = sorted(images)
        return os.path.join(folder_path, sorted_images[0]), os.path.join(folder_path, sorted_images[1])


# ══════════════════════════════════════════════
#  1. IMAGE ENCODER
# ══════════════════════════════════════════════
def image_to_base64(image_path: str) -> str:
    """
    Convert image file to Base64 encoded string.
    
    Args:
        image_path: Absolute path to image file
        
    Returns:
        Base64 encoded string (without data:image prefix)
    """
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        log.info(f"✓ Encoded image: {os.path.basename(image_path)} ({len(encoded_string)} chars)")
        return encoded_string
    except Exception as e:
        log.error(f"✗ Failed to encode image: {e}")
        raise


# ══════════════════════════════════════════════
#  2. POST SCANNER
# ══════════════════════════════════════════════
def scan_posts() -> list[str]:
    """Scan for valid post folders with urdu.jpg and eng.jpg (skip sent_ folders)"""
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

def get_next_unsent_post(db: dict, available_posts: list[str]) -> str | None:
    for post in available_posts:
        # If post is not in DB or is False, it's unsent
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
def load_groups() -> list[str]:
    if not os.path.exists(GROUPS_FILE):
        log.error(f"groups.txt not found at: {GROUPS_FILE}")
        return []
    with open(GROUPS_FILE, "r", encoding="utf-8") as f:
        groups = [line.strip() for line in f if line.strip()]
    log.info(f"Loaded {len(groups)} group(s): {groups}")
    return groups


# ══════════════════════════════════════════════
#  5. API SENDER (UltraMsg)
# ══════════════════════════════════════════════
def send_image_via_api(group_name: str, image_path: str, caption: str = "") -> bool:
    """
    Send image to WhatsApp group via UltraMsg API.

    This bypasses the UI entirely by using Base64 encoding.
    UltraMsg API: https://api.ultramsg.com/{instance_id}/messages/image

    Args:
        group_name: Name of the WhatsApp group or phone number
        image_path: Path to image file
        caption: Optional caption text

    Returns:
        True if sent successfully, False otherwise
    """
    # Encode image to Base64
    image_base64 = image_to_base64(image_path)

    # UltraMsg API URL with token as parameter
    api_url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/image"

    # Convert group name to proper format
    # If it's a name (not a number), we need to get the actual group ID or phone
    # For now, try sending to the name directly (UltraMsg might resolve it)
    recipient = group_name

    # If recipient doesn't look like a phone number or group ID, add @g.us for groups
    if not recipient.endswith('@g.us') and not recipient.endswith('@s.whatsapp.net'):
        # Check if it's a phone number (all digits)
        if recipient.replace('+', '').isdigit():
            # It's a phone number, add @s.whatsapp.net for individuals
            recipient = recipient + '@s.whatsapp.net'
        else:
            # It's a name, try as group name (UltraMsg will try to resolve)
            # For groups, we need the actual group JID
            # For now, pass as-is and let UltraMsg handle it
            pass

    # Prepare API payload for UltraMsg
    payload = {
        "token": API_TOKEN,
        "to": recipient,
        "image": image_base64,
        "caption": caption
    }

    try:
        log.info(f"Sending to UltraMsg API: {group_name} (as: {recipient}) - {os.path.basename(image_path)}")

        # Send POST request (UltraMsg expects form-data, not JSON)
        response = requests.post(api_url, data=payload, timeout=30)

        # Check response
        if response.status_code == 200:
            result = response.json()
            # UltraMsg returns {'sent': 'true', 'message': 'ok', 'id': xxx} on success
            if result.get("sent") == "true" or result.get("success") == True or result.get("message") == "ok":
                log.info(f"✓ API sent successfully to '{group_name}'")
                return True
            else:
                log.error(f"✗ API error: {result}")
                return False
        else:
            log.error(f"✗ HTTP {response.status_code}: {response.text}")
            return False

    except requests.exceptions.Timeout:
        log.error(f"✗ API timeout for '{group_name}'")
        return False
    except requests.exceptions.RequestException as e:
        log.error(f"✗ API request failed: {e}")
        return False
    except Exception as e:
        log.error(f"✗ Unexpected error: {e}")
        return False


# ══════════════════════════════════════════════
#  6. ALTERNATIVE: TWILIO WHATSAPP API
# ══════════════════════════════════════════════
def send_via_twilio(group_id: str, image_path: str, caption: str = "") -> bool:
    """
    Send via Twilio WhatsApp Business API.
    
    Requires: pip install twilio
    """
    try:
        from twilio.rest import Client
        
        # Twilio credentials (set as environment variables)
        account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        from_number = os.environ.get("TWILIO_WHATSAPP_NUMBER")
        
        if not all([account_sid, auth_token, from_number]):
            log.error("Twilio credentials not configured")
            return False
        
        client = Client(account_sid, auth_token)
        
        # Upload media
        media = client.media.create(
            from_=f"whatsapp:{from_number}",
            filename=os.path.basename(image_path),
            path=image_path
        )
        
        # Send message with media
        message = client.messages.create(
            from_=f"whatsapp:{from_number}",
            body=caption,
            media_sid=media.sid,
            to=f"whatsapp:{group_id}"  # Group ID format: <group_id>@g.us
        )
        
        log.info(f"✓ Twilio sent: {message.sid}")
        return True
        
    except ImportError:
        log.error("Twilio library not installed. Run: pip install twilio")
        return False
    except Exception as e:
        log.error(f"✗ Twilio error: {e}")
        return False


# ══════════════════════════════════════════════
#  7. MAIN DAILY JOB (API VERSION)
# ══════════════════════════════════════════════
def daily_job_api():
    """Main job using REST API approach"""
    log.info("=" * 60)
    log.info(f"Daily job started (API mode) — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.info("=" * 60)
    
    # Scan for posts
    posts = scan_posts()
    if not posts:
        log.error("No valid posts found. Aborting.")
        return
    
    # Load database
    db = load_db()
    
    # Get next unsent post
    post_name = get_next_unsent_post(db, posts)
    if not post_name:
        log.info("All posts sent! Add new folders to continue.")
        return
    
    log.info(f"Selected post: '{post_name}'")

    # Load groups
    groups = load_groups()
    if not groups:
        log.error("No groups found. Aborting.")
        return

    # Auto-detect Urdu and English images using AI OCR
    post_folder = os.path.join(POSTS_FOLDER, post_name)
    urdu_img, eng_img = identify_urdu_and_english_images(post_folder)

    if not urdu_img or not eng_img:
        log.error("Failed to identify Urdu and English images")
        return

    log.info(f"Urdu image: {os.path.basename(urdu_img)}")
    log.info(f"English image: {os.path.basename(eng_img)}")

    # Track success/failure
    successful = []
    failed = []

    # Send to each group
    for group in groups:
        try:
            # Send Urdu image (NO caption)
            success_urdu = send_image_via_api(
                group,
                urdu_img,
                caption=""
            )

            if success_urdu:
                # Send English image (NO caption)
                success_eng = send_image_via_api(
                    group,
                    eng_img,
                    caption=""
                )
                
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

        # Check for next unsent post
        next_post = get_next_unsent_post(db, scan_posts())
        if next_post:
            log.info(f"➡️  Next unsent post: '{next_post}'")
            log.info("➡️  Sending next post automatically...")
            time.sleep(2)
            # Send next post (recursive call)
            daily_job_api()
        else:
            log.info("✅ All posts sent! No more unsent posts.")
    else:
        log.error(f"❌ Post '{post_name}' was NOT sent to any group")

    if failed:
        log.warning(f"⚠️  Failed groups: {failed}")

    log.info(f"Daily job complete — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.info("=" * 60)


# ══════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════
if __name__ == "__main__":
    import sys

    # Check if API is configured
    if not API_ENABLED or API_TOKEN == "YOUR_API_TOKEN_HERE":
        log.error("=" * 60)
        log.error("API NOT CONFIGURED!")
        log.error("=" * 60)
        log.error("Please update api_config.py with your UltraMsg credentials")
        log.error("=" * 60)
    else:
        if len(sys.argv) > 1 and sys.argv[1] == "--now":
            log.info("Running immediately (--now flag detected) …")
            daily_job_api()
        else:
            # Schedule for 7 PM daily
            log.info("=" * 60)
            log.info("🕖 SCHEDULER STARTED - Will run daily at 7:00 PM")
            log.info("=" * 60)
            log.info("Press Ctrl+C to stop\n")

            # Schedule daily job at 7 PM (19:00)
            schedule.every().day.at("19:00").do(daily_job_api)

            # Run scheduler
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
