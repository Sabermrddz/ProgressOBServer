# WebEtu Grades Monitor Bot - DigitalOcean Deployment Guide

This guide explains how to deploy the WebEtu Grades Monitor Bot on DigitalOcean App Platform.

## Prerequisites

- DigitalOcean Account (with App Platform enabled)
- GitHub Account (to store your repository)
- Telegram Bot Token (from BotFather)
- WebEtu Credentials (username & password)

## Deployment Steps

### 1. Prepare Your Repository

```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit - ready for deployment"
git push -u origin main
```

### 2. Create GitHub Repository

1. Go to github.com and create a new repository
2. Push your local code to GitHub:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/ProgressOBSe.git
   git push -u origin main
   ```

### 3. Deploy on DigitalOcean App Platform

1. Go to [DigitalOcean Console](https://cloud.digitalocean.com)
2. Click **Create** → **App**
3. Choose **GitHub** as source
4. Select your **ProgressOBSe** repository
5. DigitalOcean will auto-detect the Docker configuration
6. In the **Environment Variables** section, add:

   ```
   WEBETU_USERNAME=YOUR_USERNAME
   WEBETU_PASSWORD=YOUR_PASSWORD
   DIA_ID=YOUR_DIA_ID
   IND_ID=YOUR_IND_ID
   TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN
   TELEGRAM_CHAT_ID=YOUR_CHAT_ID
   CHECK_INTERVAL_MINUTES=15
   LOG_LEVEL=INFO
   ```

7. Click **Review** and then **Create App**

### 4. Verify Persistent Storage

The bot requires persistent storage for:
- `grades.json` - Stores grade history
- `token.json` - Stores JWT tokens
- `webetu_bot.log` - Application logs

DigitalOcean App Platform automatically creates a 1GB volume mounted at `/app/data`.

### 5. Monitor the Deployment

1. Go to your App → **Deployment** tab
2. Watch the build progress
3. Once deployed, check **Runtime Logs** to see if the bot started successfully
4. You should see messages like:
   ```
   ✅ WebEtu authentication successful
   ✅ Telegram connection successful
   🚀 Starting scheduler...
   ```

## What Happens After Deployment

Once deployed, the bot will:

1. **Authenticate** with WebEtu API every time it runs
2. **Check for new grades** every 15 minutes
3. **Send notifications** to your Telegram chat when new grades appear
4. **Store grade history** in persistent volume
5. **Auto-restart** if it crashes

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `WEBETU_USERNAME` | Your university login | `202335040314` |
| `WEBETU_PASSWORD` | Your university password | `example_password` |
| `DIA_ID` | Student DIA ID | `39608221` |
| `IND_ID` | Student Individual ID | `38669075` |
| `TELEGRAM_BOT_TOKEN` | Bot token from BotFather | `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID | `5014464093` |
| `CHECK_INTERVAL_MINUTES` | Grade check frequency | `15` |
| `LOG_LEVEL` | Logging level (INFO/DEBUG) | `INFO` |

## Troubleshooting

### Bot Not Sending Notifications

1. Check **Runtime Logs** for errors
2. Verify Telegram chat ID is correct
3. Ensure bot token is valid
4. Check WebEtu credentials are correct

### High Resource Usage

If the app uses too much memory/CPU:
1. Increase CHECK_INTERVAL_MINUTES (check grades less often)
2. Set LOG_LEVEL to INFO (less verbose logging)

### Authentication Failures

1. Verify WebEtu credentials are correct
2. Check if account has API access enabled
3. Verify DIA_ID and IND_ID are correct

## Scaling

For production use:
- Consider increasing resource allocation in app.yaml
- Monitor logs regularly
- Set up DigitalOcean monitoring alerts
- Enable auto-scaling if needed

## Updates

To update the bot:
1. Make changes locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update: description"
   git push
   ```
3. DigitalOcean will auto-deploy the changes

## Local Testing with Docker

Before deploying, test locally:

```bash
# Create .env file with your credentials
cp .env.example .env
# Edit .env with your values

# Build and run with docker-compose
docker-compose up --build

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## Support

For issues:
- Check `/app/data/webetu_bot.log` in DigitalOcean console
- Review WebEtu API documentation
- Verify Telegram Bot API credentials
- Check DigitalOcean App logs

## License

This project is for personal educational use only.
