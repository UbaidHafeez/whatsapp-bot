# 🚀 UPLOAD TO GITHUB - SIMPLE GUIDE

## ✅ **All Files Ready in This Folder!**

Just upload this entire folder to GitHub!

---

## 📋 **Step-by-Step (5 Minutes)**

### **Step 1: Create GitHub Account**

1. Go to: https://github.com
2. Click **"Sign up"** (top right)
3. Create free account
4. Verify email

---

### **Step 2: Create New Repository**

1. After login, click **"+"** (top right)
2. Click **"New repository"**
3. Repository name: `whatsapp-bot`
4. Select **"Public"** or **"Private"**
5. Click **"Create repository"**

---

### **Step 3: Upload All Files**

1. On the repository page, click **"uploading an existing file"**
2. **Select ALL files** from this `GITHUB_UPLOAD` folder:
   - ✅ `whatsapp_bot_cloud.py`
   - ✅ `api_config.py`
   - ✅ `groups.txt`
   - ✅ `posts_db.json`
   - ✅ `requirements.txt`
   - ✅ `bot_log.txt`
   - ✅ `.gitignore`
   - ✅ `.github` folder (with workflows inside)
   - ✅ `islamic_posts` folder (with your images)
3. Drag all files to the upload box
4. Click **"Commit changes"**

---

### **Step 4: Add API Secrets**

1. In your repository, go to: **Settings** (top menu)
2. Click **"Secrets and variables"** → **"Actions"**
3. Click **"New repository secret"**

**Add Secret 1:**
- Name: `ULTRAMSG_TOKEN`
- Value: `pak8408yn0osmffv`
- Click **"Add secret"**

**Add Secret 2:**
- Name: `ULTRAMSG_INSTANCE`
- Value: `instance167704`
- Click **"Add secret"**

---

### **Step 5: Enable Actions**

1. Click **"Actions"** tab (top menu)
2. If you see a warning, click **"I understand my workflows, go ahead and enable them"**

---

### **Step 6: Test the Bot**

1. In **Actions** tab, click **"WhatsApp Islamic Post Sender"**
2. Click **"Run workflow"** (dropdown button)
3. Click **"Run workflow"** again
4. Wait 1-2 minutes
5. Check your WhatsApp phone - you should receive images! ✅

---

## ⏰ **Automatic Schedule**

The bot is configured to run:
- **Every day at 7:00 PM Pakistan time**
- Automatically, no commands needed
- Your computer can be OFF!

---

## 📱 **Add More Posts**

1. Create folder with images:
   ```
   islamic_posts/
   └── post_007/
       ├── image1.jpg
       └── image2.jpg
   ```

2. Upload to GitHub:
   - Go to your repository
   - Click **"Add file"** → **"Upload files"**
   - Upload the folder
   - Click **"Commit changes"**

3. Bot will send at next 7 PM automatically!

---

## 📊 **Check If It's Working**

1. Go to **"Actions"** tab
2. See the workflow runs
3. Green checkmark = ✅ Success
4. Red X = ❌ Failed (click to see error)

---

## 🔧 **Change Time**

Want different time than 7 PM?

1. Open: `.github/workflows/whatsapp_bot.yml`
2. Find this line:
   ```yaml
   - cron: '0 14 * * *'
   ```
3. Change `14` to your time (UTC):
   - 7 PM PKT = 14:00 UTC
   - 8 PM PKT = 15:00 UTC
   - 9 PM PKT = 16:00 UTC
4. Click **"Commit changes"**

---

## ✅ **Setup Complete Checklist**

- [ ] Created GitHub account
- [ ] Created repository named `whatsapp-bot`
- [ ] Uploaded ALL files from this folder
- [ ] Added `ULTRAMSG_TOKEN` secret
- [ ] Added `ULTRAMSG_INSTANCE` secret
- [ ] Enabled Actions
- [ ] Tested with "Run workflow"
- [ ] Received images on WhatsApp

---

## 🎉 **Done!**

Your bot now runs **automatically every day at 7 PM**!

**Computer can be OFF** - it runs in GitHub cloud! ☁️

---

## 💰 **Cost: $0**

- GitHub Actions: FREE (you use ~30 min out of 2000)
- UltraMsg API: FREE (you use ~20 msg out of 100/day)
- **Total: 100% FREE forever!**

---

## 📞 **Need Help?**

- Check **Actions** tab for logs
- Check **Settings** → **Secrets** for credentials
- Check `bot_log.txt` for errors

---

**Permanent cloud solution complete!** ☁️✅
