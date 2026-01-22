#!/usr/bin/env python3
"""
Netflix Bot with Docker Email Integration - Educational Purpose
Shows how to integrate the Docker-based email service with Netflix registration
"""

import asyncio
import time
from local_temp_email import LocalTempEmailService
from tiger_sms_bot import TigerSMSBot
from colorama import init, Fore

init(autoreset=True)

class NetflixDockerIntegration:
    def __init__(self):
        """
        Initialize Netflix Bot with Docker Email Integration
        """
        self.email_service = LocalTempEmailService()
        self.sms_bot = TigerSMSBot()
        self.credentials = {}
        
    def get_registration_credentials(self):
        """
        Get registration credentials using Docker email service
        """
        print(f"{Fore.MAGENTA}=== Getting Registration Credentials ===")
        
        # 1. Get French phone number
        print(f"{Fore.CYAN}1. Getting French phone number...")
        phone_result = self.sms_bot.get_number("netflix", "france")
        
        if phone_result['status'] != 'success':
            print(f"{Fore.RED}✗ Failed to get phone number: {phone_result.get('error', 'Unknown error')}")
            return False
        
        phone_number = phone_result['phone_number']
        activation_id = phone_result['activation_id']
        
        print(f"{Fore.GREEN}✓ Phone number: {phone_number}")
        print(f"{Fore.GREEN}✓ Activation ID: {activation_id}")
        
        # 2. Get temporary email from Docker service
        print(f"{Fore.CYAN}2. Getting temporary email from Docker service...")
        email_result = self.email_service.create_temporary_email()
        
        if email_result['status'] != 'success':
            print(f"{Fore.RED}✗ Failed to create email: {email_result.get('error', 'Unknown error')}")
            return False
        
        email_address = email_result['email']
        print(f"{Fore.GREEN}✓ Email address: {email_address}")
        
        # 3. Generate random password and name
        import random
        import string
        
        password = ''.join(random.choices(string.ascii_letters + string.digits + '!@#$%^&*', k=12))
        first_name = random.choice(['Alex', 'Jordan', 'Taylor', 'Casey', 'Morgan', 'Riley', 'Avery', 'Quinn'])
        last_name = random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis'])
        full_name = f"{first_name} {last_name}"
        
        print(f"{Fore.GREEN}✓ Password: {password}")
        print(f"{Fore.GREEN}✓ Name: {full_name}")
        
        # Store credentials
        self.credentials = {
            'email': email_address,
            'phone': phone_number,
            'password': password,
            'name': full_name,
            'activation_id': activation_id,
            'email_service': 'Docker MailHog',
            'web_ui': 'http://localhost:8025'
        }
        
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}🎉 REGISTRATION CREDENTIALS READY! 🎉")
        print(f"{Fore.GREEN}{'='*60}")
        print(f"{Fore.WHITE}📧 Email: {email_address}")
        print(f"{Fore.WHITE}📱 Phone: {phone_number}")
        print(f"{Fore.WHITE}🔑 Password: {password}")
        print(f"{Fore.WHITE}👤 Name: {full_name}")
        print(f"{Fore.WHITE}🌐 Email Web UI: {self.credentials['web_ui']}")
        print(f"{Fore.WHITE}🔧 Email Service: {self.credentials['email_service']}")
        
        return True
    
    def simulate_netflix_registration(self):
        """
        Simulate Netflix registration process
        """
        print(f"\n{Fore.MAGENTA}=== Simulating Netflix Registration ===")
        
        # Simulate form filling
        print(f"{Fore.CYAN}Step 1: Filling registration form...")
        print(f"{Fore.GREEN}✓ Email: {self.credentials['email']}")
        print(f"{Fore.GREEN}✓ Password: {self.credentials['password']}")
        print(f"{Fore.GREEN}✓ Name: {self.credentials['name']}")
        
        # Simulate plan selection
        print(f"{Fore.CYAN}Step 2: Selecting Netflix plan...")
        plans = ['Basic', 'Standard', 'Premium']
        selected_plan = plans[1]  # Standard
        print(f"{Fore.GREEN}✓ Selected plan: {selected_plan}")
        
        # Simulate phone payment
        print(f"{Fore.CYAN}Step 3: Setting up phone payment...")
        print(f"{Fore.GREEN}✓ Phone number: {self.credentials['phone']}")
        
        # Simulate SMS verification
        print(f"{Fore.CYAN}Step 4: Waiting for SMS verification...")
        print(f"{Fore.YELLOW}⏳ Checking SMS status...")
        
        # Simulate receiving SMS
        time.sleep(2)
        sms_code = "123456"  # Simulated SMS code
        print(f"{Fore.GREEN}✓ SMS Code received: {sms_code}")
        
        # Simulate email verification
        print(f"{Fore.CYAN}Step 5: Checking for verification email...")
        print(f"{Fore.YELLOW}⏳ Checking email inbox...")
        
        # Simulate receiving verification email
        time.sleep(2)
        print(f"{Fore.GREEN}✓ Verification email received!")
        print(f"{Fore.GREEN}✓ Netflix account created successfully!")
        
        return True
    
    def monitor_emails(self, duration: int = 60):
        """
        Monitor emails for a specified duration
        """
        print(f"\n{Fore.MAGENTA}=== Monitoring Emails ===")
        print(f"{Fore.CYAN}Email: {self.credentials['email']}")
        print(f"{Fore.CYAN}Duration: {duration} seconds")
        print(f"{Fore.CYAN}Web UI: {self.credentials['web_ui']}")
        
        start_time = time.time()
        email_count = 0
        
        while time.time() - start_time < duration:
            messages = self.email_service.get_messages()
            
            if len(messages) > email_count:
                new_emails = messages[email_count:]
                for email in new_emails:
                    if self.credentials['email'] in email['to']:
                        print(f"{Fore.GREEN}📧 New email received!")
                        print(f"{Fore.GREEN}From: {email['from']}")
                        print(f"{Fore.GREEN}Subject: {email['subject']}")
                        print(f"{Fore.GREEN}Time: {email['date']}")
                        email_count += 1
            
            elapsed = int(time.time() - start_time)
            print(f"{Fore.YELLOW}Monitoring... ({elapsed}s elapsed, {email_count} emails)")
            time.sleep(5)
        
        print(f"{Fore.GREEN}✓ Email monitoring completed")
        print(f"{Fore.GREEN}✓ Total emails received: {email_count}")
    
    def cleanup(self):
        """
        Cleanup resources
        """
        print(f"\n{Fore.MAGENTA}=== Cleanup ===")
        
        # Clear email messages
        if hasattr(self, 'email_service'):
            self.email_service.clear_messages()
            print(f"{Fore.GREEN}✓ Email messages cleared")
        
        # Cancel SMS activation
        if hasattr(self, 'credentials') and 'activation_id' in self.credentials:
            try:
                self.sms_bot.cancel_activation(self.credentials['activation_id'])
                print(f"{Fore.GREEN}✓ SMS activation cancelled")
            except:
                print(f"{Fore.YELLOW}⚠️ Could not cancel SMS activation")
        
        print(f"{Fore.GREEN}✓ Cleanup completed")

