#!/usr/bin/env python3
"""
Local Temporary Email Service with Docker - Educational Purpose
Uses MailHog Docker container for local temporary email generation
"""

import requests
import time
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Optional, List
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

class LocalTempEmailService:
    def __init__(self):
        """
        Initialize the Local Temporary Email Service
        """
        self.smtp_host = "localhost"
        self.smtp_port = 1025
        self.web_ui_url = "http://localhost:8025"
        self.api_url = "http://localhost:8025/api/v1"
        self.current_email = None
        self.session = requests.Session()
        
    def generate_random_email(self, length: int = 8) -> str:
        """
        Generate a random email address
        
        Args:
            length (int): Length of the random part
            
        Returns:
            str: Random email address
        """
        # Generate random string
        random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        
        # Use local domain
        domain = "fmail.com"
        return f"{random_part}@{domain}"
    
    def check_service_status(self) -> bool:
        """
        Check if MailHog service is running
        
        Returns:
            bool: True if service is running
        """
        try:
            response = self.session.get(f"{self.api_url}/messages", timeout=5)
            if response.status_code == 200:
                print(f"{Fore.GREEN}✓ MailHog service is running")
                return True
            else:
                print(f"{Fore.RED}✗ MailHog service not responding")
                return False
        except Exception as e:
            print(f"{Fore.RED}✗ MailHog service not available: {str(e)}")
            return False
    
    def create_temporary_email(self) -> Dict:
        """
        Create a temporary email address
        
        Returns:
            Dict: Email information
        """
        print(f"{Fore.MAGENTA}=== Creating Local Temporary Email ===")
        
        # Check if service is running
        if not self.check_service_status():
            return {
                'email': None,
                'service': 'Local MailHog',
                'status': 'error',
                'error': 'MailHog service not running'
            }
        
        # Generate random email
        email = self.generate_random_email()
        self.current_email = email
        
        print(f"{Fore.GREEN}✓ Local temporary email created: {email}")
        print(f"{Fore.CYAN}Web UI: {self.web_ui_url}")
        print(f"{Fore.CYAN}SMTP: {self.smtp_host}:{self.smtp_port}")
        
        return {
            'email': email,
            'service': 'Local MailHog',
            'status': 'success',
            'web_ui': self.web_ui_url,
            'smtp_host': self.smtp_host,
            'smtp_port': self.smtp_port
        }
    
    def send_test_email(self, to_email: str, subject: str = "Test Email", body: str = "This is a test email from local temp email service") -> bool:
        """
        Send a test email to verify the service works
        
        Args:
            to_email (str): Email address to send to
            subject (str): Email subject
            body (str): Email body
            
        Returns:
            bool: True if email sent successfully
        """
        try:
            print(f"{Fore.MAGENTA}=== Sending Test Email ===")
            print(f"{Fore.CYAN}To: {to_email}")
            print(f"{Fore.CYAN}Subject: {subject}")
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = "test@localhost"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email via SMTP
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.send_message(msg)
            
            print(f"{Fore.GREEN}✓ Test email sent successfully")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}✗ Failed to send test email: {str(e)}")
            return False
    
    def get_messages(self) -> List[Dict]:
        """
        Get all messages from MailHog
        
        Returns:
            List[Dict]: List of messages
        """
        try:
            print(f"{Fore.MAGENTA}=== Getting Messages ===")
            
            response = self.session.get(f"{self.api_url}/messages")
            if response.status_code == 200:
                messages = response.json()
                print(f"{Fore.GREEN}✓ Found {len(messages)} messages")
                
                formatted_messages = []
                for msg in messages:
                    formatted_msg = {
                        'id': msg.get('ID', ''),
                        'from': msg.get('From', {}).get('Mailbox', '') + '@' + msg.get('From', {}).get('Domain', ''),
                        'to': [to.get('Mailbox', '') + '@' + to.get('Domain', '') for to in msg.get('To', [])],
                        'subject': msg.get('Content', {}).get('Headers', {}).get('Subject', [''])[0],
                        'date': msg.get('Created', ''),
                        'body': msg.get('Content', {}).get('Body', '')
                    }
                    formatted_messages.append(formatted_msg)
                
                return formatted_messages
            else:
                print(f"{Fore.RED}✗ Failed to get messages: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"{Fore.RED}✗ Error getting messages: {str(e)}")
            return []
    
    def wait_for_email(self, max_wait_time: int = 60, check_interval: int = 5) -> Optional[Dict]:
        """
        Wait for an email to arrive
        
        Args:
            max_wait_time (int): Maximum time to wait in seconds
            check_interval (int): Time between checks in seconds
            
        Returns:
            Optional[Dict]: Email message if received
        """
        print(f"{Fore.MAGENTA}=== Waiting for Email ===")
        print(f"{Fore.CYAN}Email: {self.current_email}")
        print(f"{Fore.CYAN}Max wait time: {max_wait_time} seconds")
        
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            messages = self.get_messages()
            
            # Look for emails to our address
            for msg in messages:
                if self.current_email in msg['to']:
                    print(f"{Fore.GREEN}✓ Email received!")
                    print(f"{Fore.GREEN}From: {msg['from']}")
                    print(f"{Fore.GREEN}Subject: {msg['subject']}")
                    return msg
            
            elapsed = int(time.time() - start_time)
            print(f"{Fore.YELLOW}Waiting for email... ({elapsed}s elapsed)")
            time.sleep(check_interval)
        
        print(f"{Fore.RED}✗ Timeout waiting for email")
        return None
    
    def clear_messages(self) -> bool:
        """
        Clear all messages from MailHog
        
        Returns:
            bool: True if cleared successfully
        """
        try:
            print(f"{Fore.MAGENTA}=== Clearing Messages ===")
            
            response = self.session.delete(f"{self.api_url}/messages")
            if response.status_code == 200:
                print(f"{Fore.GREEN}✓ Messages cleared successfully")
                return True
            else:
                print(f"{Fore.RED}✗ Failed to clear messages: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}✗ Error clearing messages: {str(e)}")
            return False

def main():
    """
    Main function to test the local temporary email service
    """
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}Local Temporary Email Service Test - Educational Purpose")
    print(f"{Fore.CYAN}{'='*60}")
    
    # Initialize service
    email_service = LocalTempEmailService()
    
    try:
        # Test 1: Check service status
        print(f"\n{Fore.BLUE}Test 1: Checking service status...")
        if not email_service.check_service_status():
            print(f"{Fore.RED}✗ MailHog service is not running!")
            print(f"{Fore.YELLOW}Please run: docker-compose up -d")
            return
        
        # Test 2: Create temporary email
        print(f"\n{Fore.BLUE}Test 2: Creating temporary email...")
        email_result = email_service.create_temporary_email()
        
        if email_result['status'] != 'success':
            print(f"{Fore.RED}✗ Failed to create email: {email_result.get('error', 'Unknown error')}")
            return
        
        # Test 3: Send test email
        print(f"\n{Fore.BLUE}Test 3: Sending test email...")
        if email_service.send_test_email(email_result['email'], "Netflix Registration Test", "This is a test email for Netflix registration"):
            print(f"{Fore.GREEN}✓ Test email sent successfully")
        else:
            print(f"{Fore.RED}✗ Failed to send test email")
            return
        
        # Test 4: Wait for email
        print(f"\n{Fore.BLUE}Test 4: Waiting for email...")
        received_email = email_service.wait_for_email(max_wait_time=30)
        
        if received_email:
            print(f"{Fore.GREEN}✓ Email received successfully!")
            print(f"{Fore.GREEN}From: {received_email['from']}")
            print(f"{Fore.GREEN}Subject: {received_email['subject']}")
            print(f"{Fore.GREEN}Body: {received_email['body'][:100]}...")
        else:
            print(f"{Fore.RED}✗ No email received")
        
        # Test 5: Get all messages
        print(f"\n{Fore.BLUE}Test 5: Getting all messages...")
        all_messages = email_service.get_messages()
        print(f"{Fore.GREEN}✓ Total messages: {len(all_messages)}")
        
        # Test 6: Clear messages
        print(f"\n{Fore.BLUE}Test 6: Clearing messages...")
        email_service.clear_messages()
        
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}🎉 ALL TESTS COMPLETED SUCCESSFULLY! 🎉")
        print(f"{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}✓ Local temporary email service is working correctly")
        print(f"{Fore.GREEN}✓ You can now use this service for Netflix registration")
        print(f"{Fore.CYAN}Web UI: {email_service.web_ui_url}")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Test stopped by user")
    except Exception as e:
        print(f"\n{Fore.RED}An error occurred: {str(e)}")
    
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}Local email service test completed")
    print(f"{Fore.CYAN}{'='*60}")

if __name__ == "__main__":
    main()

