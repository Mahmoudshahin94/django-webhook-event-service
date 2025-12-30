# Django Webhook Event Service

A production-ready webhook receiver service built with Django REST Framework, featuring JWT authentication, Celery background tasks, and integrations with Google Sheets, Slack, and GitHub.

## 🚀 Features

- **Generic Webhook Receiver**: Accept and process webhooks from any source (Slack, Stripe, GitHub, etc.)
- **JWT Authentication**: Secure API endpoints with token-based authentication
- **Async Processing**: Celery + Redis for background task processing
- **Google Sheets Integration**: Write data with custom formatting using gspread
- **Slack Integration**: Send messages via both Slack SDK and webhooks
- **GitHub Backup System**: Automated daily backups of database scripts to GitHub
- **Django Admin**: Full admin interface for managing webhooks and processes
- **RESTful API**: Clean, documented API endpoints

## 📋 Tech Stack

- **Python 3.11**
- **Django 5.0**
- **Django REST Framework 3.14**
- **JWT Authentication** (djangorestframework-simplejwt)
- **SQLite** (default database)
- **Celery 5.3** (background tasks)
- **Redis** (Celery broker)
- **gspread** (Google Sheets)
- **slack-sdk** (Slack integration)
- **PyGithub** (GitHub API)

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11** or higher
- **pip** (Python package manager)
- **Redis** (for Celery broker)
  - macOS: `brew install redis`
  - Ubuntu: `sudo apt-get install redis-server`
- **Git** (for version control)

## 📦 Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd django-webhook-event-service
```

### 2. Create Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file and configure it:

```bash
cp env.example .env
```

Edit `.env` file with your credentials:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT Authentication
JWT_SECRET_KEY=your-jwt-secret-key

# Google Sheets
GOOGLE_SERVICE_ACCOUNT_FILE=credentials/django-gspread-integration-0c471d0387ea.json

# Slack
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
SLACK_DM_USER_ID=U02AAG62RPH

# GitHub
GITHUB_TOKEN=your-github-token
GITHUB_USERNAME=your-username
GITHUB_REPO=processes_backup

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### 5. Database Setup

Run migrations to create the database:

```bash
python manage.py migrate
```

Create a superuser for admin access:

```bash
python manage.py createsuperuser
```

Create sample process records:

```bash
python manage.py create_sample_processes
```

## 🔑 External Service Setup

### Google Sheets Configuration

The Google Service Account JSON file is already included in the `credentials/` directory. To use it:

1. The service account email is: `gspread-sa@django-gspread-integration.iam.gserviceaccount.com`
2. Share any Google Sheet you want to access with this email address
3. Give it "Editor" permissions
4. The path is already configured in `env.example`

**Testing Google Sheets:**

```bash
python manage.py write_to_gsheet
```

This will create a test sheet with sample data and custom formatting.

### Slack App Configuration

You need to configure your Slack app with the following scopes:

#### Step 1: Create/Configure Slack App

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Select your app or create a new one
3. Go to **OAuth & Permissions**

#### Step 2: Add Bot Token Scopes

Add these scopes under "Bot Token Scopes":
- `chat:write` - Send messages
- `im:write` - Send direct messages
- `users:read` - Read user information

#### Step 3: Install App to Workspace

1. Click "Install to Workspace"
2. Authorize the app
3. Copy the **Bot User OAuth Token** (starts with `xoxb-`)
4. Add it to your `.env` file as `SLACK_BOT_TOKEN`

#### Step 4: Set Up Incoming Webhooks (Optional)

For the webhook approach:

1. Go to **Incoming Webhooks** in your Slack app settings
2. Activate Incoming Webhooks
3. Click "Add New Webhook to Workspace"
4. Select a channel
5. Copy the webhook URL
6. Add it to your `.env` file as `SLACK_WEBHOOK_URL`

**Testing Slack Integration:**

```bash
# Test both SDK and webhook methods
python manage.py send_slack_welcome

# Test only SDK
python manage.py send_slack_welcome --method sdk

