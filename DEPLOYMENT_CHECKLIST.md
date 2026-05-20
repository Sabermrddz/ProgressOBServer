# Deployment Checklist ✅

Complete this checklist before deploying to DigitalOcean App Platform.

## Phase 1: Pre-Deployment Verification

### Local Testing
- [ ] Virtual environment created: `python -m venv venv`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Bot runs successfully: `python main.py`
- [ ] Grades fetched successfully (check logs for "✅ Fetched")
- [ ] Telegram notifications work (should send test message on start)
- [ ] Logs show schedule running every 15 minutes

### Configuration Review
- [ ] `.env` file contains all required variables:
  - [ ] WEBETU_USERNAME (your student ID)
  - [ ] WEBETU_PASSWORD (your password)
  - [ ] DIA_ID (student identifier from WebEtu)
  - [ ] IND_ID (student identifier from WebEtu)
  - [ ] TELEGRAM_BOT_TOKEN (from BotFather)
  - [ ] TELEGRAM_CHAT_ID (your personal chat ID)
  - [ ] CHECK_INTERVAL_MINUTES=15
  - [ ] LOG_LEVEL=INFO (or DEBUG for troubleshooting)
- [ ] `.env` is NOT committed to git (added to .gitignore)
- [ ] `.env.example` has placeholder values only

### Docker Verification
- [ ] Docker is installed: `docker --version`
- [ ] Docker Compose is installed: `docker-compose --version`
- [ ] Local Docker test passes: `docker-compose up --build`
- [ ] Container starts successfully
- [ ] Logs show bot initializing
- [ ] Container stops cleanly: `docker-compose down`

## Phase 2: GitHub Repository Setup

### Repository Creation
- [ ] Created GitHub repository: `ProgressOBSe`
- [ ] Repository is private (avoid exposing credentials)
- [ ] Cloned locally or initialized git

### Files Committed to Git
- [ ] ✅ `main.py`
- [ ] ✅ `bot.py`
- [ ] ✅ `api.py`
- [ ] ✅ `config.py`
- [ ] ✅ `storage.py`
- [ ] ✅ `requirements.txt`
- [ ] ✅ `Dockerfile`
- [ ] ✅ `docker-compose.yml`
- [ ] ✅ `app.yaml`
- [ ] ✅ `runtime.txt`
- [ ] ✅ `.dockerignore`
- [ ] ✅ `README.md`
- [ ] ✅ `DIGITALOCEAN_DEPLOYMENT.md`
- [ ] ✅ `.gitignore`
- [ ] ✅ `.env.example` (with placeholder values only)

### Files NOT Committed to Git
- [ ] ❌ `.env` (actual credentials - blocked by .gitignore)
- [ ] ❌ `data/` directory (auto-generated)
- [ ] ❌ `grades.json` (auto-generated)
- [ ] ❌ `token.json` (auto-generated)
- [ ] ❌ `webetu_bot.log` (auto-generated)
- [ ] ❌ `venv/` (virtual environment - blocked by .gitignore)
- [ ] ❌ `__pycache__/` (Python cache - blocked by .gitignore)

### Git Operations
- [ ] Initialized git: `git init`
- [ ] Added all files: `git add .`
- [ ] Created initial commit: `git commit -m "Initial commit"`
- [ ] Added remote: `git remote add origin https://github.com/YOUR_USERNAME/ProgressOBSe.git`
- [ ] Pushed to GitHub: `git push -u origin main`
- [ ] Verified files on GitHub (exclude .env!)

## Phase 3: DigitalOcean Account Setup

### Account & Permissions
- [ ] DigitalOcean account created
- [ ] App Platform available in account
- [ ] GitHub connected to DigitalOcean
- [ ] Authorization granted (repository access)

### Create App
- [ ] Navigated to DigitalOcean Console
- [ ] Clicked "Create" → "App"
- [ ] Selected "GitHub" as source
- [ ] Selected "ProgressOBSe" repository
- [ ] App name: `webetu-bot` (or preferred name)
- [ ] DigitalOcean detected Docker configuration ✅

## Phase 4: Environment Variables Configuration

