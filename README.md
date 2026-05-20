# WebEtu Grades Monitor Bot 📚

A Python Telegram bot that monitors your university grades from the WebEtu portal (PROGRESS system) and sends notifications when new grades are posted.

## Features

- ✅ **Automatic Grade Monitoring** - Checks for new grades every 15 minutes
- ✅ **Telegram Notifications** - Instant alerts when new grades arrive
- ✅ **Persistent Storage** - Keeps history of all grades in JSON format
- ✅ **JWT Authentication** - Secure connection to WebEtu API
- ✅ **Error Handling** - Automatic retries and graceful error reporting
- ✅ **Docker Support** - Easy deployment with containerization
- ✅ **DigitalOcean Ready** - Pre-configured for cloud deployment

## Quick Start

### Prerequisites

- Python 3.12+
- pip (Python package installer)
- Telegram Bot Token
- WebEtu credentials

### Local Setup

1. **Clone or download the project**

```bash
cd webetu-bot
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment**

```bash
# Copy the example configuration
cp .env.example .env

# Edit .env with your credentials
# Required variables:
# - WEBETU_USERNAME: Your student ID
# - WEBETU_PASSWORD: Your university password
# - DIA_ID: Your student DIA ID
# - IND_ID: Your student Individual ID
# - TELEGRAM_BOT_TOKEN: From BotFather
# - TELEGRAM_CHAT_ID: Your personal Telegram chat ID
```

5. **Run the bot**

```bash
python main.py
```

## How to Get Required Credentials

### WebEtu Credentials
- **Username**: Your student ID (usually 12 digits)
- **Password**: Your university portal password

### DIA_ID & IND_ID
First run the bot in debug mode - it will print these IDs:
```bash
LOG_LEVEL=DEBUG python main.py
```

### Telegram Bot Token
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Name your bot (e.g., "WebEtu Grades Monitor")
4. Copy the token provided

### Telegram Chat ID
1. Open Telegram and search for `@userinfobot`
2. Send `/start` to get your chat ID
3. Use this ID as `TELEGRAM_CHAT_ID`

## Project Structure

```
webetu-bot/
├── main.py              # Bot scheduler and main entry point
├── bot.py               # Telegram notifications
├── api.py               # WebEtu API client
├── storage.py          # Grade storage and management
├── config.py           # Configuration and environment variables
├── requirements.txt     # Python dependencies
├── .env.example         # Configuration template
├── Dockerfile           # Docker containerization
├── docker-compose.yml   # Local Docker setup
├── app.yaml             # DigitalOcean configuration
└── data/
    ├── grades.json      # Grade history (auto-generated)
    ├── token.json       # JWT tokens (auto-generated)
    └── webetu_bot.log   # Application logs (auto-generated)
```

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `WEBETU_USERNAME` | Yes | - | Your student ID |
| `WEBETU_PASSWORD` | Yes | - | Your university password |
| `DIA_ID` | Yes | - | Student DIA ID |
| `IND_ID` | Yes | - | Student Individual ID |
| `TELEGRAM_BOT_TOKEN` | Yes | - | Telegram bot token |
| `TELEGRAM_CHAT_ID` | Yes | - | Your chat ID |
| `CHECK_INTERVAL_MINUTES` | No | 15 | Grade check frequency |
| `LOG_LEVEL` | No | INFO | Logging verbosity |

## Docker Deployment

### Local Testing

```bash
# Build and run
docker-compose up --build

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Production Deployment

See [DIGITALOCEAN_DEPLOYMENT.md](DIGITALOCEAN_DEPLOYMENT.md) for DigitalOcean App Platform setup.

## API Endpoints Used

The bot communicates with the WebEtu API:
- **Authentication**: `POST /api/auth/login`
- **Exam Grades**: `GET /api/service/result/read/exam/{DIA_ID}/{IND_ID}`
- **Continuous Grades**: `GET /api/service/result/read/continuous/{DIA_ID}/{IND_ID}`

## Monitoring

### Application Logs

Logs are saved to `/app/data/webetu_bot.log` and displayed in console.

**Log Levels**:
- `DEBUG`: Detailed information for troubleshooting
- `INFO`: Normal operation information
- `WARNING`: Warning messages
- `ERROR`: Error messages only

### Grade Storage

Grades are stored in JSON format at `/app/data/grades.json`:

```json
{
  "exam_grades": [
    {"subject": "Mathematics", "grade": 18.5, "type": "exam"},
    ...
  ],
  "continuous_grades": [...],
  "metadata": {
    "total_exam_grades": 14,
    "total_continuous_grades": 20,
    "last_updated": "2024-05-20T21:26:48",
    "initialized": true
  }
}
```

## Troubleshooting

### Bot Won't Start

1. Check `.env` file exists with all required variables
2. Verify Python 3.12+ installed: `python --version`
3. Check dependencies: `pip list`
4. Review logs for detailed error messages

### No Notifications Received

1. Verify Telegram bot token is correct
2. Check chat ID is accurate
3. Ensure bot has permission to message the chat
4. Check bot.py logs for send errors

### Authentication Fails

1. Verify WebEtu username and password
2. Check WebEtu portal is accessible
3. Verify DIA_ID and IND_ID are correct
4. Ensure account hasn't locked due to failed attempts

### High Memory Usage

1. Increase `CHECK_INTERVAL_MINUTES` to check less frequently
2. Change `LOG_LEVEL` to INFO (less verbose)
3. Check Docker resource limits in `docker-compose.yml`

## Performance

- **Initial startup**: ~5 seconds
- **Grade check cycle**: ~2-3 seconds
- **Memory usage**: ~50-100 MB (normal operation)
- **Storage**: < 1 MB (grades.json)

## Security Notes

⚠️ **Important**: 
- Never commit `.env` file to git (contains credentials)
- Use `.env.example` as a template only
- Rotate Telegram bot token if credentials are leaked
- Run in isolated environment (Docker recommended)

## License

This project is for personal educational use only. Use at your own risk.

## Support

For issues:
1. Check logs with `LOG_LEVEL=DEBUG`
2. Review [DIGITALOCEAN_DEPLOYMENT.md](DIGITALOCEAN_DEPLOYMENT.md)
3. Verify all configuration variables
4. Test with simplified setup

## Changelog

### v1.0.0 (Current)
- ✅ Full WebEtu API integration
- ✅ Telegram notifications
- ✅ Persistent grade storage
- ✅ Docker containerization
- ✅ DigitalOcean deployment ready
- ✅ English localization
- ✅ 15-minute check interval
- ✅ Baseline sync (no notifications on first run)

---

**Last Updated**: 2024-05-20
**Status**: Production Ready ✅
