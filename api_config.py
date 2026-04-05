# WhatsApp Bot API Configuration
# For GitHub Actions Cloud Version

# IMPORTANT: Don't hardcode credentials here!
# Set these as environment variables or GitHub Secrets:
# - ULTRAMSG_TOKEN
# - ULTRAMSG_INSTANCE

import os

# Load from environment variables (set by GitHub Actions or local .env file)
ULTRAMSG_TOKEN = os.environ.get("ULTRAMSG_TOKEN", "")
ULTRAMSG_INSTANCE = os.environ.get("ULTRAMSG_INSTANCE", "")

# Flag to enable/disable UltraMsg
ULTRAMSG_ENABLED = True
USE_ULTRAMSG = True
