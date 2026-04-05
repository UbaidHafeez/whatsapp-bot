"""
UltraMsg Diagnostic Script
Tests your API connection and shows detailed status
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.environ.get("ULTRAMSG_TOKEN", "")
INSTANCE_ID = os.environ.get("ULTRAMSG_INSTANCE", "")

print("=" * 60)
print("🔍 UltraMsg Diagnostic Test")
print("=" * 60)

# Test 1: Check credentials
print("\n1️⃣  Checking credentials...")
if API_TOKEN and INSTANCE_ID:
    print(f"✅ Token: {API_TOKEN[:10]}...")
    print(f"✅ Instance: {INSTANCE_ID}")
else:
    print("❌ Credentials missing!")
    exit(1)

# Test 2: Check instance status
print("\n2️⃣  Checking instance status...")
status_url = f"https://api.ultramsg.com/{INSTANCE_ID}/instance/status"
try:
    response = requests.get(status_url, params={"token": API_TOKEN}, timeout=10)
    print(f"📡 Status Code: {response.status_code}")
    print(f"📄 Response: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "authorized":
            print("✅ Instance is CONNECTED and authorized!")
        elif data.get("status") == "stopped":
            print("❌ Instance is STOPPED - needs payment!")
        else:
            print(f"⚠️ Instance status: {data.get('status')}")
    else:
        print(f"❌ Failed to get status")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Try sending a test image
print("\n3️⃣  Testing image send...")
test_image = "islamic_posts/post 3/WhatsApp Image 2026-03-25 at 5.14.40 PM.jpeg"
if os.path.exists(test_image):
    print(f"✅ Test image found: {test_image}")
    
    import base64
    with open(test_image, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode('utf-8')
    
    # Send to personal number with @c.us suffix
    send_url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/image"
    payload = {
        "token": API_TOKEN,
        "to": "923140839915@c.us",  # Personal chat format
        "image": image_base64,
        "caption": "🔍 Diagnostic Test - Did you receive this?"
    }
    
    print(f"📤 Sending test image to 923140839915@c.us...")
    try:
        response = requests.post(send_url, data=payload, timeout=30)
        print(f"📡 Response Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("sent") == "true" or result.get("message") == "ok":
                print("✅ SUCCESS! Check your WhatsApp!")
            else:
                print(f"❌ API Error: {result}")
        else:
            print(f"❌ HTTP Error {response.status_code}")
    except Exception as e:
        print(f"❌ Request failed: {e}")
else:
    print(f"❌ Test image not found: {test_image}")

print("\n" + "=" * 60)
print("📋 Summary:")
print("=" * 60)
print("If you see 'STOPPED' status, you need to:")
print("  1. Go to https://ultramsg.com")
print("  2. Login to your account")
print("  3. Activate/pay for instance167704")
print("  4. Wait 5 minutes")
print("  5. Run this test again")
print("=" * 60)
