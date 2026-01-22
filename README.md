# Netflix Registration Bot with Playwright - Educational Purpose

Complete automated Netflix registration system using Playwright web automation, Tiger SMS API, and temporary email services.

## ⚠️ Important Notice

This bot is for **educational purposes only**. Please ensure you:
- Comply with Netflix's Terms of Service
- Use the service responsibly
- Respect the API rate limits
- Follow all applicable laws and regulations

## 🚀 Features

### 🔢 Tiger SMS Integration
- Get French phone numbers for Netflix verification
- Automatic SMS code monitoring
- Real-time verification code detection
- Tiger SMS API integration

### 📧 Temporary Email Generation
- Multiple temporary email services (TempMail, 10MinuteMail, GuerrillaMail, MailDrop)
- Automatic email address generation
- Fallback random email generation
- Email monitoring capabilities

### 🤖 Complete Netflix Registration Bot
- **Playwright Web Automation**: Automated browser interaction
- **Random Plan Selection**: Automatically selects Netflix plans
- **Phone Payment Integration**: Uses phone numbers for payment
- **Form Auto-Fill**: Automatically fills registration forms
- **SMS Verification**: Monitors and enters SMS codes
- **Stealth Mode**: Anti-detection browser settings

## 📦 Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install
```

## 🎯 Usage

### 1. Phone Number Only (Tiger SMS)
```bash
python tiger_sms_bot.py
```

### 2. Email Only (Temporary Email)
```bash
python temp_email_generator.py
```

### 3. Complete Netflix Registration (Full Automation)
```bash
python netflix_registration_bot.py
```

## 📁 File Structure

```
bot-netflix/
├── tiger_sms_bot.py              # SMS bot for phone numbers
├── temp_email_generator.py       # Temporary email generator with Playwright
├── netflix_registration_bot.py   # Complete Netflix registration bot
├── config.py                     # Configuration and API settings
├── requirements.txt              # Python dependencies
├── env_example.txt               # Environment variables template
└── README.md                     # This documentation
```

## 🔄 How It Works

### Complete Registration Process:

1. **🔑 Get Credentials**: 
   - French phone number from Tiger SMS API
   - Temporary email from disposable services
   - Generated password and random name

2. **🌐 Navigate to Netflix**: 
   - Opens Netflix signup page
   - Handles cookies and redirects

3. **📋 Select Random Plan**: 
   - Automatically selects a Netflix plan
   - Handles plan selection UI

4. **📝 Fill Registration Form**: 
   - Enters email and password
   - Handles form validation

5. **💳 Navigate to Phone Payment**: 
   - Goes to phone payment option
   - Fills phone number for payment

6. **📱 SMS Verification**: 
   - Monitors for SMS codes
   - Automatically enters verification codes

7. **✅ Complete Registration**: 
   - Finalizes Netflix account creation

### Example Output:

```
============================================================
Netflix Registration Bot with Playwright - Educational Purpose
============================================================
Starting browser for Netflix registration...
✓ Browser started successfully
=== Getting Registration Credentials ===

1. Getting French phone number for Netflix...
✓ Phone number: 33602898192

2. Getting temporary email address...
✓ Random email generated: wz7xmil7@throwaway.email
✓ Email address: wz7xmil7@throwaway.email
✓ Password: K7Rq!zsWubLK
✓ Name: Emery Kendall

Registration Credentials:
📧 Email: wz7xmil7@throwaway.email
📱 Phone: 33602898192
🔑 Password: K7Rq!zsWubLK
👤 Name: Emery Kendall

Step 1: Navigating to Netflix signup...
✓ Successfully navigated to Netflix signup

Step 2: Selecting random plan...
✓ Selected plan: Premium - $22.99

Step 3: Filling registration form...
✓ Email filled: wz7xmil7@throwaway.email
✓ Password filled

Step 4: Navigating to phone payment...
✓ Successfully navigated to phone payment page

Step 5: Filling phone payment form...
✓ Phone number filled: 33602898192

Step 6: Waiting for SMS verification...
✓ SMS Code received: 123456

