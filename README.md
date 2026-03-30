# 🚀 WhatsApp Islamic Post Sender - AUTO with AI OCR

## ✅ **Fully Automatic - AI-Powered**

---

## 🎯 **Features**

✅ **AI OCR Detection** - Auto-detect Urdu & English images  
✅ **Send to multiple groups/numbers**  
✅ **NO caption** (just clean images)  
✅ **Auto-rename folder** to "sent_" after sending  
✅ **Auto-send next unsent post**  
✅ **Daily scheduler at 7:00 PM**  

---

## 📋 **How It Works**

### **Agent Tasks:**

1. ✅ **Check folder** for images
2. ✅ **AI OCR Analysis** - Detect which is Urdu and which is English
3. ✅ **Auto-rename** images to `urdu.jpg` and `eng.jpg`
4. ✅ **Send both images** to ALL groups (NO caption)
5. ✅ **Rename folder** to `sent_postname`
6. ✅ **Check for next post** and send automatically
7. ✅ **Run daily at 7 PM**

---

## 📁 **Setup**

### **Step 1: Add Your Images**

Just drop 2 images in a folder:

```
islamic_posts/
└── post_001/
    ├── image1.jpg  ← Any name (AI will detect)
    └── image2.jpg  ← Any name (AI will detect)
```

**The AI will automatically:**
- Detect which is Urdu
- Detect which is English
- Rename them correctly
- Send both

---

### **Step 2: Add Recipients**

Edit `groups.txt` - add one per line:

```
923140839915
123456789-123456@g.us
```

---

### **Step 3: Run**

**Send now:**
```bash
python whatsapp_api_sender.py --now
```

**Start scheduler (7 PM daily):**
```bash
python whatsapp_api_sender.py
```

---

## 🤖 **AI OCR Detection**

The bot uses **EasyOCR** AI to detect languages:

- **Urdu text** → Arabic script characters
- **English text** → Latin script characters

**First time:** Downloads AI models (~200MB)  
**Next times:** Instant detection!

---

## 🔄 **Automatic Workflow**

```
1. Scan islamic_posts/ folder
   ↓
2. Find unsent post
   ↓
3. AI OCR detects Urdu/English
   ↓
4. Send both images (NO caption)
   ↓
5. Rename folder to sent_
   ↓
6. Check for next post → Repeat
   ↓
7. Wait for tomorrow 7 PM
```

---

## 💰 **Cost: FREE**

- UltraMsg free tier: 100 messages/day
- Your usage: 2 messages × groups
- **Example:** 10 groups = 20 messages = Still FREE!

---

## 📱 **Get Group ID**

1. Go to: https://ultramsg.com
2. Login → Click `instance167704`
3. Click **"Groups"** tab
4. Copy Group ID (format: `xxx-xxx@g.us`)
5. Add to `groups.txt`

---

## 🛑 **Stop Scheduler**

Press **Ctrl+C** in command prompt

---

## 📁 **Files**

- `whatsapp_api_sender.py` - Bot with AI OCR & scheduler
- `api_config.py` - Your credentials (configured)
- `groups.txt` - Recipients list
- `islamic_posts/` - Your images (AI will sort)

---

**That's it!** AI handles everything! 🎉
