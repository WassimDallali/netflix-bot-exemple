#!/usr/bin/env python3
"""
Simple Docker Email Test
Tests the basic functionality of the Docker-based email service
"""

import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from colorama import init, Fore

init(autoreset=True)

def test_web_interface():
    """Test if web interface is accessible"""
    try:
        response = requests.get("http://localhost:8025", timeout=5)
        if response.status_code == 200:
            print(f"{Fore.GREEN}✓ Web interface is accessible")
            return True
        else:
            print(f"{Fore.RED}✗ Web interface not accessible (status: {response.status_code})")
            return False
    except Exception as e:
        print(f"{Fore.RED}✗ Web interface error: {str(e)}")
        return False

def test_smtp_server():
    """Test if SMTP server is working"""
    try:
        # Create a simple test email
        msg = MIMEMultipart()
        msg['From'] = "test@localhost"
        msg['To'] = "recipient@localhost"
        msg['Subject'] = "Docker Email Test"
        
        body = "This is a test email from the Docker MailHog service!"
        msg.attach(MIMEText(body, 'plain'))
        
        # Send via SMTP
        with smtplib.SMTP("localhost", 1025) as server:
            server.send_message(msg)
        
        print(f"{Fore.GREEN}✓ SMTP server is working - email sent successfully")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}✗ SMTP server error: {str(e)}")
        return False

def test_api_endpoints():
    """Test different API endpoints"""
    endpoints = [
        "http://localhost:8025/api/v1/messages",
        "http://localhost:8025/api/v2/messages",
        "http://localhost:8025/api/v1/messages?limit=10"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, timeout=5)
            if response.status_code == 200:
                print(f"{Fore.GREEN}✓ API endpoint working: {endpoint}")
                return True
            else:
                print(f"{Fore.YELLOW}⚠️ API endpoint issue: {endpoint} (status: {response.status_code})")
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️ API endpoint error: {endpoint} - {str(e)}")
    
    return False

def main():
    """Main test function"""
    print(f"{Fore.CYAN}{'='*50}")
    print(f"{Fore.CYAN}Simple Docker Email Service Test")
    print(f"{Fore.CYAN}{'='*50}")
    
    # Test 1: Web Interface
    print(f"\n{Fore.BLUE}Test 1: Web Interface")
    web_ok = test_web_interface()
    
    # Test 2: SMTP Server
    print(f"\n{Fore.BLUE}Test 2: SMTP Server")
    smtp_ok = test_smtp_server()
    
    # Test 3: API Endpoints
    print(f"\n{Fore.BLUE}Test 3: API Endpoints")
    api_ok = test_api_endpoints()
    
    # Summary
    print(f"\n{Fore.CYAN}{'='*50}")
    print(f"{Fore.CYAN}TEST SUMMARY")
    print(f"{Fore.CYAN}{'='*50}")
    
    if web_ok:
        print(f"{Fore.GREEN}✓ Web Interface: http://localhost:8025")
    else:
        print(f"{Fore.RED}✗ Web Interface: Not accessible")
    
    if smtp_ok:
        print(f"{Fore.GREEN}✓ SMTP Server: localhost:1025")
    else:
        print(f"{Fore.RED}✗ SMTP Server: Not working")
    
    if api_ok:
        print(f"{Fore.GREEN}✓ API Endpoints: Working")
    else:
        print(f"{Fore.YELLOW}⚠️ API Endpoints: Some issues")
    
    # Overall result
    if web_ok and smtp_ok:
        print(f"\n{Fore.GREEN}{'='*50}")
        print(f"{Fore.GREEN}🎉 DOCKER EMAIL SERVICE IS WORKING! 🎉")
        print(f"{Fore.GREEN}{'='*50}")
        print(f"{Fore.GREEN}✓ You can now use this for Netflix registration")
        print(f"{Fore.CYAN}🌐 Open http://localhost:8025 in your browser to see emails")
        print(f"{Fore.CYAN}📧 SMTP: localhost:1025")
    else:
        print(f"\n{Fore.RED}{'='*50}")
        print(f"{Fore.RED}❌ DOCKER EMAIL SERVICE HAS ISSUES")
        print(f"{Fore.RED}{'='*50}")
        print(f"{Fore.YELLOW}Please check Docker container status:")
        print(f"{Fore.YELLOW}docker-compose ps")
        print(f"{Fore.YELLOW}docker-compose logs mailhog")

if __name__ == "__main__":
    main()