Step 7: Entering SMS verification code...
✓ SMS code entered: 123456

Step 8: Completing registration...
🎉 NETFLIX REGISTRATION COMPLETED! 🎉
✓ Account created successfully
✓ Email: wz7xmil7@throwaway.email
✓ Phone: 33602898192
✓ You can now use your Netflix account!
```

## 🛠️ Technical Features

### Playwright Automation
- **Stealth Mode**: Anti-detection browser settings
- **Multiple Selectors**: Robust element selection
- **Error Handling**: Comprehensive error recovery
- **Real Browser**: Full Chromium automation

### Tiger SMS Integration
- **API Integration**: Direct Tiger SMS API calls
- **SMS Monitoring**: Real-time SMS code detection
- **French Numbers**: Specialized for Netflix France
- **Error Handling**: Robust API error management

### Temporary Email Services
- **Multiple Providers**: TempMail, 10MinuteMail, GuerrillaMail, MailDrop
- **Fallback System**: Random email generation
- **Email Monitoring**: Inbox checking capabilities
- **Service Redundancy**: Multiple service options

## 🔧 Configuration

### API Settings (config.py)
```python
# Tiger SMS API Configuration
API_KEY = "v0SU1z0PyBV6VvaKiEAYRvh2OprF1OGm"
BASE_URL = "https://api.tiger-sms.com/stubs/handler_api.php"

# Service and Country Codes
SERVICES = {
    "netflix": "nf",
    "instagram": "ig", 
    "telegram": "tg",
    "whatsapp": "wa"
}

COUNTRIES = {
    "france": "78",
    "usa": "1", 
    "uk": "44"
}
```

### Browser Settings
- **Headless Mode**: Configurable browser visibility
- **User Agent**: Random user agent rotation
- **Viewport**: Realistic screen resolution
- **Geolocation**: New York coordinates
- **Stealth Scripts**: Anti-automation detection

## 📊 Services Supported

### Phone Number Services:
- **Tiger SMS API**: French numbers (country code 78)
- **Netflix Service**: Service code 'nf'
- **SMS Monitoring**: Real-time code detection

### Email Services:
- **TempMail.org**: Primary service
- **10MinuteMail.com**: Secondary service
- **GuerrillaMail.com**: Tertiary service
- **MailDrop.cc**: Quaternary service
- **Random Generation**: Fallback system

### Netflix Integration:
- **Signup Page**: https://www.netflix.com/signup/
- **Phone Payment**: https://www.netflix.com/signup/dcboption
- **Plan Selection**: Automatic plan selection
- **Form Automation**: Complete form filling

## 🎓 Educational Value

This bot demonstrates:
- **Web Automation**: Playwright browser automation
- **API Integration**: REST API communication
- **Error Handling**: Robust error management
- **Service Orchestration**: Multiple service coordination
- **Anti-Detection**: Stealth automation techniques
- **Form Automation**: Dynamic form filling
- **SMS Integration**: Real-time SMS monitoring

## 🔒 Security & Privacy

- **Temporary Data**: All data is temporary and disposable
- **No Personal Info**: No real personal information used
- **Educational Only**: Designed for learning purposes
- **API Keys**: Secure API key management
- **Browser Isolation**: Isolated browser sessions

## 🚨 Troubleshooting

### Common Issues:

1. **Browser Not Starting**: Install Playwright browsers
2. **API Errors**: Check Tiger SMS API key
3. **Selector Issues**: Netflix UI changes
4. **SMS Timeout**: Check phone number validity
5. **Email Services**: Temporary email services may be down

### Solutions:

```bash
# Reinstall Playwright browsers
python -m playwright install

# Check API key in config.py
# Verify Tiger SMS account balance
# Update selectors for Netflix UI changes
```

## 📝 Disclaimer

This software is provided for **educational purposes only**. The authors are not responsible for any misuse of this software. Users must comply with all applicable laws and terms of service of the services they interact with.

## 📄 License

This project is for educational purposes only. Use at your own risk.

---

**🎯 Ready to learn web automation with Playwright and API integration!**