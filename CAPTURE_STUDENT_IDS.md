# Capturing Student Identifiers with HTTP Toolkit

This guide shows how to capture your **DIA_ID** and **IND_ID** from the WebEtu API using HTTP Toolkit.

## What Are These IDs?

- **DIA_ID**: Your student DIA identifier (12-15 digits)
- **IND_ID**: Your individual student ID (8 digits)

You need these to fetch your grades. They're returned by the WebEtu authentication API.

## Method 1: Using HTTP Toolkit (Recommended)

### Step 1: Download & Install HTTP Toolkit
- Go to https://httptoolkit.tech/
- Download for your platform (Windows/Mac/Linux)
- Install and open the application

### Step 2: Configure Your Phone/Emulator
- Open HTTP Toolkit
- Click **"Intercept traffic"**
- Choose your platform:
  - **Phone**: Take screenshot of QR code → scan on your phone
  - **Android Emulator**: Select your emulator from list
- HTTP Toolkit will intercept all requests

### Step 3: Log in to WebEtu
- Open browser on phone or emulator
- Go to https://webetu.mesrs.dz
- Enter credentials:
  - Username: Your student ID (e.g., `202335040314`)
  - Password: Your password
- Click Login

### Step 4: Capture Login Response
In HTTP Toolkit sidebar, look for request to:
```
POST /api/auth/login
```

Click on this request → View **Response** tab

You'll see JSON like:
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "dia": "12756153",
    "ind": "38669075",
    "name": "Your Name",
    ...
  }
}
```

**Copy these values:**
- `"dia"` = Your **DIA_ID** → `12756153`
- `"ind"` = Your **IND_ID** → `38669075`

### Step 5: Add to .env File
Edit your `.env` file:
```
WEBETU_USERNAME=202335040314
WEBETU_PASSWORD=your_password
DIA_ID=12756153
IND_ID=38669075
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
CHECK_INTERVAL_MINUTES=15
LOG_LEVEL=INFO
```

## Method 2: Using Android Emulator

### Setup Android Emulator
1. Download Android Studio (includes emulator)
2. Create Virtual Device (Android 10+)
3. Start emulator
4. Use Method 1 above, selecting your emulator in HTTP Toolkit

## Method 3: Using iPhone Simulator with Proxy

1. Open iPhone Simulator in Xcode
2. Go to Settings → Wifi → Configure Proxy
3. Enter your computer's IP address and HTTP Toolkit proxy port
4. Follow Steps 3-5 above

## Quick Check

To verify your IDs are correct, run:
```bash
python main.py
```

If you see in logs:
```
✅ Fetched 14 exam grades
✅ Fetched 20 continuous grades
```

Your IDs are correct! ✅

## Troubleshooting

### "Invalid or expired JWT" Error
- Your DIA_ID or IND_ID might be wrong
- Check HTTP Toolkit response again
- Verify both IDs match exactly

### "401 Unauthorized"
- Credentials are wrong
- Try logging in manually on WebEtu portal first
- Capture new credentials with HTTP Toolkit

### Can't intercept requests
- Restart HTTP Toolkit
- Restart phone/emulator
- Clear browser cache
- Try Method 2 (Android Emulator) instead

## Security Notes

⚠️ Never share your credentials or IDs publicly
⚠️ Keep HTTP Toolkit output private
⚠️ Delete HTTP Toolkit logs after capturing IDs
✅ Once you have IDs, you only need them in `.env` (don't share .env file)

---

**Done?** Now run your bot with the correct IDs:
```bash
python main.py
```

Enjoy automated grade notifications! 🎓📱
