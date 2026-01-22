#!/usr/bin/env python3
"""
Temporary Email Generator with Playwright - Educational Purpose
Creates disposable email addresses using web automation
"""

import asyncio
import time
import random
import string
from typing import Dict, Optional, List
from colorama import init, Fore, Style
from playwright.async_api import async_playwright, Browser, Page
from fake_useragent import UserAgent

# Initialize colorama for colored output
init(autoreset=True)

class TempEmailGenerator:
    def __init__(self):
        """
        Initialize the Temporary Email Generator
        """
        self.browser = None
        self.page = None
        self.current_email = None
        self.current_service = None
        self.ua = UserAgent()
        
        # Multiple temporary email services
        self.email_services = [
            {
                'name': 'TempMail',
                'url': 'https://temp-mail.org',
                'email_selector': '#mail',
                'refresh_selector': '.fa-refresh',
                'inbox_selector': '.mail',
                'subject_selector': '.subject',
                'from_selector': '.from'
            },
            {
                'name': '10MinuteMail',
                'url': 'https://10minutemail.com',
                'email_selector': '#mailAddress',
                'refresh_selector': '#reload',
                'inbox_selector': '.mail',
                'subject_selector': '.subject',
                'from_selector': '.from'
            },
            {
                'name': 'GuerrillaMail',
                'url': 'https://www.guerrillamail.com',
                'email_selector': '#email-widget',
                'refresh_selector': '#refresh',
                'inbox_selector': '.mail',
                'subject_selector': '.subject',
                'from_selector': '.from'
            },
            {
                'name': 'MailDrop',
                'url': 'https://maildrop.cc',
                'email_selector': '#inboxid',
                'refresh_selector': '#refresh',
                'inbox_selector': '.mail',
                'subject_selector': '.subject',
                'from_selector': '.from'
            }
        ]
    
    async def start_browser(self):
        """
        Start Playwright browser
        """
        print(f"{Fore.YELLOW}Starting browser...")
        playwright = await async_playwright().start()
        
        # Use Chromium with stealth settings
        self.browser = await playwright.chromium.launch(
            headless=False,  # Set to True for headless mode
            args=[
                '--no-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]
        )
        
        # Create context with realistic settings
        context = await self.browser.new_context(
            user_agent=self.ua.random,
            viewport={'width': 1920, 'height': 1080},
            locale='en-US',
            timezone_id='America/New_York'
        )
        
        self.page = await context.new_page()
        
        # Add stealth scripts
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)
        
        print(f"{Fore.GREEN}✓ Browser started successfully")
    
    async def close_browser(self):
        """
        Close Playwright browser
        """
        if self.browser:
            await self.browser.close()
            print(f"{Fore.YELLOW}Browser closed")
    
    async def get_temp_mail_email(self) -> Optional[Dict]:
        """
        Get email from TempMail.org using Playwright
        
        Returns:
            Optional[Dict]: Email information
        """
        try:
            print(f"{Fore.YELLOW}Trying TempMail.org...")
            
            await self.page.goto('https://temp-mail.org', wait_until='domcontentloaded', timeout=10000)
            await self.page.wait_for_timeout(3000)
            
            # Try multiple selectors for email
            email_selectors = [
                '#mail',
                'input[type="email"]',
                '.email-address',
                '#email',
                '[data-clipboard-text]'
            ]
            
            email = None
            for selector in email_selectors:
                try:
                    email_element = await self.page.query_selector(selector)
                    if email_element:
                        # Try different methods to get email
                        email = await email_element.input_value() or await email_element.get_attribute('value') or await email_element.get_attribute('data-clipboard-text')
                        if email and '@' in email:
                            break
                except:
                    continue
            
            if email and '@' in email:
                self.current_email = email
                self.current_service = 'TempMail'
                
                print(f"{Fore.GREEN}✓ TempMail email: {email}")
                return {
                    'email': email,
                    'service': 'TempMail',
                    'status': 'success',
                    'url': 'https://temp-mail.org'
                }
            
            print(f"{Fore.RED}✗ Failed to get TempMail email")
            return None
            
        except Exception as e:
            print(f"{Fore.RED}TempMail error: {str(e)}")
            return None
    
    async def get_10minutemail_email(self) -> Optional[Dict]:
        """
        Get email from 10MinuteMail using Playwright
        
        Returns:
            Optional[Dict]: Email information
        """
        try:
            print(f"{Fore.YELLOW}Trying 10MinuteMail...")
            
            await self.page.goto('https://10minutemail.com', wait_until='networkidle')
            await self.page.wait_for_timeout(2000)
            
            # Get the email address
            email_element = await self.page.query_selector('#mailAddress')
            if email_element:
                email = await email_element.input_value()
                if email and '@' in email:
                    self.current_email = email
                    self.current_service = '10MinuteMail'
                    
                    print(f"{Fore.GREEN}✓ 10MinuteMail email: {email}")
                    return {
                        'email': email,
                        'service': '10MinuteMail',
                        'status': 'success',
                        'url': 'https://10minutemail.com'
                    }
            
            print(f"{Fore.RED}✗ Failed to get 10MinuteMail email")
            return None
            
        except Exception as e:
            print(f"{Fore.RED}10MinuteMail error: {str(e)}")
            return None
    
    async def get_guerrilla_email(self) -> Optional[Dict]:
        """
        Get email from GuerrillaMail using Playwright
        
        Returns:
            Optional[Dict]: Email information
        """
        try:
            print(f"{Fore.YELLOW}Trying GuerrillaMail...")
            
            await self.page.goto('https://www.guerrillamail.com', wait_until='networkidle')
            await self.page.wait_for_timeout(2000)
            
            # Get the email address
            email_element = await self.page.query_selector('#email-widget')
            if email_element:
                email = await email_element.input_value()
                if email and '@' in email:
                    self.current_email = email
                    self.current_service = 'GuerrillaMail'
                    
                    print(f"{Fore.GREEN}✓ GuerrillaMail email: {email}")
                    return {
                        'email': email,
                        'service': 'GuerrillaMail',
                        'status': 'success',
                        'url': 'https://www.guerrillamail.com'
                    }
            
            print(f"{Fore.RED}✗ Failed to get GuerrillaMail email")
            return None
            
        except Exception as e:
            print(f"{Fore.RED}GuerrillaMail error: {str(e)}")
            return None
    
    async def get_maildrop_email(self) -> Optional[Dict]:
        """
        Get email from MailDrop using Playwright
        
        Returns:
            Optional[Dict]: Email information
        """
        try:
            print(f"{Fore.YELLOW}Trying MailDrop...")
            
            await self.page.goto('https://maildrop.cc', wait_until='networkidle')
            await self.page.wait_for_timeout(2000)
            
            # Get the email address
            email_element = await self.page.query_selector('#inboxid')
            if email_element:
                email = await email_element.input_value()
                if email and '@' in email:
                    self.current_email = email
                    self.current_service = 'MailDrop'
                    
                    print(f"{Fore.GREEN}✓ MailDrop email: {email}")
                    return {
                        'email': email,
                        'service': 'MailDrop',
                        'status': 'success',
                        'url': 'https://maildrop.cc'
                    }
            
            print(f"{Fore.RED}✗ Failed to get MailDrop email")
            return None
            
        except Exception as e:
            print(f"{Fore.RED}MailDrop error: {str(e)}")
            return None
    
    async def get_temporary_email(self) -> Optional[Dict]:
        """
        Get a temporary email address from available services
        
        Returns:
            Optional[Dict]: Email information
        """
        print(f"{Fore.MAGENTA}=== Getting Temporary Email ===")
        
        # Try different services in order
        services = [
            self.get_temp_mail_email,
            self.get_10minutemail_email,
            self.get_guerrilla_email,
            self.get_maildrop_email
        ]
        
        for service_func in services:
            try:
                result = await service_func()
                if result and result['status'] == 'success':
                    return result
            except Exception as e:
                print(f"{Fore.RED}Service error: {str(e)}")
                continue
        
        # If all web services fail, generate a random email
        print(f"{Fore.YELLOW}All web services failed, generating random email...")
        email = await self.generate_random_email()
        
        self.current_email = email
        self.current_service = 'Random'
        
        print(f"{Fore.GREEN}✓ Random email generated: {email}")
        return {
            'email': email,
            'service': 'Random',
            'status': 'success',
            'url': 'Generated locally'
        }
    
    async def check_email_inbox(self, max_emails: int = 10) -> List[Dict]:
        """
        Check email inbox for messages
        
        Args:
            max_emails (int): Maximum number of emails to retrieve
            
        Returns:
            List[Dict]: List of emails
        """
        if not self.current_email:
            print(f"{Fore.RED}No email address to check")
            return []
        
        print(f"{Fore.MAGENTA}=== Checking Email Inbox ===")
        print(f"{Fore.CYAN}Email: {self.current_email}")
        
        try:
            # Refresh the inbox
            refresh_button = await self.page.query_selector('.fa-refresh, #reload, #refresh')
            if refresh_button:
                await refresh_button.click()
                await self.page.wait_for_timeout(2000)
            
            # Get emails from inbox
            emails = []
            email_elements = await self.page.query_selector_all('.mail, .message, .email')
            
            for i, email_element in enumerate(email_elements[:max_emails]):
                try:
                    # Extract email details
                    subject_element = await email_element.query_selector('.subject, .mail-subject')
                    from_element = await email_element.query_selector('.from, .mail-from')
                    time_element = await email_element.query_selector('.time, .mail-time')
                    
                    subject = await subject_element.inner_text() if subject_element else "No subject"
                    sender = await from_element.inner_text() if from_element else "Unknown sender"
                    time_text = await time_element.inner_text() if time_element else "Unknown time"
                    
                    emails.append({
                        'subject': subject.strip(),
                        'from': sender.strip(),
                        'time': time_text.strip(),
                        'index': i + 1
                    })
                    
                except Exception as e:
                    print(f"{Fore.YELLOW}Error parsing email {i+1}: {str(e)}")
                    continue
            
            print(f"{Fore.GREEN}✓ Found {len(emails)} emails")
            return emails
            
        except Exception as e:
            print(f"{Fore.RED}Error checking inbox: {str(e)}")
            return []
    
    async def wait_for_netflix_email(self, max_wait_time: int = 300, check_interval: int = 10) -> Optional[Dict]:
        """
        Wait for Netflix verification email
        
        Args:
            max_wait_time (int): Maximum time to wait in seconds
            check_interval (int): Time between checks in seconds
            
        Returns:
            Optional[Dict]: Netflix email information
        """
        print(f"{Fore.MAGENTA}=== Waiting for Netflix Email ===")
        print(f"{Fore.CYAN}Email: {self.current_email}")
        print(f"{Fore.CYAN}Max wait time: {max_wait_time} seconds")
        print(f"{Fore.CYAN}Check interval: {check_interval} seconds")
        
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            print(f"{Fore.YELLOW}Checking for Netflix email... ({int(time.time() - start_time)}s elapsed)")
            
            # Check inbox for emails
            emails = await self.check_email_inbox()
            
            # Look for Netflix emails
            for email in emails:
                if 'netflix' in email['from'].lower() or 'netflix' in email['subject'].lower():
                    print(f"{Fore.GREEN}✓ Netflix email found!")
                    print(f"{Fore.GREEN}From: {email['from']}")
                    print(f"{Fore.GREEN}Subject: {email['subject']}")
                    return email
            
            # Wait before next check
            await asyncio.sleep(check_interval)
        
        print(f"{Fore.RED}Timeout waiting for Netflix email")
        return None
    
    async def generate_random_email(self, length: int = 8) -> str:
        """
        Generate a random email address (fallback method)
        
        Args:
            length (int): Length of the random part
            
        Returns:
            str: Random email address
        """
        # Generate random string
        random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        
        # Common disposable email domains
        domains = [
            'tempmail.org',
            '10minutemail.com',
            'guerrillamail.com',
            'maildrop.cc',
            'yopmail.com',
            'temp-mail.org',
            'throwaway.email',
            'getnada.com'
        ]
        
        domain = random.choice(domains)
        return f"{random_part}@{domain}"

