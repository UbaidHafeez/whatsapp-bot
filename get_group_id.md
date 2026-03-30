# How to Get WhatsApp Group ID for UltraMsg API

## The Problem

UltraMsg API needs the **actual Group ID** (JID), not the group name.

**Format:**
- ❌ Wrong: `Family`
- ✅ Correct: `123456789-123456@g.us` or `923001234567@s.whatsapp.net`

---

## Method 1: Get Group ID from UltraMsg Dashboard (Easiest)

1. Go to: https://ultramsg.com
2. Login to your account
3. Click on your instance: `instance167704`
4. Look for **"Groups"** or **"Chats"** tab
5. Find your "Family" group
6. Copy the **Group ID** (looks like: `123456789-123456@g.us`)
7. Update `groups.txt` with this ID

---

## Method 2: Send to Your Phone First (Test)

To test if the API is working, send to your phone number first:

1. Edit `groups.txt`
2. Replace `Family` with your phone number:
   ```
   923001234567
   ```
   (Use your actual Pakistan phone number, format: 923XXXXXXXXX)

3. Save the file
4. Run: `python whatsapp_api_sender.py --now`
5. If it works, you'll receive the images on your personal WhatsApp

---

## Method 3: Get Group ID from WhatsApp

### On Android:
1. Open WhatsApp
2. Go to "Family" group
3. Tap on group name at top
4. Scroll down to "Group info"
5. Look for "Group ID" or "Invite via link"
6. The ID is in the link: `https://chat.whatsapp.com/ABC123...`
   - The part after `/invite/` is the invite code
   - You need the actual JID which UltraMsg can show

### Better: Check UltraMsg Dashboard
1. Go to UltraMsg dashboard
2. Click your instance
3. Look for "Groups" section
4. You'll see all groups you're in with their IDs

---

## Update Your groups.txt

Once you have the Group ID, edit `groups.txt`:

**Before:**
```
Family
```

**After:**
```
123456789-123456@g.us
```

Or if sending to phone:
```
923001234567
```

---

## Quick Test Now

To test the API right now with your phone:

1. Open Notepad
2. Open: `d:\WORK\whats group upload\groups.txt`
3. Replace `Family` with your phone number: `923XXXXXXXXX`
4. Save
5. Run: `python whatsapp_api_sender.py --now`

If successful, you'll get the images on your personal WhatsApp!

---

## Then Add Group Later

After testing with your phone:
1. Go to UltraMsg dashboard
2. Find the Group ID for "Family"
3. Update `groups.txt` with the Group ID
4. Run again

---

## Example groups.txt Formats

```
# Personal (phone number)
923001234567

# Group (Group ID)
123456789-123456@g.us

# Multiple recipients
923001234567
923111234567
123456789-123456@g.us
```

---

**Need help?** Check your UltraMsg dashboard at https://ultramsg.com for the exact Group ID format!
