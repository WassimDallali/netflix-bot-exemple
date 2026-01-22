# Configuration file for Tiger SMS Bot
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Tiger SMS API Configuration
API_KEY = "--YOUR_API_KEY_HERE--"
BASE_URL = "https://api.tiger-sms.com/stubs/handler_api.php"

# Service and Country Codes
SERVICES = {
    "netflix": "nf",
    "instagram": "ig", 
    "telegram": "tg",
    "whatsapp": "wa",
    "facebook": "fb",
    "google": "go",
    "tiktok": "tt"
}

COUNTRIES = {
    "france": "78",
    "usa": "1", 
    "uk": "44",
    "germany": "49",
    "spain": "34"
}

# API Endpoints
ENDPOINTS = {
    "get_number": "getNumber",
    "get_status": "getStatus", 
    "set_status": "setStatus",
    "get_balance": "getBalance"
}

# Request timeout (seconds)
TIMEOUT = 30

# Maximum retry attempts
MAX_RETRIES = 3

