#!/usr/bin/env python3
"""
Tiger SMS Bot - Educational Purpose
Automated bot to get phone numbers for Netflix verification
"""

import requests
import time
import json
from typing import Dict, Optional, Tuple
from colorama import init, Fore, Style
from config import API_KEY, BASE_URL, SERVICES, COUNTRIES, ENDPOINTS, TIMEOUT, MAX_RETRIES

# Initialize colorama for colored output
init(autoreset=True)

class TigerSMSBot:
    def __init__(self, api_key: str = API_KEY):
        """
        Initialize the Tiger SMS Bot
        
        Args:
            api_key (str): Your Tiger SMS API key
        """
        self.api_key = api_key
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.timeout = TIMEOUT
        
    def _make_request(self, action: str, **params) -> Dict:
        """
        Make a request to the Tiger SMS API
        
        Args:
            action (str): API action to perform
            **params: Additional parameters for the request
            
        Returns:
            Dict: API response as dictionary
        """
        # Prepare request parameters
        request_params = {
            'api_key': self.api_key,
            'action': action,
            **params
        }
        
        try:
            print(f"{Fore.YELLOW}Making request to Tiger SMS API...")
            print(f"{Fore.CYAN}Action: {action}")
            print(f"{Fore.CYAN}Parameters: {request_params}")
            
            response = self.session.get(self.base_url, params=request_params)
            response.raise_for_status()
            
            # Parse response
            response_text = response.text.strip()
            print(f"{Fore.GREEN}API Response: {response_text}")
            
            # Handle different response formats
            if response_text.startswith('ACCESS_'):
                return {
                    'status': 'success',
                    'data': response_text,
                    'raw_response': response_text
                }
            elif response_text.startswith('NO_NUMBERS'):
                return {
                    'status': 'no_numbers',
                    'message': 'No numbers available for the selected service/country',
                    'raw_response': response_text
                }
            elif response_text.startswith('BAD_'):
                return {
                    'status': 'error',
                    'error': response_text,
                    'raw_response': response_text
                }
            else:
                return {
                    'status': 'unknown',
                    'raw_response': response_text
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'status': 'error',
                'error': f"Request failed: {str(e)}",
                'raw_response': None
            }
    
    def get_balance(self) -> Dict:
        """
        Get account balance
        
        Returns:
            Dict: Balance information
        """
        print(f"{Fore.MAGENTA}=== Getting Account Balance ===")
        return self._make_request(ENDPOINTS['get_balance'])
    
    def get_number(self, service: str, country: str, ref: str = None, max_price: float = None) -> Dict:
        """
        Get a phone number for verification
        
        Args:
            service (str): Service name (e.g., 'netflix')
            country (str): Country name (e.g., 'france')
            ref (str, optional): Referral ID
            max_price (float, optional): Maximum price willing to pay
            
        Returns:
            Dict: Phone number information
        """
        print(f"{Fore.MAGENTA}=== Getting Phone Number ===")
        print(f"{Fore.CYAN}Service: {service}")
        print(f"{Fore.CYAN}Country: {country}")
        
        # Convert service and country names to codes
        service_code = SERVICES.get(service.lower())
        country_code = COUNTRIES.get(country.lower())
        
        if not service_code:
            return {
                'status': 'error',
                'error': f"Unknown service: {service}. Available services: {list(SERVICES.keys())}"
            }
            
        if not country_code:
            return {
                'status': 'error', 
                'error': f"Unknown country: {country}. Available countries: {list(COUNTRIES.keys())}"
            }
        
        # Prepare parameters
        params = {
            'service': service_code,
            'country': country_code
        }
        
        if ref:
            params['ref'] = ref
        if max_price:
            params['maxPrice'] = max_price
            
        return self._make_request(ENDPOINTS['get_number'], **params)
    
    def get_status(self, activation_id: str) -> Dict:
        """
        Get activation status
        
        Args:
            activation_id (str): Activation ID from get_number response
            
        Returns:
            Dict: Status information
        """
        print(f"{Fore.MAGENTA}=== Getting Activation Status ===")
        print(f"{Fore.CYAN}Activation ID: {activation_id}")
        
        return self._make_request(ENDPOINTS['get_status'], id=activation_id)
    
    def set_status(self, activation_id: str, status: str) -> Dict:
        """
        Set activation status
        
        Args:
            activation_id (str): Activation ID
            status (str): Status to set ('1' for ready, '6' for cancel)
            
        Returns:
            Dict: Response information
        """
        print(f"{Fore.MAGENTA}=== Setting Activation Status ===")
        print(f"{Fore.CYAN}Activation ID: {activation_id}")
        print(f"{Fore.CYAN}Status: {status}")
        
        return self._make_request(ENDPOINTS['set_status'], id=activation_id, status=status)
    
    def wait_for_sms(self, activation_id: str, max_wait_time: int = 300) -> Optional[str]:
        """
        Wait for SMS code to arrive
        
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
            status_response = self.get_status(activation_id)
            
            if status_response['status'] == 'success':
                response_data = status_response['data']
                
                if response_data.startswith('STATUS_OK'):
                    # Extract SMS code
                    sms_code = response_data.split(':')[-1] if ':' in response_data else None
                    print(f"{Fore.GREEN}SMS Code received: {sms_code}")
                    return sms_code
                elif response_data == 'STATUS_WAIT_CODE':
                    print(f"{Fore.YELLOW}Waiting for SMS... ({int(time.time() - start_time)}s elapsed)")
                    time.sleep(10)  # Wait 10 seconds before checking again
                elif response_data == 'STATUS_CANCEL':
                    print(f"{Fore.RED}Activation was cancelled")
                    return None
                else:
                    print(f"{Fore.YELLOW}Status: {response_data}")
                    time.sleep(10)
            elif status_response['status'] == 'unknown':
                # Handle direct status responses like STATUS_WAIT_CODE
                response_data = status_response['raw_response']
                if response_data == 'STATUS_WAIT_CODE':
                    print(f"{Fore.YELLOW}Waiting for SMS... ({int(time.time() - start_time)}s elapsed)")
                    time.sleep(10)  # Wait 10 seconds before checking again
                elif response_data.startswith('STATUS_OK'):
                    # Extract SMS code
                    sms_code = response_data.split(':')[-1] if ':' in response_data else None
                    print(f"{Fore.GREEN}SMS Code received: {sms_code}")
                    return sms_code
                elif response_data == 'STATUS_CANCEL':
                    print(f"{Fore.RED}Activation was cancelled")
                    return None
                else:
                    print(f"{Fore.YELLOW}Status: {response_data}")
                    time.sleep(10)
            else:
                print(f"{Fore.RED}Error checking status: {status_response.get('error', 'Unknown error')}")
                time.sleep(10)
        
        print(f"{Fore.RED}Timeout waiting for SMS code")
        return None

def main():
    """
    Main function to demonstrate the bot usage
    """
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}Tiger SMS Bot - Educational Purpose")
    print(f"{Fore.CYAN}{'='*60}")
    
    # Initialize bot
    bot = TigerSMSBot()
    
    try:
        # Check balance first
        print(f"\n{Fore.BLUE}1. Checking account balance...")
        balance_response = bot.get_balance()
        print(f"{Fore.WHITE}Balance Response: {json.dumps(balance_response, indent=2)}")
        
        # Get phone number for Netflix (France)
        print(f"\n{Fore.BLUE}2. Getting phone number for Netflix (France)...")
        number_response = bot.get_number('netflix', 'france')
        print(f"{Fore.WHITE}Number Response: {json.dumps(number_response, indent=2)}")
        
        if number_response['status'] == 'success':
            # Extract activation ID and phone number
            response_data = number_response['data']
            if response_data.startswith('ACCESS_'):
                parts = response_data.split(':')
                if len(parts) >= 2:
                    activation_id = parts[1]
                    phone_number = parts[2] if len(parts) > 2 else "Unknown"
                    
                    print(f"{Fore.GREEN}✓ Phone number obtained!")
                    print(f"{Fore.GREEN}Activation ID: {activation_id}")
                    print(f"{Fore.GREEN}Phone Number: {phone_number}")
                    
                    # Wait for SMS code
                    print(f"\n{Fore.BLUE}3. Waiting for SMS code...")
                    print(f"{Fore.YELLOW}Please use this phone number to register on Netflix:")
                    print(f"{Fore.CYAN}Phone: {phone_number}")
                    print(f"{Fore.YELLOW}Waiting for verification code...")
                    
                    sms_code = bot.wait_for_sms(activation_id, max_wait_time=300)
                    
                    if sms_code:
                        print(f"{Fore.GREEN}✓ SMS Code received: {sms_code}")
                        print(f"{Fore.GREEN}You can now complete the Netflix registration!")
                    else:
                        print(f"{Fore.RED}✗ No SMS code received within timeout period")
                        print(f"{Fore.YELLOW}You can cancel the activation if needed")
                        
                        # Ask if user wants to cancel
                        cancel = input(f"{Fore.YELLOW}Do you want to cancel the activation? (y/n): ").lower()
                        if cancel == 'y':
                            cancel_response = bot.set_status(activation_id, '6')
                            print(f"{Fore.WHITE}Cancel Response: {json.dumps(cancel_response, indent=2)}")
                else:
                    print(f"{Fore.RED}✗ Unexpected response format: {response_data}")
            else:
                print(f"{Fore.RED}✗ Failed to get phone number: {response_data}")
        else:
            print(f"{Fore.RED}✗ Error getting phone number: {number_response.get('error', 'Unknown error')}")
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Bot stopped by user")
    except Exception as e:
        print(f"\n{Fore.RED}An error occurred: {str(e)}")
    
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}Bot execution completed")
    print(f"{Fore.CYAN}{'='*60}")

if __name__ == "__main__":
    main()