async def main():
    """
    Main function to demonstrate the temporary email generator
    """
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}Temporary Email Generator with Playwright - Educational Purpose")
    print(f"{Fore.CYAN}{'='*60}")
    
    # Initialize generator
    generator = TempEmailGenerator()
    
    try:
        # Start browser
        await generator.start_browser()
        
        # Get temporary email
        print(f"\n{Fore.BLUE}1. Getting temporary email address...")
        email_result = await generator.get_temporary_email()
        
        if email_result and email_result['status'] == 'success':
            print(f"{Fore.GREEN}✓ Temporary email obtained!")
            print(f"{Fore.GREEN}Email: {email_result['email']}")
            print(f"{Fore.GREEN}Service: {email_result['service']}")
            print(f"{Fore.GREEN}URL: {email_result['url']}")
            
            # Display instructions
            print(f"\n{Fore.BLUE}2. Instructions for Netflix registration:")
            print(f"{Fore.YELLOW}1. Go to Netflix signup page: https://www.netflix.com/signup")
            print(f"{Fore.YELLOW}2. Use this email: {email_result['email']}")
            print(f"{Fore.YELLOW}3. Complete the registration form")
            print(f"{Fore.YELLOW}4. Netflix will send a verification email")
            
            # Wait for Netflix email
            print(f"\n{Fore.BLUE}3. Waiting for Netflix verification email...")
            netflix_email = await generator.wait_for_netflix_email(max_wait_time=300)
            
            if netflix_email:
                print(f"{Fore.GREEN}✓ Netflix email detected!")
                print(f"{Fore.GREEN}Please check your email to complete verification")
            else:
                print(f"{Fore.RED}✗ No Netflix email received within timeout")
                print(f"{Fore.YELLOW}You may need to check the email service manually")
                
        else:
            print(f"{Fore.RED}✗ Failed to get temporary email")
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Generator stopped by user")
    except Exception as e:
        print(f"\n{Fore.RED}An error occurred: {str(e)}")
    finally:
        # Close browser
        await generator.close_browser()
    
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}Email generator execution completed")
    print(f"{Fore.CYAN}{'='*60}")

if __name__ == "__main__":
    asyncio.run(main())
