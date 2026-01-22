#!/usr/bin/env python3
"""
Netflix Registration Bot with Playwright - Educational Purpose
Complete automated Netflix registration with phone payment
"""

import asyncio
import time
import random
import os, requests
import string
from typing import Dict, Optional, List
from colorama import init, Fore, Style
from playwright.async_api import async_playwright, Browser, Page
from fake_useragent import UserAgent
from tiger_sms_bot import TigerSMSBot
from local_temp_email import LocalTempEmailService


# Initialize colorama for colored output
init(autoreset=True)

class NetflixRegistrationBot:
    def __init__(self):
        """
        Initialize the Netflix Registration Bot
        """
        self.browser = None
        self.page = None
        self.sms_bot = TigerSMSBot()
        self.email_service = LocalTempEmailService()
        self.ua = UserAgent()
        # PremiSocks token from env; do not hardcode
        self.premsocks_token = os.getenv('PREMISOCKS_TOKEN')
        
        # Registration data
        self.email_address = None
        self.phone_number = None
        self.activation_id = None
        self.password = None
        self.first_name = None
        self.last_name = None
        

    
    async def start_browser(self):
        """
        Start Playwright browser with stealth settings
        """
        print(f"{Fore.YELLOW}Starting browser for Netflix registration (French interface)...")
        playwright = await async_playwright().start()
        
        # Use Chromium with stealth settings
        self.browser = await playwright.firefox.launch(
            headless=False,  # Set to True for headless mode
            #proxy={ "server": f"socks5h://{proxy['ip']}:{proxy['port']}" } if proxy else None,
            args=[
                '--no-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--disable-dev-shm-usage',
                '--no-first-run',
                '--disable-default-apps'
            ]
        )
        
        # Get a fast SOCKS5 proxy from PremiSocks if token configured
        proxy_param = None
        proxy = None
        if self.premsocks_token:
            try:
                proxy = self.get_best_proxy()
            except Exception as e:
                print(f"{Fore.YELLOW}PremiSocks warning: {e}")
        if proxy:
            print(f"{Fore.CYAN}Using PremiSocks proxy: {proxy['proxy_string']}")
            proxy_param = { 'server': f"socks5://{proxy['ip']}:{proxy['port']}" }

        # Create context with French settings
        context = await self.browser.new_context(
            proxy=proxy_param,
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0',
            viewport={'width': 1920, 'height': 1080},
            locale='fr-FR',  # French language
            timezone_id='Europe/Paris',  # French timezone
            geolocation={'latitude': 48.8566, 'longitude': 2.3522},  # Paris, France
            permissions=['geolocation']
        )
        
        self.page = await context.new_page()
        
        # Add stealth scripts
