# ☁️ Cloud Setup Guide - GitHub Actions (FREE)

## 🎯 **Permanent Solution - Runs Automatically at 7 PM Daily**

**Your computer can be OFF** - bot runs in GitHub cloud!

---

## 📋 **Step-by-Step Setup (10 Minutes)**

### **Step 1: Create GitHub Repository**

1. Go to: https://github.com
2. Login (or create free account)
3. Click **"+"** (top right) → **"New repository"**
4. Name: `whatsapp-bot`
5. Select **"Public"** or **"Private"**
6. Click **"Create repository"**

---

### **Step 2: Upload Your Files**

1. In your new repository, click **"uploading an existing file"**
2. Upload these files:
   ```
   ✓ whatsapp_bot_cloud.py
   ✓ api_config.py
   ✓ groups.txt
   ✓ islamic_posts/ (folder with your images)
   ✓ posts_db.json
   ✓ requirements.txt
   ```
3. Click **"Commit changes"**

---

### **Step 3: Add GitHub Actions Workflow**

1. In your repository, click **"Actions"** tab (top menu)
2. Click **"set up a workflow yourself"**
3. Copy the content from `.github/workflows/whatsapp_bot.yml`
4. Paste into the editor
5. Click **"Commit changes"**

---

### **Step 4: Add API Secrets**

1. In your repository, go to: **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"**
3. Add these secrets:

**Secret 1:**
- Name: `ULTRAMSG_TOKEN`
- Value: `pak8408yn0osmffv`
- Click **"Add secret"**

**Secret 2:**
- Name: `ULTRAMSG_INSTANCE`
- Value: `instance167704`
- Click **"Add secret"**

---

### **Step 5: Test the Bot**

1. Go to **"Actions"** tab
2. Click on **"WhatsApp Islamic Post Sender"** workflow
3. Click **"Run workflow"** (dropdown) → **"Run workflow"**
4. Wait 1-2 minutes
5. Check your WhatsApp - you should receive the images!

---

### **Step 6: Verify Schedule**

The bot is scheduled to run at **7:00 PM PKT daily** (14:00 UTC).

To verify:
1. Go to **"Actions"** tab
2. You'll see the workflow file
3. It shows: `schedule: - cron: '0 14 * * *'`
4. This means: **Every day at 14:00 UTC = 7:00 PM Pakistan time**

---

## ✅ **What Happens Now**

- ✅ **Every day at 7 PM** - Bot runs automatically
- ✅ **Your computer can be OFF** - runs in GitHub cloud
- ✅ **Sends to all groups** in `groups.txt`
- ✅ **Auto-rename folders** to `sent_`
- ✅ **Free 2000 minutes/month** (you use ~30 minutes)

---

## 📱 **Add New Posts**

When you want to add new Islamic posts:

1. Create folder in `islamic_posts/`:
   ```
   islamic_posts/
   └── post_008/
       ├── image1.jpg
       └── image2.jpg
   ```

2. Commit to GitHub:
   - Go to your repository
   - Click **"Add file"** → **"Upload files"**
   - Upload the new folder
   - Click **"Commit changes"**

3. Bot will send it automatically at next 7 PM!

---

## 📊 **Monitor Your Bot**

1. Go to **"Actions"** tab
2. See all runs (successful/failed)
3. Click on any run to see logs
4. Check if images were sent

---

## 🔧 **Update Groups**

To add/remove groups:

1. Edit `groups.txt` in your repository
2. Add one number/Group ID per line
3. Commit changes
4. Bot will use updated list at next run

---

## 💰 **Cost: 100% FREE**

- GitHub Actions: **Free 2000 minutes/month**
- Your usage: **~30 minutes/month** (1-2 minutes per run × 30 days)
- **Remaining: 1970 minutes FREE!**

---

## ⚙️ **Change Schedule Time**

To run at different time:

1. Go to repository
2. Edit `.github/workflows/whatsapp_bot.yml`
3. Change the cron time:
   ```yaml
   # Current: 7 PM PKT (14:00 UTC)
   - cron: '0 14 * * *'
   
   # For 8 PM PKT (15:00 UTC):
   - cron: '0 15 * * *'
   ```
4. Commit changes

---

## 🎯 **Cron Time Converter**

| Pakistan Time | UTC Time | Cron |
|---------------|----------|------|
| 7:00 PM | 14:00 | `0 14 * * *` |
| 8:00 PM | 15:00 | `0 15 * * *` |
| 9:00 PM | 16:00 | `0 16 * * *` |

---

## ✅ **Setup Checklist**

- [ ] Created GitHub account
- [ ] Created repository
- [ ] Uploaded all files
- [ ] Added workflow file
- [ ] Added ULTRAMSG_TOKEN secret
- [ ] Added ULTRAMSG_INSTANCE secret
- [ ] Tested with manual run
- [ ] Verified schedule is set

---

## 🎉 **Done!**

Your bot now runs **automatically every day at 7 PM** in the cloud!

**Your computer can be OFF** - it doesn't matter!

---

## 📞 **Need Help?**

- Check **Actions** tab for logs
- Check **Settings** → **Secrets** for credentials
- Check `bot_log.txt` in repository for errors

---

**Permanent cloud solution complete!** ☁️✅
