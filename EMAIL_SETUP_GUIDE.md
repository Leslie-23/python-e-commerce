# Gmail SMTP Setup Guide for OTP Email Delivery

## Current Status

✅ **SMTP is already configured** in your `.env` file!

- Gmail SMTP server: `smtp.gmail.com:587`
- Current email: `seunpau1003@gmail.com`
- App password is already set

## To Use Your Own Email (Optional)

If you want to use `codexcoder082@gmail.com` to send OTPs, follow these steps:

### 1. Enable 2-Factor Authentication

- Go to [Google Account Security](https://myaccount.google.com/security)
- Enable 2-Factor Authentication if not already enabled

### 2. Generate App Password

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Click "2-Step Verification"
3. Scroll down to "App passwords"
4. Select "Mail" and "Other (custom name)"
5. Enter "E-commerce OTP App"
6. Copy the 16-character password (like: `abcd efgh ijkl mnop`)

### 3. Update .env File

Edit `flask_backend/.env` and replace:

```env
EMAIL_USER=codexcoder082@gmail.com
EMAIL_PASS=your-16-character-app-password
```

## Test Email Delivery

Run this test to check if emails are being sent:

```bash
cd flask_backend
python -c "
from app.utils.emails import send_mail
result = send_mail('codexcoder082@gmail.com', 'Test Email', '<h1>Test successful!</h1>')
print('Email sent successfully!' if result else 'Email failed!')
"
```

## Current Configuration

Your current setup should already work with the existing email (`seunpau1003@gmail.com`).

**Ready to test OTP emails right now!** 🚀

The system will:

1. ✅ Generate OTP and save to database
2. ✅ Print OTP to console (backup)
3. ✅ Send HTML email with OTP to user
4. ✅ Email expires in 10 minutes

## Frontend Integration

The frontend OTP component (`OtpVerfication.jsx`) is already set up to:

- ✅ Show email where OTP was sent
- ✅ Accept 4-digit OTP input
- ✅ Verify OTP with backend
- ✅ Handle success/error states
- ✅ Allow OTP resend

**Everything is ready for production email delivery!** 📧
