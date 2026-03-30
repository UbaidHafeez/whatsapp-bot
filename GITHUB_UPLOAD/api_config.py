# ============================================
# WhatsApp Bot API Configuration
# ============================================

# OPTION 1: UltraMsg (Recommended for beginners)
# 1. Go to https://ultramsg.com
# 2. Sign up for free account
# 3. Create new instance
# 4. Copy your token and instance ID below

ULTRAMSG_TOKEN = "pak8408yn0osmffv"
ULTRAMSG_INSTANCE = "instance167704"
ULTRAMSG_ENABLED = True  # ✅ Enabled

# OPTION 2: Twilio WhatsApp API (Official but more complex)
# 1. Go to https://www.twilio.com/whatsapp
# 2. Sign up and create account
# 3. Get your credentials
# 4. Set environment variables instead of editing here

TWILIO_ENABLED = False  # Requires environment variables


# OPTION 3: WhatsMate (Paid but reliable)
# 1. Go to https://www.whatsmate.com
# 2. Sign up and purchase plan
# 3. Get your API credentials

WHATSMATE_TOKEN = "YOUR_TOKEN_HERE"
WHATSMATE_ENABLED = False  # Set to True when you add your credentials


# ============================================
# Which API to use? (Set one to True)
# ============================================
USE_ULTRAMSG = True  # ✅ Using UltraMsg
USE_TWILIO = False
USE_WHATSMATE = False


# ============================================
# Free Alternative: Use Browser Automation
# ============================================
# If all APIs are disabled (all False above),
# the script will try browser automation instead.
# Note: This is less reliable due to WhatsApp changes.
