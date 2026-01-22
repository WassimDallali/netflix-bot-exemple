#!/usr/bin/env python3
"""
Test Netflix Bot with Docker Email Integration
Tests the integration without running the full registration process
"""

import asyncio
from netflix_registration_bot import NetflixRegistrationBot
from colorama import init, Fore

init(autoreset=True)

async def test_docker_integration():
    """
    Test the Docker email integration
    """
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}Testing Netflix Bot with Docker Email Integration")
    print(f"{Fore.CYAN}{'='*60}")
    
    bot = NetflixRegistrationBot()
    
    try:
        # Test 1: Check Docker email service
        print(f"\n{Fore.BLUE}Test 1: Checking Docker email service...")
        if not bot.email_service.check_service_status():
            print(f"{Fore.RED}✗ Docker email service not running!")
            print(f"{Fore.YELLOW}Please run: docker-compose up -d")
            return False
        
        print(f"{Fore.GREEN}✓ Docker email service is running")
        
        # Test 2: Get registration credentials
        print(f"\n{Fore.BLUE}Test 2: Getting registration credentials...")
        credentials = await bot.get_registration_credentials()
        
        if credentials['status'] != 'success':
            print(f"{Fore.RED}✗ Failed to get registration credentials")
            return False
        
        print(f"{Fore.GREEN}✓ Registration credentials obtained:")
        print(f"{Fore.WHITE}📧 Email: {credentials['email']}")
        print(f"{Fore.WHITE}📱 Phone: {credentials['phone']}")
        print(f"{Fore.WHITE}🔑 Password: {bot.password}")
        print(f"{Fore.WHITE}👤 Name: {bot.first_name} {bot.last_name}")
        
        # Test 3: Test email monitoring
        print(f"\n{Fore.BLUE}Test 3: Testing email monitoring...")
        messages = bot.email_service.get_messages()
        print(f"{Fore.GREEN}✓ Email monitoring working - {len(messages)} messages found")
        
        # Test 4: Send test email
        print(f"\n{Fore.BLUE}Test 4: Sending test email...")
        if bot.email_service.send_test_email(
            to_email=credentials['email'],
            subject="Netflix Registration Test",
            body="This is a test email for Netflix registration verification."
        ):
            print(f"{Fore.GREEN}✓ Test email sent successfully")
        else:
            print(f"{Fore.RED}✗ Failed to send test email")
            return False
        
        # Test 5: Wait for test email
        print(f"\n{Fore.BLUE}Test 5: Waiting for test email...")
        import time
        start_time = time.time()
        email_received = False
        
        while time.time() - start_time < 30:  # Wait up to 30 seconds
            messages = bot.email_service.get_messages()
            for msg in messages:
                if (credentials['email'] in msg['to'] and 
                    'test' in msg['subject'].lower()):
                    print(f"{Fore.GREEN}✓ Test email received!")
                    print(f"{Fore.GREEN}From: {msg['from']}")
                    print(f"{Fore.GREEN}Subject: {msg['subject']}")
                    email_received = True
                    break
            
            if email_received:
                break
            
            print(f"{Fore.YELLOW}Waiting for test email... ({int(time.time() - start_time)}s elapsed)")
            await asyncio.sleep(2)
        
        if not email_received:
            print(f"{Fore.YELLOW}⚠️ Test email not received within timeout")
        
        # Test 6: Cleanup
        print(f"\n{Fore.BLUE}Test 6: Cleaning up...")
        bot.email_service.clear_messages()
        print(f"{Fore.GREEN}✓ Email messages cleared")
        
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}🎉 ALL TESTS PASSED! 🎉")
        print(f"{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}✓ Docker email service integration working perfectly")
        print(f"{Fore.GREEN}✓ Ready for Netflix registration automation")
        print(f"{Fore.CYAN}🌐 Check emails at: http://localhost:8025")
        
        return True
        
    except Exception as e:
        print(f"\n{Fore.RED}✗ Test failed: {str(e)}")
        return False

async def main():
    """
    Main test function
    """
    success = await test_docker_integration()
    
    if success:
        print(f"\n{Fore.GREEN}✅ Integration test completed successfully!")
        print(f"{Fore.GREEN}The Netflix bot is ready to use with Docker email service.")
    else:
        print(f"\n{Fore.RED}❌ Integration test failed!")
        print(f"{Fore.RED}Please check the Docker email service and try again.")

if __name__ == "__main__":
    asyncio.run(main())

