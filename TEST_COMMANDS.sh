#!/bin/bash
# Test Commands for Django Webhook Service
# Run these commands to test all features

echo "======================================"
echo "Django Webhook Service - Test Suite"
echo "======================================"
echo ""

# Activate virtual environment
source venv/bin/activate

echo "1. Testing Sample Processes Creation..."
python manage.py create_sample_processes
echo ""

echo "2. Testing Google Sheets Integration..."
echo "   (This will create a test sheet and return the URL)"
python manage.py write_to_gsheet
echo ""

echo "3. Testing Slack Integration (SDK)..."
echo "   (This will send a welcome message via Slack SDK)"
# Uncomment when Slack is fully configured:
# python manage.py send_slack_welcome --method sdk
echo "   ⚠️  Configure SLACK_BOT_TOKEN in .env and uncomment in script"
echo ""

echo "4. Testing GitHub Backup..."
echo "   (This will backup processes to GitHub)"
# Uncomment when GitHub is configured:
# python manage.py backup_processes
echo "   ⚠️  Configure GITHUB_TOKEN in .env and uncomment in script"
echo ""

echo "======================================"
echo "API Tests (requires running server)"
echo "======================================"
echo ""

echo "5. Register a test user:"
echo 'curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"testuser\",\"email\":\"test@example.com\",\"password\":\"Test123456!\",\"password2\":\"Test123456!\"}"'
echo ""

echo "6. Get access token:"
echo 'curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"testuser\",\"password\":\"Test123456!\"}"'
echo ""

echo "7. Send a test webhook (replace YOUR_TOKEN):"
echo 'curl -X POST "http://localhost:8000/api/webhooks/receive/?source=test" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"event\":\"test\",\"message\":\"Hello Webhook!\",\"timestamp\":\"2024-01-01T12:00:00Z\"}"'
echo ""

echo "8. List webhooks (replace YOUR_TOKEN):"
echo 'curl -X GET http://localhost:8000/api/webhooks/list/ \
  -H "Authorization: Bearer YOUR_TOKEN"'
echo ""

echo "======================================"
echo "To run these commands:"
echo "1. Make script executable: chmod +x TEST_COMMANDS.sh"
echo "2. Run: ./TEST_COMMANDS.sh"
echo "======================================"

