# 🐳 Docker-Based Local Temporary Email Service

This setup provides a **local temporary email service** using Docker and MailHog for the Netflix registration bot.

## 🚀 Quick Start

### 1. Start the Email Service
```bash
# Start MailHog in Docker
docker-compose up -d

# Check if it's running
docker-compose ps
```

### 2. Test the Service
```bash
# Quick test to verify Docker service
python test_docker_email.py

# Full functionality test
python local_temp_email.py
```

### 3. Access Web Interface
- **Web UI**: http://localhost:8025
- **SMTP**: localhost:1025
- **API**: http://localhost:8025/api/v1

## 📁 Files Created

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Docker configuration for MailHog |
| `local_temp_email.py` | Local email service implementation |
| `test_docker_email.py` | Quick test to verify Docker setup |
| `README_Docker_Email.md` | This documentation |

## 🔧 Features

### ✅ **Local Email Service**
- **No external dependencies** - runs completely locally
- **Docker-based** - easy to start/stop
- **Web interface** - view emails in browser
- **SMTP server** - send/receive emails
- **API access** - programmatic email management

### ✅ **Email Operations**
- Generate random email addresses
- Send test emails
- Receive and monitor emails
- Clear email inbox
- Wait for specific emails

## 🎯 Usage Examples

### Basic Email Generation
```python
from local_temp_email import LocalTempEmailService

# Initialize service
email_service = LocalTempEmailService()

# Create temporary email
result = email_service.create_temporary_email()
print(f"Email: {result['email']}")
```

### Send Test Email
```python
# Send a test email
email_service.send_test_email(
    to_email="test@localhost",
    subject="Netflix Registration",
    body="Welcome to Netflix!"
)
```

### Wait for Email
```python
# Wait for email to arrive
email = email_service.wait_for_email(max_wait_time=60)
if email:
    print(f"Received: {email['subject']}")
```

## 🛠️ Docker Commands

### Start Service
```bash
docker-compose up -d
```

### Stop Service
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f
```

### Restart Service
```bash
docker-compose restart
```

## 🔍 Monitoring

### Check Service Status
```bash
# Check if containers are running
docker-compose ps

# Check logs
docker-compose logs mailhog
```

### Web Interface
- Open http://localhost:8025 in your browser
- View all received emails
- Monitor email traffic in real-time

## 🚨 Troubleshooting

### Service Not Starting
```bash
# Check Docker is running
docker --version

# Check if ports are available
netstat -an | findstr :8025
netstat -an | findstr :1025
```

### Port Conflicts
If ports 8025 or 1025 are in use:
1. Edit `docker-compose.yml`
2. Change port mappings:
   ```yaml
   ports:
     - "8026:8025"  # Web UI
     - "1026:1025"   # SMTP
   ```

### Service Not Responding
```bash
# Restart the service
docker-compose down
docker-compose up -d

# Check logs for errors
docker-compose logs mailhog
```

## 🔗 Integration with Netflix Bot

The local email service can be integrated with the Netflix registration bot by:

1. **Replacing external email services** with local service
2. **Using SMTP for email sending** instead of web scraping
3. **Monitoring emails via API** instead of browser automation

### Example Integration
```python
# In netflix_registration_bot.py
from local_temp_email import LocalTempEmailService

# Replace temp email generator
email_service = LocalTempEmailService()
email_result = email_service.create_temporary_email()
```

## 📊 Benefits

### ✅ **Advantages over External Services**
- **No rate limits** - unlimited email generation
- **No network dependencies** - works offline
- **Full control** - customize as needed
- **Privacy** - emails stay local
- **Reliability** - no external service failures

### ✅ **Perfect for Netflix Bot**
- **Fast email generation** - instant results
- **Reliable email monitoring** - no timeouts
- **No captcha issues** - no web scraping
- **Consistent performance** - no external dependencies

## 🎉 Ready to Use!

Once the Docker service is running, you can:

1. **Generate emails instantly** - no waiting for external services
2. **Monitor emails reliably** - no web scraping failures
3. **Test the Netflix bot** - with consistent email service
4. **Scale as needed** - multiple email addresses simultaneously

The local email service provides a **robust, reliable foundation** for the Netflix registration bot! 🚀