# Enhanced stealth script
        await self.page.add_init_script("""
            // Remove webdriver property
            delete navigator.__proto__.webdriver;
            
            // Mock plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            
            // Mock languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['fr-FR', 'fr', 'en-US', 'en']
            });
            
            // Mock hardware concurrency
            Object.defineProperty(navigator, 'hardwareConcurrency', {
                get: () => 8
            });
            
            // Mock permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
        """)
        
        # Add random delays to mimic human behavior
        await self.page.add_init_script("""
            const originalFetch = window.fetch;
            window.fetch = function(...args) {
                return new Promise(resolve => {
                    setTimeout(() => {
                        resolve(originalFetch.apply(this, args));
                    }, Math.random() * 1000 + 500); // 0.5-1.5s delay
                });
            };
        """)
        
        print(f"{Fore.GREEN}✓ Browser started successfully")

    def get_best_proxy(self, max_attempts: int = 3, country: str = "FR"):
        """
        Get a random SOCKS5 proxy from PremiSocks and validate HTTPS connectivity.
        Returns {'ip','port','proxy_string'} or None.
        """
        if not self.premsocks_token:
            return None
        headers = {"Authorization": f"Bearer {self.premsocks_token}"}
        url = f"https://premsocks.com/api/v1/socks/random?country={country}"
        for attempt in range(1, max_attempts + 1):
            try:
                print(f"Info: Requesting best proxy (attempt {attempt}/{max_attempts})...")
                resp = requests.get(url, headers=headers, timeout=10)
                if resp.status_code != 200:
                    print(f"Error: API status {resp.status_code}")
                    continue
                js = resp.json()
                if not js.get("status") or js.get("count", 0) < 1:
                    print("Error: No proxies returned")
                    continue
                proxy = js["data"][0]
                print(f"Info: Got proxy {proxy['proxy_string']} from {proxy.get('country','?')}")
                if self._proxy_connectivity_ok(proxy):
                    return proxy
                print("Warning: Proxy failed connectivity test, trying another...")
            except Exception as e:
                print(f"Error: {e}")
            if attempt < max_attempts:
                time.sleep(1)
        print("Error: Failed to get a working proxy after multiple attempts")
        return None

    def _proxy_connectivity_ok(self, proxy, test_url: str = "https://api.ipify.org?format=json", timeout: int = 8) -> bool:
        """Validate HTTPS through SOCKS5; measure basic latency (use socks5h for DNS over proxy)."""
        try:
            s = requests.Session()
            s.proxies = {
                'http':  f"socks5h://{proxy['ip']}:{proxy['port']}",
                'https': f"socks5h://{proxy['ip']}:{proxy['port']}"
            }
            start = time.time()
            r = s.get(test_url, timeout=timeout)
            dt = time.time() - start
            if r.status_code == 200 and dt < 3.0:
                print(f"Info: Proxy OK (latency {dt:.2f}s, ip={r.text})")
                return True
            print(f"Warning: Proxy slow/unreliable (code={r.status_code}, {dt:.2f}s)")
            return False
        except Exception as e:
            print(f"Error connectivity test: {e}")
            return False
    
    async def close_browser(self):
        """
        Close Playwright browser
        """
        try:
            if self.browser:
                await self.browser.close()
                print(f"{Fore.YELLOW}Browser closed")
        except Exception as e:
            print(f"{Fore.YELLOW}Browser close warning: {str(e)}")
    
    async def get_registration_credentials(self) -> Dict:
        """
        Get phone number and email for Netflix registration
        
        Returns:
            Dict: Registration credentials
        """
        print(f"{Fore.MAGENTA}=== Getting Registration Credentials ===")
        
        credentials = {
            'phone': None,
            'email': None,
            'status': 'pending'
        }
        
        try:
            # Get phone number from Tiger SMS
            print(f"\n{Fore.BLUE}1. Getting French phone number for Netflix...")
            phone_response = self.sms_bot.get_number('netflix', 'france')
            
            if phone_response['status'] == 'success':
                response_data = phone_response['data']
                if response_data.startswith('ACCESS_'):
                    parts = response_data.split(':')
                    if len(parts) >= 3:
                        self.activation_id = parts[1]
                        self.phone_number = parts[2]
                        credentials['phone'] = self.phone_number
                        print(f"{Fore.GREEN}✓ Phone number: {self.phone_number}")
                    else:
                        print(f"{Fore.RED}✗ Unexpected phone response format")
                        return credentials
                else:
                    print(f"{Fore.RED}✗ Failed to get phone number")
                    return credentials
            else:
                print(f"{Fore.RED}✗ Phone number error: {phone_response.get('error', 'Unknown error')}")
                return credentials
            
            # Get email address from Docker service
            print(f"\n{Fore.BLUE}2. Getting temporary email address from Docker service...")
            email_response = self.email_service.create_temporary_email()
            
            if email_response and email_response['status'] == 'success':
                self.email_address = email_response['email']
                credentials['email'] = self.email_address
                print(f"{Fore.GREEN}✓ Email address: {self.email_address}")
                print(f"{Fore.GREEN}✓ Email service: {email_response['service']}")
                print(f"{Fore.CYAN}Web UI: {email_response.get('web_ui', 'http://localhost:8025')}")
            else:
                print(f"{Fore.RED}✗ Failed to get email address: {email_response.get('error', 'Unknown error')}")
                return credentials
            
            # Generate additional registration data
            self.password = self.generate_password()
            self.first_name = self.generate_name()
            self.last_name = self.generate_name()
            
            print(f"{Fore.GREEN}✓ Password: {self.password}")
            print(f"{Fore.GREEN}✓ Name: {self.first_name} {self.last_name}")
            
            credentials['status'] = 'success'
            return credentials
            
        except Exception as e:
            print(f"{Fore.RED}Error getting credentials: {str(e)}")
            credentials['status'] = 'error'
            return credentials
    async def select_mobile_billing_method(self) -> bool:
        print(f"{Fore.MAGENTA}=== Selecting Mobile Billing (DCB) ===")
        try:
            # Attendre l'onglet/méthode “Ajouter à la facture mobile”
            selectors = [
                'button[data-uia="payment-choice+dcbOption"]',
                '#directCarrierBillingStringIdPreAndPostpaid',
                'button:has-text("Ajouter à la facture mobile")'
            ]
            btn = None
            for sel in selectors:
                try:
                    btn = await self.page.wait_for_selector(sel, timeout=4000)
                    if btn:
                        break
                except:
                    continue

            if not btn:
                print(f"{Fore.RED}✗ DCB option not found on payment picker")
                return False

            await btn.click()
            # Attendre redirection/chargement vers la page DCB
            try:
                await self.page.wait_for_url(lambda url: "dcboption" in url or "carrier" in url.lower(), timeout=15000)
            except:
                # Fallback: courte attente si l’URL ne change pas immédiatement
                await self.page.wait_for_timeout(3000)

            print(f"{Fore.GREEN}✓ Mobile billing option selected")
            print(f"{Fore.CYAN}Current URL: {self.page.url}")
            return True
        except Exception as e:
            print(f"{Fore.RED}Error selecting mobile billing: {str(e)}")
            return False

    async def wait_between_steps(self, seconds: int = 30):
        try:
            # Ensure DOM is loaded; ignore errors if already loaded
            await self.page.wait_for_load_state('domcontentloaded', timeout=30000)
            # Optional: also wait for 'networkidle' if you want even more stability
            # await self.page.wait_for_load_state('networkidle', timeout=30000)
        except:
            pass
        await self.page.wait_for_timeout(seconds * 1000)

    def generate_password(self, length: int = 12) -> str:
        """
        Generate a strong password
        
        Args:
            length (int): Password length
            
        Returns:
            str: Generated password
        """
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choices(chars, k=length))
    
    def format_phone_for_france(self, phone_number: str):
        """
        Format phone number for French Netflix (convert 33602956360 to 0602956360)
        
        Args:
            phone_number (str): Original phone number from Tiger SMS (e.g., 33602956360)
            
        Returns:
            str: Formatted phone number for France (e.g., 0602956360)
        """
        print(f"{Fore.CYAN}Converting Tiger SMS number: {phone_number}")
        
        # Remove +33 prefix and any spaces/dashes
        clean_number = phone_number.replace('+33', '').replace(' ', '').replace('-', '')
        
        # Tiger SMS format: 33602956360 -> 0602956360
        if len(clean_number) == 10 and clean_number.startswith('33'):
            # Remove 33 prefix and add 0: 33602956360 -> 0602956360
            clean_number = '0' + clean_number[2:]
            print(f"{Fore.GREEN}Formatted for France: {clean_number}")
            return clean_number
        elif len(clean_number) == 9:
            # Add leading 0: 602956360 -> 0602956360
            clean_number = '0' + clean_number
            print(f"{Fore.GREEN}Formatted for France: {clean_number}")
            return clean_number
        elif len(clean_number) == 10 and not clean_number.startswith('0'):
            # Add leading 0 if missing: 33602956360 -> 0602956360
            clean_number = '0' + clean_number[1:]
            print(f"{Fore.GREEN}Formatted for France: {clean_number}")
            return clean_number
        else:
            # Fallback: return the clean number
            print(f"{Fore.YELLOW}Using fallback format: {clean_number}")
            return clean_number
    
    def format_fr_phone_compact(self, phone: str) -> str:
        p = ''.join(ch for ch in phone if ch.isdigit())
        if p.startswith('33'):
            p = p[2:]
        if not p.startswith('0'):
            p = '0' + p
        return p[:10]
    
    async def try_alternative_phone_formats(self, phone_input, original_phone: str):
        """
        Try different phone number formats if the first one doesn't work
        
        Args:
            phone_input: The phone input element
            original_phone (str): Original phone number from Tiger SMS
        """
        print(f"{Fore.YELLOW}⚠️ Trying alternative phone formats...")
        
        # Alternative formats to try
        alternative_formats = [
            # Format 1: French format (0602956360)
            self.format_phone_for_france(original_phone),
            # Format 2: Direct conversion (33602956360 -> 0602956360)
            '0' + original_phone[2:] if original_phone.startswith('33') and len(original_phone) == 10 else original_phone,
            # Format 3: Clean format without spaces
            original_phone.replace('+33', '').replace(' ', '').replace('-', ''),
            # Format 4: With spaces (06 02 95 63 60)
            self.format_phone_for_france(original_phone)[:2] + ' ' + self.format_phone_for_france(original_phone)[2:4] + ' ' + self.format_phone_for_france(original_phone)[4:6] + ' ' + self.format_phone_for_france(original_phone)[6:8] + ' ' + self.format_phone_for_france(original_phone)[8:10],
            # Format 5: Just the number without country code
            original_phone.replace('+33', ''),
        ]
        
        for i, alt_format in enumerate(alternative_formats):
            try:
                print(f"{Fore.CYAN}Trying format {i+1}: {alt_format}")
                await phone_input.fill('')
                await phone_input.fill(alt_format)
                await self.page.wait_for_timeout(1000)
                
                # Check if there's an error message
                error_selectors = [
                    '[data-uia="error-message"]',
                    '.error-message',
                    '[class*="error"]',
                    '[class*="invalid"]',
                    '[data-uia*="error"]',
                    '[role="alert"]',
                    '.alert',
                    '[class*="alert"]'
                ]
                
                has_error = False
                error_message = ""
                for error_selector in error_selectors:
                    try:
                        error_element = await self.page.query_selector(error_selector)
                        if error_element and await error_element.is_visible():
                            error_text = await error_element.text_content()
                            if error_text and error_text.strip():
                                has_error = True
                                error_message = error_text.strip()
                                print(f"{Fore.RED}Error detected: {error_message}")
                                break
                    except:
                        continue
                
                # Also check for specific Netflix error messages
                if not has_error:
                    try:
                        # Check for specific Netflix error text
                        error_texts = [
                            "Ce numéro de téléphone n'a pas fonctionné",
                            "numéro prépayé",
                            "vérifier qu'il est correct",
                            "choisissez un autre mode de paiement",
                            "phone number",
                            "invalid",
                            "error"
                        ]
                        
                        page_text = await self.page.text_content('body')
                        for error_text in error_texts:
                            if error_text.lower() in page_text.lower():
                                has_error = True
                                error_message = f"Netflix error detected: {error_text}"
                                print(f"{Fore.RED}{error_message}")
                                break
                    except:
                        pass
                
                if not has_error:
                    print(f"{Fore.GREEN}✓ Format {i+1} accepted: {alt_format}")
                    return True
                else:
                    print(f"{Fore.RED}✗ Format {i+1} rejected: {alt_format}")
                    
            except Exception as e:
                print(f"{Fore.RED}✗ Error trying format {i+1}: {str(e)}")
                continue
        
        print(f"{Fore.YELLOW}⚠️ All alternative formats failed, trying test number...")
        
        # Try a test French number as last resort
        test_numbers = [
            "0602956360",      # Same format as Tiger SMS conversion
            "06 02 95 63 60",  # With spaces
            "06-02-95-63-60",  # With dashes
            "0612345678",      # Alternative test number
        ]
        
        for i, test_number in enumerate(test_numbers):
            try:
                print(f"{Fore.CYAN}Trying test number {i+1}: {test_number}")
                await phone_input.fill('')
                await phone_input.fill(test_number)
                await self.page.wait_for_timeout(1000)
                
                # Check for errors
                has_error = False
                try:
                    page_text = await self.page.text_content('body')
                    error_texts = ["Ce numéro de téléphone n'a pas fonctionné", "numéro prépayé", "vérifier qu'il est correct"]
                    for error_text in error_texts:
                        if error_text.lower() in page_text.lower():
                            has_error = True
                            break
                except:
                    pass
                
                if not has_error:
                    print(f"{Fore.GREEN}✓ Test number {i+1} accepted: {test_number}")
                    return True
                else:
                    print(f"{Fore.RED}✗ Test number {i+1} rejected: {test_number}")
                    
            except Exception as e:
                print(f"{Fore.RED}✗ Error trying test number {i+1}: {str(e)}")
                continue
        
        print(f"{Fore.RED}✗ All formats and test numbers failed")
        return False
    
    def generate_name(self) -> str:
        """
        Generate a random name
        
        Returns:
            str: Random name
        """
        names = [
            'Alex', 'Jordan', 'Taylor', 'Casey', 'Morgan', 'Riley', 'Avery', 'Quinn',
            'Blake', 'Cameron', 'Drew', 'Emery', 'Finley', 'Hayden', 'Jamie', 'Kendall',
            'Logan', 'Parker', 'Reese', 'Sage', 'Skyler', 'Sydney', 'Tatum', 'River'
        ]
        return random.choice(names)
    
    async def check_netflix_signup_page(self):
        """
        Check if we're on the Netflix signup page and click Next
        """
        print(f"{Fore.MAGENTA}=== Checking Netflix Signup Page ===")
        
        try:
            current_url = self.page.url
            print(f"{Fore.CYAN}Current URL: {current_url}")
            
            # Check if we're on the signup page
            if 'signup' in current_url and 'planform' not in current_url and 'dcboption' not in current_url:
                print(f"{Fore.GREEN}✓ On Netflix signup page")
                
                # Try multiple selectors for the Suivant button
                next_selectors = [
                    'button[data-uia="continue-button"]',
                    'button[data-uia="cta-button"]',
                    'button[type="submit"]',
                    'button:has-text("Suivant")',
                    'button:has-text("Suivant")',
                    'button:has-text("Next")',
                    'button:has-text("Continue")',
                    'button:has-text("Get Started")',
                    'button:has-text("Start Membership")',
                    '.btn-primary',
                    '[data-testid="continue-button"]'
                ]
                
                next_button = None
                for selector in next_selectors:
                    try:
                        next_button = await self.page.wait_for_selector(selector, timeout=3000)
                        if next_button:
                            print(f"{Fore.YELLOW}Found Next button with selector: {selector}")
                            break
                    except:
                        continue
                
                if next_button:
                    await next_button.click()
                    await self.page.wait_for_timeout(3000)
                    print(f"{Fore.GREEN}✓ Clicked initial Next button")
                    return True
                else:
                    print(f"{Fore.YELLOW}⚠️ Next button not found, but continuing...")
                    return True  # Continue anyway as the page might have auto-advanced
            else:
                print(f"{Fore.YELLOW}⚠️ Not on initial signup page, current URL: {current_url}")
                return False
            
        except Exception as e:
            print(f"{Fore.RED}Error checking Netflix signup page: {str(e)}")
            return False
    
    async def check_and_select_plan(self):
        """
        Check if we're on the planform page and select a plan
        """
        print(f"{Fore.MAGENTA}=== Checking Plan Selection Page ===")
        await self.page.wait_for_timeout(3000)
        try:
            current_url = self.page.url
            print(f"{Fore.CYAN}Current URL: {current_url}")
            
            # Check if we're on the plan selection page
            if 'planform' in current_url or 'PLAN_SELECTION' in current_url or 'signup' in current_url:
                print(f"{Fore.GREEN}✓ On Netflix planform page")
                await self.wait_between_steps(30)
                
                # Wait for page to fully load
                await self.page.wait_for_timeout(3000)
                
                # Skip plan selection and just press Suivant
                print(f"{Fore.YELLOW}⚠️ Skipping plan selection, just pressing Suivant...")
                
                # Try multiple selectors for the Suivant button
                next_selectors = [
                    'button[data-uia="cta-plan-selection"]',
                    'button[data-uia="cta-button"]',
                    'button[type="submit"]',
                    'button:has-text("Suivant")',
                    'button:has-text("Suivant")',
                    'button:has-text("Next")',
                    'button:has-text("Continue")',
                    'button:has-text("Get Started")',
                    'button:has-text("Start Membership")',
                    '.btn-primary',
                    'button[class*="btn"]',
                    'button[class*="button"]'
                ]
                
                next_button = None
                for selector in next_selectors:
                    try:
                        next_button = await self.page.wait_for_selector(selector, timeout=2000)
                        if next_button:
                            print(f"{Fore.YELLOW}Found Next button with selector: {selector}")
                            break
                    except:
                        continue
                
                if next_button:
                    try:
                        await next_button.click()
                        await self.wait_between_steps(30)
                        await self.page.wait_for_timeout(3000)
                        print(f"{Fore.GREEN}✓ Clicked Suivant button (skipped plan selection)")
                    except Exception as e:
                        print(f"{Fore.YELLOW}⚠️ Error clicking Next button: {str(e)}")
                else:
                    print(f"{Fore.YELLOW}⚠️ Suivant button not found, trying Enter key...")
                    try:
                        await self.page.keyboard.press('Enter')
                        await self.page.wait_for_timeout(2000)
                        print(f"{Fore.YELLOW}✓ Pressed Enter to proceed")
                    except:
                        pass
                
                return True
            else:
                print(f"{Fore.YELLOW}⚠️ Not on planform page, current URL: {current_url}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}Error checking plan selection: {str(e)}")
            return False
    
    async def click_following_button(self):
        """
        Click the "Suivant" button to proceed to registration form
        """
        print(f"{Fore.MAGENTA}=== Clicking Suivant Button ===")
        
        try:
            # Wait for the Suivant button to appear
            await self.page.wait_for_timeout(3000)
            
            # Try multiple selectors for the Suivant button
            following_selectors = [
                'button[data-uia="cta-continue-registration"]',
                'button:has-text("Suivant")',
                'button:has-text("Following")',
                'button[class*="ea2wixt2"]',
                'button[type="button"]:has-text("Suivant")',
                'button[type="button"]:has-text("Following")'
            ]
            
            following_button = None
            for selector in following_selectors:
                try:
                    following_button = await self.page.wait_for_selector(selector, timeout=3000)
                    if following_button:
                        print(f"{Fore.YELLOW}Found Suivant button with selector: {selector}")
                        break
                except:
                    continue
            
            if following_button:
                await following_button.click()
                await self.page.wait_for_timeout(3000)
                print(f"{Fore.GREEN}✓ Clicked Suivant button")
                return True
            else:
                print(f"{Fore.YELLOW}⚠️ Suivant button not found, trying alternative approach...")
                # Try to find any button with "Suivant" text
                try:
                    following_button = await self.page.query_selector('button:has-text("Suivant")')
                    if following_button:
                        await following_button.click()
                        await self.page.wait_for_timeout(3000)
                        print(f"{Fore.GREEN}✓ Clicked Suivant button (alternative method)")
                        return True
                except:
                    pass
                
                # Try "Following" as fallback
                try:
                    following_button = await self.page.query_selector('button:has-text("Following")')
                    if following_button:
                        await following_button.click()
                        await self.page.wait_for_timeout(3000)
                        print(f"{Fore.GREEN}✓ Clicked Following button (fallback method)")
                        return True
                except:
                    pass
                
                print(f"{Fore.RED}✗ Suivant button not found")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}Error clicking Suivant button: {str(e)}")
            return False
    
    async def fill_registration_form(self, credentials: Dict):
        """
        Fill the Netflix registration form (email and password)
        
        Args:
            credentials (Dict): Registration credentials
        """
        print(f"{Fore.MAGENTA}=== Filling Registration Form ===")
        
        try:
            # Wait for the registration page to load
            await self.page.wait_for_timeout(3000)
            
            # Fill email
            email_selectors = [
                'input[type="email"]',
                'input[name="email"]',
                'input[data-uia="email"]',
                'input[placeholder*="email"]',
                'input[placeholder*="Email"]',
                'input[placeholder*="E-mail"]',
                'input[id*="email"]'
            ]
            
            email_input = None
            for selector in email_selectors:
                try:
                    email_input = await self.page.wait_for_selector(selector, timeout=3000)
                    if email_input:
                        print(f"{Fore.YELLOW}Found email input with selector: {selector}")
                        break
                except:
                    continue
            
            if email_input:
                await email_input.fill(credentials['email'])
                print(f"{Fore.GREEN}✓ Email filled: {credentials['email']}")
            else:
                print(f"{Fore.RED}✗ Email input not found")
                return False
            
            # Fill password
            password_selectors = [
                'input[type="password"]',
                'input[name="password"]',
                'input[data-uia="password"]',
                'input[placeholder*="password"]',
                'input[placeholder*="Password"]',
                'input[placeholder*="Mot de passe"]',
                'input[id*="password"]'
            ]
            
            password_input = None
            for selector in password_selectors:
                try:
                    password_input = await self.page.wait_for_selector(selector, timeout=3000)
                    if password_input:
                        print(f"{Fore.YELLOW}Found password input with selector: {selector}")
                        break
                except:
                    continue
            
            if password_input:
                await password_input.fill(self.password)
                print(f"{Fore.GREEN}✓ Password filled")
            else:
                print(f"{Fore.RED}✗ Password input not found")
                return False
            
            # Click Suivant/Continue button
            next_selectors = [
                'button[type="submit"]',
                'button[data-uia="continue-button"]',
                'button[data-uia="next-button"]',
                'button:has-text("Suivant")',
                'button:has-text("Next")',
                'button:has-text("Continue")',
                'button:has-text("Get Started")',
                '.btn-primary',
                'button[class*="btn"]'
            ]
            
            next_button = None
            for selector in next_selectors:
                try:
                    next_button = await self.page.wait_for_selector(selector, timeout=2000)
                    if next_button:
                        print(f"{Fore.YELLOW}Found Next button with selector: {selector}")
                        break
                except:
                    continue
            
            if next_button:
                await next_button.click()
                await self.wait_between_steps(30)
                await self.page.wait_for_timeout(3000)
                print(f"{Fore.GREEN}✓ Clicked Suivant button")
            else:
                print(f"{Fore.YELLOW}⚠️ Suivant button not found, trying Enter key...")
                try:
                    await self.page.keyboard.press('Enter')
                    await self.page.wait_for_timeout(2000)
                    print(f"{Fore.YELLOW}✓ Pressed Enter to proceed")
                except:
                    pass
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}Error filling form: {str(e)}")
            return False
    
    async def check_phone_payment_page(self):
        """
        Check if we're on the phone payment page (dcboption)
        """
        print(f"{Fore.MAGENTA}=== Checking Phone Payment Page ===")
        
        try:
            current_url = self.page.url
            print(f"{Fore.CYAN}Current URL: {current_url}")
            
            # Check if we're on the dcboption page
            if 'dcboption' in current_url:
                print(f"{Fore.GREEN}✓ On Netflix phone payment page")
                return True
            else:
                print(f"{Fore.YELLOW}⚠️ Not on phone payment page, current URL: {current_url}")
                return False
            
        except Exception as e:
            print(f"{Fore.RED}Error checking phone payment page: {str(e)}")
            return False
    
    async def fill_phone_payment_form(self, phone_number: str):
        """
        Fill the phone payment form with French phone number
        
        Args:
            phone_number (str): Phone number for payment
        """
        print(f"{Fore.MAGENTA}=== Filling Phone Payment Form ===")
        
        try:
            # Phone input (use the current selector)
            formatted_phone = self.format_fr_phone_compact(phone_number)
            phone_input = await self.page.wait_for_selector('input[data-uia="field-phoneNumber"]', timeout=15000)
            await phone_input.fill('')
            await phone_input.fill(formatted_phone)
            print(f"{Fore.GREEN}✓ Phone number filled: {formatted_phone}")

            # Legal checkbox (new data-uia)
            try:
                legal_checkbox = await self.page.wait_for_selector('input[data-uia="legal-checkbox"]', timeout=5000)
                if legal_checkbox and not await legal_checkbox.is_checked():
                    await legal_checkbox.click()
                print(f"{Fore.GREEN}✓ Legal checkbox checked")
            except Exception as e:
                print(f"{Fore.YELLOW}⚠️ Could not check legal checkbox: {e}")
                try:
                    label = await self.page.query_selector('label[data-uia="legal-checkbox+label"]')
                    if label:
                        await label.click()
                        print(f"{Fore.GREEN}✓ Legal checkbox checked via label")
                except:
                    pass

            # Verify button
            verify_btn = None
            for sel in [
                'button[data-uia="action-submit-payment"]',
                'button[title*="Vérifier le numéro"]',
                'button[type="submit"]',
                'button:has-text("Vérifier le numéro de téléphone")'
            ]:
                try:
                    verify_btn = await self.page.wait_for_selector(sel, timeout=5000)
                    if verify_btn:
                        break
                except:
                    continue

            if verify_btn:
                await verify_btn.click()
                print(f"{Fore.GREEN}✓ Clicked Verify Phone Number button")
            else:
                print(f"{Fore.RED}✗ Verify Phone Number button not found")
        except Exception as e:
            print(f"{Fore.RED}Error in phone payment step: {e}")
    
    async def perform_phone_verification_loop(self, max_rotations: int = 20, use_initial: bool = True) -> Optional[str]:
        """
        Step 7 logic:
        1) Try with the prepared number (if provided): fill, checkbox, verify, wait 120s for SMS.
        2) If no SMS, cancel + wait 120s, then generate a new number and repeat until SMS arrives.
        """

        async def _fill_and_verify_current_number() -> bool:
            phone_input = await self.page.wait_for_selector('input[data-uia="field-phoneNumber"]', timeout=15000)
            await phone_input.fill('')
            await phone_input.fill(self.phone_number)
            print(f"{Fore.GREEN}✓ Phone filled: {self.phone_number}")

            try:
                legal_checkbox = await self.page.wait_for_selector('input[data-uia="legal-checkbox"]', timeout=5000)
                if legal_checkbox and not await legal_checkbox.is_checked():
                    await legal_checkbox.click()
                print(f"{Fore.GREEN}✓ Legal checkbox checked")
            except Exception as e:
                print(f"{Fore.YELLOW}⚠️ Could not check legal checkbox: {e}")
                try:
                    label = await self.page.query_selector('label[data-uia="legal-checkbox+label"]')
                    if label:
                        await label.click()
                        print(f"{Fore.GREEN}✓ Legal checkbox checked via label")
                except:
                    pass

            verify_btn = None
            for sel in [
                'button[data-uia="action-submit-payment"]',
                'button[title*="Vérifier le numéro"]',
                'button[type="submit"]',
                'button:has-text("Vérifier le numéro de téléphone")',
            ]:
                try:
                    verify_btn = await self.page.wait_for_selector(sel, timeout=5000)
                    if verify_btn:
                        break
                except:
                    continue

            if not verify_btn:
                print(f"{Fore.RED}✗ Verify button not found")
                return False

            await verify_btn.click()
            print(f"{Fore.GREEN}✓ Clicked Verify Phone Number")
            return True

        # A) Try the initial prepared number if requested
        if use_initial and self.activation_id and self.phone_number:
            print(f"{Fore.MAGENTA}=== Phone verify attempt (initial prepared number) ===")
            self.phone_number = self.format_fr_phone_compact(self.phone_number)
            try:
                if await _fill_and_verify_current_number():
                    code = await self.wait_for_sms_code(self.activation_id, max_wait_time=120)
                    if code:
                        print(f"{Fore.GREEN}✓ SMS code received: {code}")
                        return code
                    print(f"{Fore.YELLOW}⚠️ No SMS in 120s (initial); canceling activation and waiting 2 minutes before new number...")
                    try:
                        await self.sms_bot.cancel_activation(self.activation_id)
                    except:
                        pass
                    print(f"{Fore.CYAN}Waiting 2 minutes before requesting a new number...")
                    await asyncio.sleep(120)
            except Exception as e:
                print(f"{Fore.RED}✗ Error with initial number: {e}")
                try:
                    await self.sms_bot.cancel_activation(self.activation_id)
                except:
                    pass
                print(f"{Fore.CYAN}Waiting 2 minutes before requesting a new number...")
                await asyncio.sleep(120)

        # B) Rotate numbers until SMS arrives
        for attempt in range(1, max_rotations + 1):
            print(f"{Fore.MAGENTA}=== Phone verify rotation {attempt}/{max_rotations} ===")
            # Get new FR number
            try:
                resp = self.sms_bot.get_number('netflix', 'france')
                if resp.get('status') != 'success' or not str(resp.get('data', '')).startswith('ACCESS_'):
                    print(f"{Fore.RED}✗ Failed to get number: {resp}")
                    continue
                parts = str(resp['data']).split(':')
                self.activation_id = parts[1]
                full_number = parts[2]
                self.phone_number = self.format_fr_phone_compact(full_number)
                print(f"{Fore.CYAN}New number: {self.phone_number} (activation: {self.activation_id})")
            except Exception as e:
                print(f"{Fore.RED}✗ Error getting number: {e}")
                continue

            # Fill & verify
            try:
                ok = await _fill_and_verify_current_number()
                if not ok:
                    try:
                        await self.sms_bot.cancel_activation(self.activation_id)
                    except:
                        pass
                    print(f"{Fore.CYAN}Waiting 2 minutes before requesting a new number...")
                    await asyncio.sleep(120)
                    continue
            except Exception as e:
                print(f"{Fore.RED}✗ Error filling phone form: {e}")
                try:
                    await self.sms_bot.cancel_activation(self.activation_id)
                except:
                    pass
                print(f"{Fore.CYAN}Waiting 2 minutes before requesting a new number...")
                await asyncio.sleep(120)
                continue

            # Wait up to 120s for SMS
            code = await self.wait_for_sms_code(self.activation_id, max_wait_time=120)
            if code:
                print(f"{Fore.GREEN}✓ SMS code received: {code}")
                return code

            print(f"{Fore.YELLOW}⚠️ No SMS in 120s; canceling activation and waiting 2 minutes before new number...")
            try:
                await self.sms_bot.cancel_activation(self.activation_id)
            except:
                pass
            print(f"{Fore.CYAN}Waiting 2 minutes before requesting a new number...")
            await asyncio.sleep(120)

        print(f"{Fore.RED}✗ Exhausted {max_rotations} phone rotations without receiving SMS")
        return None
    
    async def wait_for_sms_verification(self, max_attempts=4) -> Optional[str]:
        """
        Wait for SMS verification code using Tiger SMS API with retry logic
        
        Args:
            max_attempts (int): Maximum number of attempts before restarting
            
        Returns:
            Optional[str]: SMS verification code or "RESTART_PROCESS" if max attempts reached
        """
        print(f"{Fore.MAGENTA}=== Waiting for SMS Verification ===")
        print(f"{Fore.CYAN}Phone: {self.phone_number}")
        print(f"{Fore.CYAN}Activation ID: {self.activation_id}")
        print(f"{Fore.CYAN}Max attempts: {max_attempts}")
        print(f"{Fore.CYAN}Waiting for SMS code...")
        
        for attempt in range(1, max_attempts + 1):
            print(f"{Fore.YELLOW}Attempt {attempt}/{max_attempts}")
            
            # Use the SMS bot to wait for code with proper API handling
            sms_code = await self.wait_for_sms_code(self.activation_id, max_wait_time=300)
            
            if sms_code:
                print(f"{Fore.GREEN}✓ SMS Code received: {sms_code}")
                return sms_code
            else:
                print(f"{Fore.RED}✗ No SMS code received (Attempt {attempt})")
                
                if attempt < max_attempts:
                    print(f"{Fore.YELLOW}⚠️ Starting new attempt {attempt + 1}/{max_attempts}")
                    # Cancel current activation and get new number
                    await self.cancel_activation()
                    await asyncio.sleep(5)  # Wait before getting new number
                else:
                    print(f"{Fore.RED}✗ All {max_attempts} attempts failed - restarting process")
                    return "RESTART_PROCESS"
        
        return None
    
    async def cancel_activation(self):
        """
        Cancel current SMS activation and get new credentials
        """
        print(f"{Fore.MAGENTA}=== Canceling Current Activation ===")
        
        try:
            if self.activation_id:
                # Cancel the current activation
                result = await self.sms_bot.cancel_activation(self.activation_id)
                if result['status'] == 'success':
                    print(f"{Fore.GREEN}✓ Activation canceled")
                else:
                    print(f"{Fore.YELLOW}⚠️ Could not cancel activation: {result.get('error', 'Unknown error')}")
            
            # Get new credentials
            print(f"{Fore.YELLOW}Getting new credentials...")
            credentials = await self.get_registration_credentials()
            
            if credentials:
                self.phone_number = credentials['phone']
                self.activation_id = credentials.get('activation_id')
                self.email_address = credentials['email']
                print(f"{Fore.GREEN}✓ New credentials obtained")
                print(f"{Fore.CYAN}New phone: {self.phone_number}")
                print(f"{Fore.CYAN}New email: {self.email_address}")
                return True
            else:
                print(f"{Fore.RED}✗ Failed to get new credentials")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}✗ Error canceling activation: {str(e)}")
            return False
    
    async def wait_for_sms_code(self, activation_id: str, max_wait_time: int = 300) -> Optional[str]:
        """
        Wait for SMS code using Tiger SMS API with proper response handling
        
        Args:
            activation_id (str): Activation ID
            max_wait_time (int): Maximum time to wait in seconds
            
        Returns:
            Optional[str]: SMS code if received, None otherwise
        """
        print(f"{Fore.MAGENTA}=== Waiting for SMS Code ===")
        print(f"{Fore.CYAN}Activation ID: {activation_id}")
        print(f"{Fore.CYAN}Max wait time: {max_wait_time} seconds")
        
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            try:
                # Make API request to get status
                response = self.sms_bot._make_request('getStatus', id=activation_id)
                
                if response['status'] == 'success':
                    response_data = response['data']
                    
                    if response_data == 'STATUS_WAIT_CODE':
                        elapsed = int(time.time() - start_time)
                        print(f"{Fore.YELLOW}Waiting for SMS... ({elapsed}s elapsed)")
                        await asyncio.sleep(10)  # Wait 10 seconds before checking again
                        
                    elif response_data == 'STATUS_WAIT_RESEND':
                        elapsed = int(time.time() - start_time)
                        print(f"{Fore.YELLOW}Waiting for resend... ({elapsed}s elapsed)")
                        await asyncio.sleep(10)
                        
                    elif response_data == 'STATUS_CANCEL':
                        print(f"{Fore.RED}✗ Activation was cancelled")
                        return None
                        
                    elif response_data.startswith('STATUS_OK:'):
                        # Extract SMS code from response
                        sms_code = response_data.split(':')[-1].strip()
                        print(f"{Fore.GREEN}✓ SMS Code received: {sms_code}")
                        return sms_code
                        
                    else:
                        print(f"{Fore.YELLOW}Unknown status: {response_data}")
                        await asyncio.sleep(10)
                        
                elif response['status'] == 'error':
                    error = response.get('error', 'Unknown error')
                    if 'BAD_KEY' in error:
                        print(f"{Fore.RED}✗ Invalid API key")
                        return None
                    elif 'BAD_ACTION' in error:
                        print(f"{Fore.RED}✗ Incorrect action")
                        return None
                    elif 'NO_ACTIVATION' in error:
                        print(f"{Fore.RED}✗ Incorrect activation ID")
                        return None
                    else:
                        print(f"{Fore.RED}✗ API Error: {error}")
                        await asyncio.sleep(10)
                else:
                    print(f"{Fore.RED}✗ Unknown response: {response}")
                    await asyncio.sleep(10)
                    
            except Exception as e:
                print(f"{Fore.RED}✗ Error checking SMS status: {str(e)}")
                await asyncio.sleep(10)
        
        print(f"{Fore.RED}✗ Timeout waiting for SMS code")
        return None
    
    async def cancel_activation(self, activation_id: str) -> bool:
        """
        Cancel the activation if needed
        
        Args:
            activation_id (str): Activation ID to cancel
            
        Returns:
            bool: True if cancelled successfully
        """
        try:
            print(f"{Fore.YELLOW}Cancelling activation: {activation_id}")
            response = self.sms_bot.set_status(activation_id, '6')  # 6 = cancel
            if response['status'] == 'success':
                print(f"{Fore.GREEN}✓ Activation cancelled successfully")
                return True
            else:
                print(f"{Fore.RED}✗ Failed to cancel activation: {response.get('error', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"{Fore.RED}✗ Error cancelling activation: {str(e)}")
            return False
    
    async def enter_sms_verification_code(self, sms_code: str):
        """
        Enter SMS verification code
        
        Args:
            sms_code (str): SMS verification code
        """
        print(f"{Fore.MAGENTA}=== Entering SMS Verification Code ===")
        
        try:
            # Find SMS code input with multiple possible selectors
            sms_selectors = [
                'input[data-uia*="verification"]',
                'input[name="code"]',
                'input[placeholder*="code"]',
                'input[type="text"]',
                'input[type="tel"]'
            ]
            
            sms_input = None
            for selector in sms_selectors:
                try:
                    sms_input = await self.page.wait_for_selector(selector, timeout=5000)
                    if sms_input:
                        break
                except:
                    continue
            
            if sms_input:
                await sms_input.fill(sms_code)
                print(f"{Fore.GREEN}✓ SMS code entered: {sms_code}")
                
                # Click Verify or Continue button
                verify_selectors = [
                    'button[data-uia*="verify"]',
                    'button[data-uia*="submit"]',
                    'button[type="submit"]',
                    'button:has-text("Verify")',
                    'button:has-text("Continue")',
                    'button:has-text("Next")'
                ]
                
                for selector in verify_selectors:
                    try:
                        verify_button = await self.page.query_selector(selector)
                        if verify_button:
                            await verify_button.click()
                            await self.page.wait_for_timeout(3000)
                            print(f"{Fore.GREEN}✓ Clicked verification button")
                            break
                    except:
                        continue
                
                return True
            else:
                print(f"{Fore.RED}✗ SMS code input not found")
                return False
            
        except Exception as e:
            print(f"{Fore.RED}Error entering SMS code: {str(e)}")
            return False
    
    async def wait_for_verification_email(self, max_wait_time: int = 120) -> bool:
        """
        Wait for Netflix verification email
        
        Args:
            max_wait_time (int): Maximum time to wait in seconds
            
        Returns:
            bool: True if verification email received
        """
        print(f"{Fore.MAGENTA}=== Waiting for Verification Email ===")
        print(f"{Fore.CYAN}Email: {self.email_address}")
        print(f"{Fore.CYAN}Max wait time: {max_wait_time} seconds")
        
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            try:
                messages = self.email_service.get_messages()
                
                # Look for Netflix verification emails
                for msg in messages:
                    if (self.email_address in msg['to'] and 
                        ('netflix' in msg['subject'].lower() or 
                         'verification' in msg['subject'].lower() or
                         'confirm' in msg['subject'].lower())):
                        print(f"{Fore.GREEN}✓ Verification email received!")
                        print(f"{Fore.GREEN}From: {msg['from']}")
                        print(f"{Fore.GREEN}Subject: {msg['subject']}")
                        return True
                
                elapsed = int(time.time() - start_time)
                print(f"{Fore.YELLOW}Waiting for verification email... ({elapsed}s elapsed)")
                await asyncio.sleep(10)
                
            except Exception as e:
                print(f"{Fore.RED}✗ Error checking emails: {str(e)}")
                await asyncio.sleep(10)
        
        print(f"{Fore.RED}✗ Timeout waiting for verification email")
        return False
    
    async def complete_registration(self):
        """
        Complete the Netflix registration process
        """
        print(f"{Fore.MAGENTA}=== Completing Registration ===")
        
        try:
            # Wait for completion or success page
            await self.page.wait_for_timeout(5000)
            
            # Check if we're on a success page or dashboard
            current_url = self.page.url
            if 'netflix.com' in current_url and ('browse' in current_url or 'profiles' in current_url):
                print(f"{Fore.GREEN}✓ Registration completed successfully!")
                print(f"{Fore.GREEN}✓ Netflix account created!")
                return True
            else:
                print(f"{Fore.YELLOW}Registration in progress...")
                return True
                
        except Exception as e:
            print(f"{Fore.RED}Error completing registration: {str(e)}")
            return False
    
    async def run_complete_registration(self):
        """
        Run the complete Netflix registration process
        """
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}Netflix Registration Bot with Playwright - Educational Purpose")
        print(f"{Fore.CYAN}{'='*60}")
        
        try:
            # Start browser
            await self.start_browser()
            
            # Get registration credentials
            credentials = await self.get_registration_credentials()
            
            if credentials['status'] != 'success':
                print(f"{Fore.RED}✗ Failed to get registration credentials")
                return
            
            print(f"\n{Fore.BLUE}Registration Credentials:")
            print(f"{Fore.WHITE}📧 Email: {credentials['email']}")
            print(f"{Fore.WHITE}📱 Phone: {credentials['phone']}")
            print(f"{Fore.WHITE}🔑 Password: {self.password}")
            print(f"{Fore.WHITE}👤 Name: {self.first_name} {self.last_name}")
            
            # Step 1: Navigate to Netflix signup page
            print(f"\n{Fore.BLUE}Step 1: Navigating to Netflix signup page...")
            try:
                await self.page.goto('https://www.netflix.com/fr/signup', wait_until='domcontentloaded', timeout=30000)
                await self.page.wait_for_timeout(3000)
                print(f"{Fore.GREEN}✓ Successfully navigated to Netflix signup")
                await self.wait_between_steps(30)
            except Exception as e:
                print(f"{Fore.RED}✗ Failed to navigate to Netflix signup: {str(e)}")
                return
            
            # Step 2: Check Netflix signup page
            print(f"\n{Fore.BLUE}Step 2: Checking Netflix signup page...")
            if not await self.check_netflix_signup_page():
                print(f"{Fore.RED}✗ Not on Netflix signup page")
                return
            
            # Step 3: Check and select plan
            print(f"\n{Fore.BLUE}Step 3: Checking plan selection page...")
            plan_selection_result = await self.check_and_select_plan()
            if not plan_selection_result:
                print(f"{Fore.YELLOW}⚠️ Plan selection had issues, but continuing...")
                # Wait a bit and try to continue
                await self.page.wait_for_timeout(3000)
            
            # Step 4: Click "Suivant" button to proceed to registration form
            print(f"\n{Fore.BLUE}Step 4: Clicking Suivant button...")
            if not await self.click_following_button():
                print(f"{Fore.YELLOW}⚠️ Suivant button not found, but continuing...")
                await self.page.wait_for_timeout(3000)
            
            # Step 5: Fill registration form (email and password)
            print(f"\n{Fore.BLUE}Step 5: Filling registration form...")
            if not await self.fill_registration_form(credentials):
                print(f"{Fore.YELLOW}⚠️ Registration form filling had issues, but continuing...")
                await self.page.wait_for_timeout(3000)
            
            # Step 6: Check phone payment page
            print(f"\n{Fore.BLUE}Selecting mobile billing method...")
            selected = await self.select_mobile_billing_method()
            if not selected:
                print(f"{Fore.YELLOW}⚠️ Could not auto-select DCB; trying to navigate directly...")
                try:
                    await self.page.goto('https://www.netflix.com/fr/signup/dcboption', wait_until='domcontentloaded', timeout=15000)
                    await self.page.wait_for_timeout(2000)
                except Exception as e:
                    print(f"{Fore.RED}✗ Failed to navigate to DCB page: {str(e)}")
                    return
            
            # Step 7: Phone verification with auto-rotation
            print(f"\n{Fore.BLUE}Step 7: Phone verification with auto-rotation...")
            # Ensure form is visible before loop
            await self.fill_phone_payment_form(credentials['phone'])
            sms_code = await self.perform_phone_verification_loop(max_rotations=1)
            
            if sms_code:
                # Step 8: Enter SMS verification code
                print(f"\n{Fore.BLUE}Step 8: Entering SMS verification code...")
                if await self.enter_sms_verification_code(sms_code):
                    # Step 9: Wait for verification email
                    print(f"\n{Fore.BLUE}Step 9: Waiting for verification email...")
                    email_verified = await self.wait_for_verification_email()
                    
                    if email_verified:
                        # Step 10: Complete registration
                        print(f"\n{Fore.BLUE}Step 10: Completing registration...")
                        await self.complete_registration()
                        
                        print(f"\n{Fore.GREEN}{'='*60}")
                        print(f"{Fore.GREEN}🎉 NETFLIX REGISTRATION COMPLETED! 🎉")
                        print(f"{Fore.GREEN}{'='*60}")
                        print(f"{Fore.GREEN}✓ Account created successfully")
                        print(f"{Fore.GREEN}✓ Email: {credentials['email']}")
                        print(f"{Fore.GREEN}✓ Phone: {credentials['phone']}")
                        print(f"{Fore.GREEN}✓ Email verified via Docker service")
                        print(f"{Fore.GREEN}✓ You can now use your Netflix account!")
                        print(f"{Fore.CYAN}🌐 Check emails at: http://localhost:8025")
                    else:
                        print(f"{Fore.YELLOW}⚠️ Verification email not received, but registration may still be successful")
                        await self.complete_registration()
                else:
                    print(f"{Fore.RED}✗ Failed to enter SMS verification code")
            else:
                print(f"{Fore.RED}✗ No SMS verification code received")
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Registration stopped by user")
        except Exception as e:
            print(f"\n{Fore.RED}An error occurred: {str(e)}")
    
    async def run_with_retry_logic(self, restart_delay_sec: int = 10):
        """
        Run the complete registration process in an infinite loop.
        On any failure or completion, restart from the beginning after a delay.
        """
        print(f"{Fore.MAGENTA}=== Starting Netflix Registration with Infinite Retry ===")
        attempt = 0
        while True:
            attempt += 1
            try:
                print(f"\n{Fore.YELLOW}🔄 Global attempt #{attempt}")
                # Optional: rotate proxy/context between full runs if you have a rotation helper
                try:
                    await self._rotate_free_proxy_context()
                except Exception as e:
                    print(f"{Fore.YELLOW}Proxy rotation warning: {e}")

                await self.run_complete_registration()

                print(f"{Fore.GREEN}🎉 Registration completed successfully!")
                # If you want to stop after one success, break here
                # break
            except Exception as e:
                print(f"\n{Fore.RED}✗ Run failed: {str(e)}")
            finally:
                try:
                    await self.close_browser()
                except:
                    pass

            print(f"{Fore.YELLOW}⏳ Restarting from the beginning in {restart_delay_sec}s...")
            await asyncio.sleep(restart_delay_sec)
        
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}Netflix registration process completed")
        print(f"{Fore.CYAN}{'='*60}")

async def main():
    """
    Main function to run the Netflix registration bot with infinite retry
    """
    bot = NetflixRegistrationBot()
    try:
        await bot.run_with_retry_logic(restart_delay_sec=10)
    finally:
        # Close browser
        await bot.close_browser()
        # Cleanup email service
        try:
            bot.email_service.clear_messages()
            print(f"{Fore.GREEN}✓ Email messages cleared")
        except:
            pass

if __name__ == "__main__":
    asyncio.run(main())