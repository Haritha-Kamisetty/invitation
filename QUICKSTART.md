# 🚀 Quick Start Guide

## Get Started in 3 Minutes!

### Step 1: Install Dependencies (1 minute)
```bash
cd "c:\Users\Suneel Reddy\Downloads\invitation web"
pip install -r requirements.txt
```

### Step 2: Run the Application (30 seconds)
```bash
python run.py
```

### Step 3: Open in Browser
Go to: **http://localhost:5000**

---

## ✨ What You Can Do Now

### Without Email Setup:
- ✅ Create beautiful invitations
- ✅ Customize templates
- ✅ Collect RSVPs with dietary restrictions
- ✅ View interactive maps
- ✅ Import/export guests (CSV/Excel)
- ✅ Generate QR codes
- ✅ Track statistics

### With Email Setup (Optional - 5 minutes):
1. Copy `.env.example` to `.env`
2. Add your Gmail and App Password
3. Send professional email invitations!

**Gmail App Password Setup:**
1. Go to https://myaccount.google.com/apppasswords
2. Generate new app password
3. Copy to `.env` file

---

## 📖 Quick Tutorial

### Create Your First Event:

1. **Sign Up**
   - Click "Sign Up" 
   - Enter your details
   - Login

2. **Choose Template**
   - Browse birthday, wedding, anniversary, or baby shower templates
   - Click on your favorite

3. **Customize**
   - Add event details
   - Type venue name (autocomplete will help!)
   - Add personal message
   - Preview in real-time

4. **Add Guests**
   - Add manually, OR
   - Import from `sample_guests.csv`

5. **Send Invitations**
   - Share link directly, OR
   - Send email invitations (if configured), OR
   - Download QR code to share

6. **Track Responses**
   - View dashboard
   - See who's coming
   - Check dietary restrictions
   - Export guest list

---

## 🎯 Key Features

| Feature | How to Use |
|---------|------------|
| **Import Guests** | Dashboard → Import → Select CSV |
| **Export Guests** | Dashboard → Export → Choose format |
| **Send Emails** | Dashboard → Send Invitations |
| **Generate QR Code** | API: `/api/events/<id>/qrcode` |
| **Venue Search** | Type in venue field (auto-suggests) |
| **Dietary Tracking** | Guests fill during RSVP |

---

## 📧 Email Setup (Optional)

### Gmail (Free - Recommended for Testing)
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-char-app-password
```

### SendGrid (Free - Recommended for Production)
```env
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=apikey
MAIL_PASSWORD=your-sendgrid-api-key
```

---

## 🐛 Common Issues

**Port already in use?**
```bash
# Change port in run.py or use:
python run.py --port 5001
```

**Dependencies not installing?**
```bash
# Upgrade pip first:
python -m pip install --upgrade pip
# Then retry:
pip install -r requirements.txt
```

**Email not working?**
- Check `.env` file exists
- Use App Password (not regular password) for Gmail
- Check spam folder

---

## 📚 Learn More

- **Full Documentation**: See `README.md`
- **API Reference**: See `walkthrough.md`
- **Sample Data**: Use `sample_guests.csv`

---

## 🎉 You're Ready!

Your professional invitation platform is ready to use. Start creating beautiful invitations!

**Need Help?**
- Check `README.md` for detailed documentation
- See `walkthrough.md` for implementation details
- Review code comments for technical details

---

**Made with ❤️ - Enjoy creating memorable events!**
