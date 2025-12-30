# Quick Start Guide

Get the Django Webhook Service running in 5 minutes!

## ✅ What's Already Done

- ✅ Project structure created
- ✅ Dependencies installed
- ✅ Database migrated
- ✅ Sample processes created
- ✅ Google Service Account configured
- ✅ Environment variables set up

## 🚀 Quick Start Steps

### 1. Activate Virtual Environment

```bash
cd /Users/mahmoudshahin/Desktop/project1/django-webhook-event-service
source venv/bin/activate
```

### 2. Create Superuser (for admin access)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 3. Start Redis (Required for Celery)

**macOS:**
```bash
brew services start redis
# or in foreground: redis-server
```

**Check if Redis is running:**
```bash
redis-cli ping
# Should respond: PONG
```

### 4. Start the Services

You need 3 terminals:

**Terminal 1 - Django Server:**
```bash
source venv/bin/activate
python manage.py runserver
```
Access at: http://localhost:8000

**Terminal 2 - Celery Worker:**
```bash
source venv/bin/activate
celery -A webhook_service worker --loglevel=info
```

**Terminal 3 - Celery Beat (Scheduler):**
```bash
source venv/bin/activate
celery -A webhook_service beat --loglevel=info
```

## 🧪 Test the Integrations

### Test 1: Google Sheets Integration

```bash
python manage.py write_to_gsheet
```

This will:
- Create a test Google Sheet
- Write sample data
- Apply custom formatting
- Return the sheet URL

### Test 2: Slack Integration (if configured)

```bash
python manage.py send_slack_welcome --method sdk
```

This sends a welcome message to the configured Slack user.

### Test 3: GitHub Backup (if configured)

```bash
python manage.py backup_processes
```

This backs up the sample processes to your GitHub repository.

### Test 4: Webhook API

**Step 1 - Register a user:**
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "Test123456!",
    "password2": "Test123456!"
  }'
```

Copy the `access` token from the response.

**Step 2 - Send a webhook:**
```bash
curl -X POST http://localhost:8000/api/webhooks/receive/?source=test \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "event": "test",
    "message": "Hello Webhook!",
    "timestamp": "2024-01-01T12:00:00Z"
  }'
```

**Step 3 - View webhooks:**
```bash
curl -X GET http://localhost:8000/api/webhooks/list/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 📊 Access Admin Panel

1. Go to: http://localhost:8000/admin/
2. Login with your superuser credentials
3. View webhook events and processes

## 🔧 Configure Additional Services

### Slack (Optional but recommended)

1. Go to: https://api.slack.com/apps
2. Select/Create your app
3. Add Bot Token Scopes: `chat:write`, `im:write`, `users:read`
4. Install to workspace
5. Copy Bot User OAuth Token to `.env`:
   ```
   SLACK_BOT_TOKEN=xoxb-your-token-here
   ```

### GitHub (Optional but recommended)

1. Go to: GitHub Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` scope
3. Add to `.env`:
   ```
   GITHUB_TOKEN=ghp_your-token-here
   GITHUB_USERNAME=your-username
   ```

## 📁 Current Configuration

**Database:** SQLite (`db.sqlite3`)
- 2 sample processes created (hello_world, data_processor)

**Google Sheets:**
- Service Account: `gspread-sa@django-gspread-integration.iam.gserviceaccount.com`
- Ready to use! Just share sheets with this email.

**Slack:**
- Bot Token: Already configured in `.env`
- User ID: U02AAG62RPH (configured)

**GitHub:**
- Needs token configuration (see above)

## 🎯 Next Steps

1. ✅ Create superuser
2. ✅ Test Google Sheets integration
3. 🔲 Configure Slack webhook URL (optional)
4. 🔲 Configure GitHub token
5. 🔲 Test all integrations
6. 🔲 Build your custom webhook handlers

## 📝 Notes

- Redis must be running for Celery to work
- All webhooks are processed asynchronously
- Check Celery worker terminal for task logs
- GitHub backup runs automatically every 24 hours
- Admin panel shows all webhook events and their status

## 🆘 Quick Troubleshooting

**Issue: Redis connection refused**
```bash
brew services start redis
```

**Issue: Module not found**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**Issue: Database errors**
```bash
python manage.py migrate
```

**Issue: Google Sheets permission denied**
- Share the sheet with: `gspread-sa@django-gspread-integration.iam.gserviceaccount.com`
- Give "Editor" permissions

---

**You're all set! 🚀**

Check the full [README.md](README.md) for complete documentation.