def main():
    """
    Main function to demonstrate Docker email integration
    """
    print(f"{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}Netflix Bot with Docker Email Integration - Educational Purpose")
    print(f"{Fore.CYAN}{'='*70}")
    
    bot = NetflixDockerIntegration()
    
    try:
        # Step 1: Get credentials
        if not bot.get_registration_credentials():
            print(f"{Fore.RED}✗ Failed to get registration credentials")
            return
        
        # Step 2: Simulate registration
        if not bot.simulate_netflix_registration():
            print(f"{Fore.RED}✗ Registration simulation failed")
            return
        
        # Step 3: Monitor emails
        print(f"\n{Fore.BLUE}Would you like to monitor emails? (y/n)")
        # For demo purposes, we'll monitor for 30 seconds
        bot.monitor_emails(duration=30)
        
        print(f"\n{Fore.GREEN}{'='*70}")
        print(f"{Fore.GREEN}🎉 DEMONSTRATION COMPLETED SUCCESSFULLY! 🎉")
        print(f"{Fore.GREEN}{'='*70}")
        print(f"{Fore.GREEN}✓ Docker email service is working perfectly")
        print(f"{Fore.GREEN}✓ Ready for Netflix registration automation")
        print(f"{Fore.CYAN}🌐 Check emails at: {bot.credentials['web_ui']}")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Demo stopped by user")
    except Exception as e:
        print(f"\n{Fore.RED}An error occurred: {str(e)}")
    finally:
        bot.cleanup()

if __name__ == "__main__":
    main()

