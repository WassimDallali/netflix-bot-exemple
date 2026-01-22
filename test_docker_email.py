#!/usr/bin/env python3
"""
Quick Docker Email Service Test
Tests if the Docker-based temporary email service is working
"""

import subprocess
import time
import requests
from colorama import init, Fore

init(autoreset=True)

def check_docker_running():
    """Check if Docker is running"""
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"{Fore.GREEN}✓ Docker is installed: {result.stdout.strip()}")
            return True
        else:
            print(f"{Fore.RED}✗ Docker is not installed or not running")
            return False
    except FileNotFoundError:
        print(f"{Fore.RED}✗ Docker is not installed")
        return False

def check_docker_compose():
    """Check if Docker Compose is available"""
    try:
        result = subprocess.run(['docker-compose', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"{Fore.GREEN}✓ Docker Compose is available: {result.stdout.strip()}")
            return True
        else:
            print(f"{Fore.RED}✗ Docker Compose is not available")
            return False
    except FileNotFoundError:
        print(f"{Fore.RED}✗ Docker Compose is not installed")
        return False

def start_email_service():
    """Start the email service using Docker Compose"""
    try:
        print(f"{Fore.YELLOW}Starting MailHog email service...")
        result = subprocess.run(['docker-compose', 'up', '-d'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"{Fore.GREEN}✓ Email service started successfully")
            return True
        else:
            print(f"{Fore.RED}✗ Failed to start email service: {result.stderr}")
            return False
    except Exception as e:
        print(f"{Fore.RED}✗ Error starting email service: {str(e)}")
        return False

def check_service_health():
    """Check if the email service is healthy"""
    try:
        # Wait a moment for service to start
        time.sleep(3)
        
        # Check MailHog API
        response = requests.get("http://localhost:8025/api/v1/messages", timeout=5)
        if response.status_code == 200:
            print(f"{Fore.GREEN}✓ MailHog service is healthy and responding")
            return True
        else:
            print(f"{Fore.RED}✗ MailHog service not responding (status: {response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}✗ Cannot connect to MailHog service")
        return False
    except Exception as e:
        print(f"{Fore.RED}✗ Error checking service health: {str(e)}")
        return False

def show_service_info():
    """Show service information"""
    print(f"\n{Fore.CYAN}{'='*50}")
    print(f"{Fore.CYAN}EMAIL SERVICE INFORMATION")
    print(f"{Fore.CYAN}{'='*50}")
    print(f"{Fore.WHITE}🌐 Web UI: http://localhost:8025")
    print(f"{Fore.WHITE}📧 SMTP: localhost:1025")
    print(f"{Fore.WHITE}🔧 API: http://localhost:8025/api/v1")
    print(f"{Fore.YELLOW}📝 You can now run: python local_temp_email.py")

def main():
    """Main test function"""
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}Docker Email Service Quick Test")
    print(f"{Fore.CYAN}{'='*60}")
    
    # Step 1: Check Docker
    print(f"\n{Fore.BLUE}Step 1: Checking Docker...")
    if not check_docker_running():
        return
    
    # Step 2: Check Docker Compose
    print(f"\n{Fore.BLUE}Step 2: Checking Docker Compose...")
    if not check_docker_compose():
        return
    
    # Step 3: Start email service
    print(f"\n{Fore.BLUE}Step 3: Starting email service...")
    if not start_email_service():
        return
    
    # Step 4: Check service health
    print(f"\n{Fore.BLUE}Step 4: Checking service health...")
    if not check_service_health():
        print(f"{Fore.YELLOW}⚠️ Service might still be starting, please wait a moment and try again")
        return
    
    # Step 5: Show service info
    show_service_info()
    
    print(f"\n{Fore.GREEN}{'='*60}")
    print(f"{Fore.GREEN}🎉 DOCKER EMAIL SERVICE IS READY! 🎉")
    print(f"{Fore.GREEN}{'='*60}")
    print(f"{Fore.GREEN}✓ MailHog is running in Docker")
    print(f"{Fore.GREEN}✓ Web interface available at http://localhost:8025")
    print(f"{Fore.GREEN}✓ SMTP server running on localhost:1025")
    print(f"{Fore.GREEN}✓ Ready for Netflix registration bot!")

if __name__ == "__main__":
    main()