# Test only webhook
python manage.py send_slack_welcome --method webhook
```

### GitHub Token Generation

To enable automated backups to GitHub:

#### Step 1: Generate Personal Access Token

1. Go to GitHub **Settings** → **Developer settings** → **Personal access tokens**
2. Click "Generate new token" (classic)
3. Give it a descriptive name: "Django Webhook Service Backup"
4. Select expiration (recommend: No expiration for automation)
5. Select scopes:
   - ✅ `repo` (Full control of private repositories)
6. Click "Generate token"
7. **Copy the token immediately** (you won't see it again!)

#### Step 2: Configure Environment

Add to your `.env` file:

```bash
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GITHUB_USERNAME=your-github-username
GITHUB_REPO=processes_backup
```

**The script will automatically create the repository if it doesn't exist!**

**Testing GitHub Backup:**

```bash
python manage.py backup_processes
```

This will:
- Create the `processes_backup` repository if it doesn't exist
- Back up all process scripts as `.py` files
- Create/update files based on process code

## 🏃 Running the Application

You need to run three components:

### Terminal 1: Django Development Server

```bash
python manage.py runserver
```

The API will be available at: `http://localhost:8000`

### Terminal 2: Celery Worker

```bash
celery -A webhook_service worker --loglevel=info
```

This processes background tasks (webhooks, Slack messages, etc.)

### Terminal 3: Celery Beat (Scheduler)

```bash
celery -A webhook_service beat --loglevel=info
```

This runs scheduled tasks (daily GitHub backup at 2 AM UTC)

### Start Redis (if not running)

```bash
# macOS
brew services start redis

# Ubuntu
sudo systemctl start redis-server

# Or run in foreground
redis-server
```

## 📚 API Documentation

### Authentication Endpoints

#### Register a New User

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!"
  }'
```

Response:
```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  },
  "message": "User registered successfully"
}
```

#### Obtain JWT Token

```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "SecurePass123!"
  }'
```

#### Refresh Token

```bash
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "your-refresh-token"
  }'
```

#### Get User Profile

```bash
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer your-access-token"
```

### Webhook Endpoints

#### Receive a Webhook

```bash
curl -X POST http://localhost:8000/api/webhooks/receive/ \
  -H "Authorization: Bearer your-access-token" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "slack",
    "event_type": "message",
    "data": {
      "user": "john_doe",
      "message": "Hello, World!"
    }
  }'
```

Response:
```json
{
  "message": "Webhook received successfully",
  "event_id": 1,
  "status": "queued"
}
```

#### List All Webhooks

```bash
curl -X GET http://localhost:8000/api/webhooks/list/ \
  -H "Authorization: Bearer your-access-token"
```

#### Get Webhook Details

```bash
curl -X GET http://localhost:8000/api/webhooks/1/ \
  -H "Authorization: Bearer your-access-token"
```

## 🔧 Management Commands

### Google Sheets

Write sample data to Google Sheet:
```bash
python manage.py write_to_gsheet
python manage.py write_to_gsheet --sheet-name "My Custom Sheet"
```

### Slack

Send welcome message:
```bash
python manage.py send_slack_welcome
python manage.py send_slack_welcome --user-id U12345678
python manage.py send_slack_welcome --method sdk  # or webhook or both
```

### GitHub Backup

Create sample processes:
```bash
python manage.py create_sample_processes
```

Backup processes to GitHub:
```bash
python manage.py backup_processes
```

## 📊 Admin Interface

Access the Django admin at: `http://localhost:8000/admin/`

Login with your superuser credentials to:
- View and manage webhook events
- Create/edit process scripts
- Monitor processing status
- View user accounts

## 🗂️ Project Structure