### Set Environment Variables in DigitalOcean
- [ ] `WEBETU_USERNAME` = Your student ID
- [ ] `WEBETU_PASSWORD` = Your university password
- [ ] `DIA_ID` = Student identifier (12-15 digits)
- [ ] `IND_ID` = Student individual ID (8 digits)
- [ ] `TELEGRAM_BOT_TOKEN` = Token from BotFather
- [ ] `TELEGRAM_CHAT_ID` = Your personal Telegram chat ID
- [ ] `CHECK_INTERVAL_MINUTES` = 15
- [ ] `LOG_LEVEL` = INFO
- [ ] Mark sensitive variables as "Encrypt" (password, tokens)

### Verify Persistent Storage
- [ ] Volume configured: `/app/data` → 1GB
- [ ] Mounted in service: webetu-bot
- [ ] Will persist across restarts

## Phase 5: Deployment

### Deploy App
- [ ] Reviewed all configuration
- [ ] Clicked "Review"
- [ ] Clicked "Create App"
- [ ] Deployment started
- [ ] Build progress visible in UI

### Monitor Build
- [ ] Watched build logs for errors
- [ ] Build completed successfully
- [ ] No errors in build output
- [ ] Container image created
- [ ] App running (status: "Active")

### Verify Running App
- [ ] View app URL (auto-generated)
- [ ] Check "Runtime logs"
- [ ] See success messages:
  - "✅ WebEtu authentication successful"
  - "✅ Telegram connection successful"
  - "✅ Starting scheduler..."
- [ ] No error messages in logs
- [ ] No "Connection refused" errors

## Phase 6: Post-Deployment Testing

### Telegram Notifications
- [ ] Received startup message on Telegram
- [ ] Message contains check interval info (15 minutes)
- [ ] Bot is connected and online

### Grade Monitoring
- [ ] Bot checks grades successfully
- [ ] Logs show "✅ Fetched X exam grades"
- [ ] Logs show "✅ Fetched X continuous grades"
- [ ] No 401 authentication errors
- [ ] No connection errors

### Persistence
- [ ] Grades stored in `/app/data/grades.json`
- [ ] Token stored in `/app/data/token.json`
- [ ] Logs written to `/app/data/webetu_bot.log`
- [ ] No duplicate notifications on next check
- [ ] Storage survives app restart

## Phase 7: Ongoing Maintenance

### Monitoring
- [ ] Check logs weekly: DigitalOcean Dashboard → App → Runtime logs
- [ ] Monitor CPU/memory usage
- [ ] Verify bot still running (no "Error" status)
- [ ] Check last update time in metadata

### Updates
- [ ] Git push changes to GitHub
- [ ] DigitalOcean auto-deploys (watch build progress)
- [ ] Verify new version running in logs
- [ ] No service interruption during update

### Troubleshooting
- [ ] If bot crashes, check logs for error
- [ ] Verify WebEtu API status (manually check portal)
- [ ] Re-verify credentials if authentication fails
- [ ] Increase resource limits if hitting limits

## Phase 8: Backup & Security

### Data Management
- [ ] Enable DigitalOcean backups for app
- [ ] Download grades.json locally periodically
- [ ] Document recovery steps

### Credentials
- [ ] Never commit .env to Git
- [ ] Rotate Telegram bot token if leaked
- [ ] Use DigitalOcean "Encrypt" for sensitive variables
- [ ] Don't share screenshots with credentials visible

### Access Control
- [ ] GitHub repo is private
- [ ] Only authorized GitHub accounts can access
- [ ] DigitalOcean account secured with 2FA

---

## Quick Reference

### If Bot Won't Start
1. Check "Runtime logs" in DigitalOcean
2. Verify all environment variables set
3. Check WebEtu portal is accessible
4. Restart the app (on Deployments tab)

### If Notifications Stop
1. Check if app is still "Active"
2. Verify Telegram chat ID is correct
3. Restart app and check logs
4. Contact Telegram support if needed

### To Update Credentials
1. Update in DigitalOcean dashboard (Environment tab)
2. Trigger new deployment (make Git change) or restart app
3. App will use new credentials on next run

### To Change Check Interval
1. Update `CHECK_INTERVAL_MINUTES` in DigitalOcean
2. Restart app (or wait for next deployment)
3. Verify in logs: "Scheduled grade check every X minutes"

---

**Status**: Ready to deploy ✅
**Last Updated**: 2024-05-20
