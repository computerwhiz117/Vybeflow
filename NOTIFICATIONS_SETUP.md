# VybeFlow Email & SMS Notifications Setup Guide

## ✅ Implementation Complete!

Your VybeFlow app now sends both **email** and **SMS** notifications when users sign up.

---

## 📧 Email Setup (Gmail Example)

### Step 1: Enable App Password for Gmail
1. Go to your Google Account: https://myaccount.google.com
2. Select **Security** → **2-Step Verification** (enable if not already)
3. Search for **App passwords** or visit: https://myaccount.google.com/apppasswords
4. Create a new app password for "Mail"
5. Copy the 16-character password

### Step 2: Configure Environment Variables
Create a `.env` file in your project root:
```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-char-app-password
MAIL_DEFAULT_SENDER=noreply@vybeflow.com
```

**Alternative Email Providers:**
- **Outlook/Hotmail**: smtp-mail.outlook.com (Port 587)
- **Yahoo**: smtp.mail.yahoo.com (Port 587)
- **SendGrid**: smtp.sendgrid.net (Port 587)

---

## 📱 SMS Setup (Twilio)

### Step 1: Sign Up for Twilio
1. Visit: https://www.twilio.com/try-twilio
2. Sign up for a free account (includes $15 credit)
3. Verify your email and phone number

### Step 2: Get Your Credentials
1. Go to Twilio Console: https://console.twilio.com
2. Copy your **Account SID** and **Auth Token**
3. Get a phone number:
   - Click "Get a Twilio phone number"
   - Accept the number provided (or choose a specific one)

### Step 3: Add to Environment Variables
Add these to your `.env` file:
```bash
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+15551234567
```

**Note:** For testing, Twilio free tier only allows sending to verified numbers.

---

## 🚀 How to Use

### Option 1: Load from .env file (Recommended)
Update your `app.py` to load environment variables:

```python
from dotenv import load_dotenv
load_dotenv()  # Add this at the top
```

### Option 2: Set Environment Variables Directly (Windows PowerShell)
```powershell
$env:MAIL_USERNAME="your-email@gmail.com"
$env:MAIL_PASSWORD="your-app-password"
$env:TWILIO_ACCOUNT_SID="your-sid"
$env:TWILIO_AUTH_TOKEN="your-token"
$env:TWILIO_PHONE_NUMBER="+15551234567"
```

---

## 🧪 Testing

### Test Email Only
```python
python -c "from notifications import send_welcome_email; send_welcome_email('test@example.com', 'TestUser')"
```

### Test SMS Only
```python
python -c "from notifications import send_welcome_sms; send_welcome_sms('+15551234567', 'TestUser')"
```

### Test Full Signup Flow
1. Start your Flask app: `python app.py`
2. Go to: http://127.0.0.1:5000/signup
3. Fill out the form with:
   - Valid email address
   - Phone number (with country code)
4. Check your email and phone for notifications!

---

## 📝 What Happens Now

When a user signs up:
1. ✅ Account is created in the database
2. 📧 Welcome email is sent with account details
3. 📱 Welcome SMS is sent (if phone number provided)
4. 💬 Flash message confirms notifications were sent

---

## ⚠️ Graceful Degradation

If email/SMS credentials are not configured:
- The app **will still work**
- Account creation succeeds
- Only on-screen flash messages are shown
- No errors are thrown

---

## 🔒 Security Notes

1. **Never commit .env files** to version control
2. Add `.env` to your `.gitignore` file
3. Use different credentials for production
4. Rotate your API keys regularly

---

## 📊 Cost Information

### Email (Gmail)
- **Free** for personal use
- Limit: 500 emails/day

### SMS (Twilio)
- **Free trial**: $15 credit
- Cost: ~$0.0075 per SMS (US)
- ~2000 SMS with trial credit

---

## 🎉 You're All Set!

Your VybeFlow app now has professional email and SMS notifications!