```
django-webhook-event-service/
├── apps/
│   ├── authentication/          # JWT authentication
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── webhooks/                # Webhook receiver
│   │   ├── models.py           # WebhookEvent model
│   │   ├── views.py            # API endpoints
│   │   ├── tasks.py            # Celery tasks
│   │   └── urls.py
│   └── integrations/            # External integrations
│       ├── models.py           # Process model
│       ├── google_sheets.py    # Google Sheets integration
│       ├── slack_handler.py    # Slack integration
│       ├── github_backup.py    # GitHub backup
│       ├── tasks.py            # Celery tasks
│       └── management/
│           └── commands/       # Management commands
├── webhook_service/
│   ├── settings.py             # Django settings
│   ├── celery.py              # Celery configuration
│   └── urls.py                # URL routing
├── credentials/                # Service account files
├── db.sqlite3                 # SQLite database
├── requirements.txt           # Python dependencies
├── env.example               # Environment variables template
└── README.md                 # This file
```

## 🔄 Background Tasks

### Scheduled Tasks (Celery Beat)

- **GitHub Backup**: Runs daily to backup all process scripts
  - Schedule: Every 24 hours (configurable in settings.py)
  - Task: `apps.integrations.tasks.backup_to_github_task`

### Async Tasks

- **Process Webhook**: Processes webhook events asynchronously
- **Send Slack Message**: Sends Slack messages in background
- **Write to Google Sheet**: Writes data to sheets asynchronously

## 🧪 Testing

### Test Webhook Reception

```bash
# First, get an access token
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"SecurePass123!"}' \
  | python -c "import sys, json; print(json.load(sys.stdin)['access'])")

# Send a test webhook
curl -X POST http://localhost:8000/api/webhooks/receive/?source=test \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "test": true,
    "message": "Hello from webhook test",
    "timestamp": "2024-01-01T12:00:00Z"
  }'
```

### Monitor Celery Tasks

Watch Celery worker output in Terminal 2 to see tasks being processed in real-time.

## 🚀 Deployment Notes

### Production Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use a strong `SECRET_KEY` and `JWT_SECRET_KEY`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Use environment variables for all sensitive data
- [ ] Set up proper logging
- [ ] Use a production WSGI server (Gunicorn, uWSGI)
- [ ] Set up HTTPS/SSL
- [ ] Use a production-grade Redis instance
- [ ] Configure Celery with proper concurrency settings
- [ ] Set up monitoring (Sentry, etc.)

### Environment Variables for Production

```bash
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECRET_KEY=your-production-secret-key
JWT_SECRET_KEY=your-production-jwt-key

# Use PostgreSQL in production
DATABASE_URL=postgresql://user:password@localhost:5432/webhook_db

# Use production Redis
CELERY_BROKER_URL=redis://your-redis-host:6379/0
```

## 📝 Database Models

### WebhookEvent

Stores all incoming webhook events:
- `id`: Primary key
- `source`: Source identifier (e.g., "slack", "stripe")
- `payload`: JSON data
- `received_at`: Timestamp
- `processed_at`: Processing completion time
- `status`: pending, processing, completed, failed
- `error_message`: Error details if failed

### Process

Stores scripts for GitHub backup:
- `id`: Primary key
- `name`: Process name (max 50 chars)
- `code`: Unique code (used as filename)
- `script`: Python script content
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Redis Connection Error

```
Error: Error 111 connecting to localhost:6379. Connection refused.
```

**Solution**: Start Redis server:
```bash
brew services start redis  # macOS
sudo systemctl start redis-server  # Ubuntu
```

### Google Sheets Permission Denied

```
Error: Insufficient permissions
```

**Solution**: Share the Google Sheet with the service account email:
`gspread-sa@django-gspread-integration.iam.gserviceaccount.com`

### Slack API Error

```
Error: not_in_channel or channel_not_found
```

**Solution**: Make sure your Slack bot has the correct permissions and is installed in your workspace.

### GitHub Authentication Failed

```
Error: Bad credentials
```

**Solution**: 
1. Verify your GitHub token is correct
2. Check token hasn't expired
3. Ensure token has `repo` scope

## 📞 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the error logs in terminal
3. Check Django admin for webhook/process status
4. Open an issue on GitHub

---

**Built with ❤️ using Django REST Framework**
