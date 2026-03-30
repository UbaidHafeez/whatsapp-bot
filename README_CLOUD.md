# ☁️ WhatsApp Islamic Post Bot - Cloud Edition

**Automatically sends Islamic posts to WhatsApp groups every day at 7 PM**

✅ **100% FREE** | ✅ **Runs in Cloud** | ✅ **Computer can be OFF** | ✅ **Fully Automatic**

---

## 🚀 Quick Start

### **Setup (10 minutes):**

1. **Clone/Upload** this repository to GitHub
2. **Add Secrets** (Settings → Secrets and variables → Actions):
   - `ULTRAMSG_TOKEN` = Your UltraMsg token
   - `ULTRAMSG_INSTANCE` = Your UltraMsg instance ID
3. **Go to Actions** tab → Enable workflows
4. **Test** → Click "Run workflow"

### **It's Done!** ☁️

Bot runs automatically every day at **7:00 PM PKT**.

---

## 📁 How It Works

```
Every day at 7 PM ↓
GitHub Actions triggers ↓
Runs whatsapp_bot_cloud.py ↓
Sends images to all groups ↓
Renames folder to sent_ ↓
Done!
```

---

## 📱 Add New Posts

1. Create folder: `islamic_posts/post_008/image.jpg`
2. Upload to repository
3. Bot sends it automatically at next 7 PM!

---

## 📋 Files

- `whatsapp_bot_cloud.py` - Main bot
- `.github/workflows/whatsapp_bot.yml` - Scheduler (7 PM daily)
- `groups.txt` - Your WhatsApp groups/numbers
- `islamic_posts/` - Your Islamic post images

---

## ⚙️ Configuration

### **Change Time:**

Edit `.github/workflows/whatsapp_bot.yml`:

```yaml
# 7 PM PKT = 14:00 UTC
- cron: '0 14 * * *'

# For 8 PM PKT = 15:00 UTC
- cron: '0 15 * * *'
```

### **Add Groups:**

Edit `groups.txt` (one per line):
```
923140839915
123456789-123456@g.us
```

---

## 💰 Cost

**100% FREE!**

- GitHub Actions: Free 2000 minutes/month
- UltraMsg: Free 100 messages/day
- Your usage: ~30 minutes + ~20 messages/month

---

## 📊 Monitor

1. Go to **Actions** tab
2. See all runs
3. Click to view logs
4. Check if sent successfully

---

## 🔧 Get UltraMsg Credentials

1. Go to: https://ultramsg.com
2. Sign up (free)
3. Create instance
4. Scan QR code
5. Copy token and instance ID
6. Add to GitHub Secrets

---

## 📞 Support

- **Setup Guide:** See `CLOUD_SETUP.md`
- **Logs:** Check Actions tab in GitHub
- **Issues:** Check `bot_log.txt` after run

---

## ✨ Features

- ✅ Automatic daily sending at 7 PM
- ✅ Runs in GitHub cloud (computer OFF ok)
- ✅ Send to multiple groups
- ✅ No captions (clean images)
- ✅ Auto-rename sent folders
- ✅ Free forever

---

## 🎯 Example Usage

**Before 7 PM:**
```
islamic_posts/
├── post_001/
│   ├── urdu.jpg
│   └── eng.jpg
└── post_002/
    ├── urdu.jpg
    └── eng.jpg
```

**After 7 PM:**
```
islamic_posts/
├── sent_post_001/  ✅ Sent
└── sent_post_002/  ✅ Sent
```

---

## 🌟 Made for Islamic Content Sharing

Share Islamic reminders, Quran verses, and Hadith automatically to your WhatsApp groups every day!

---

**License:** MIT | **Cost:** FREE | **Status:** ✅ Working
