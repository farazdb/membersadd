from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl import functions
import time
import os

api_id = 23877053 
api_hash = '989c360358b981dae46a910693ab2f4c' 

def print_colored(text, color):
    colors = {
        'green': '\033[92m',
        'red': '\033[91m',
        'cyan': '\033[96m',
        'reset': '\033[0m'
    }
    print(f"{colors[color]}{text}{colors['reset']}")

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = r"""
███╗   ██╗ ██████╗ ██╗   ██╗████████╗ ██████╗ ████████╗ ██████╗ ██████╗  ██████╗  ██████╗ 
████╗  ██║██╔═══██╗██║   ██║╚══██╔══╝██╔═══██╗╚══██╔══╝██╔═══██╗██╔══██╗██╔════╝ ██╔═══██╗
██╔██╗ ██║██║   ██║██║   ██║   ██║   ██║   ██║   ██║   ██║   ██║██████╔╝██║  ███╗██║   ██║
██║╚██╗██║██║   ██║██║   ██║   ██║   ██║   ██║   ██║   ██║   ██║██╔═══╝ ██║   ██║██║   ██║
██║ ╚████║╚██████╔╝╚██████╔╝   ██║   ╚██████╔╝   ██║   ╚██████╔╝██║     ╚██████╔╝╚██████╔╝
╚═╝  ╚═══╝ ╚═════╝  ╚═════╝    ╚═╝    ╚═════╝    ╚═╝    ╚═════╝ ╚═╝      ╚═════╝  ╚═════╝ 
"""
    print_colored(banner, 'cyan')
    print_colored("                           TOOL MADE BY OLD-HACKER", 'green')
    print()

# ✅ Fixed TimeoutError by adding timeout and connection_retries
client = TelegramClient('session_name', api_id, api_hash, timeout=15, connection_retries=5)

async def main():
    print_banner()

    group_to_scrape = input("Enter the username of the group to scrape members from (without @): ")
    group_to_add = input("Enter the username of the group to add members to (without @): ")

    if not await client.is_user_authorized():
        phone_number = input("Enter your phone number: ")
        await client.send_code_request(phone_number)
        otp = input("Enter the OTP: ")
        try:
            await client.sign_in(phone_number, otp)
        except SessionPasswordNeededError:
            password = input("Enter your 2FA password: ")
            await client.sign_in(password=password)
        print_colored("Login successful.", "green")
    else:
        print_colored("Already logged in.", "green")

    group_to_scrape = await client.get_entity(group_to_scrape)
    group_to_add = await client.get_entity(group_to_add)

    members = await client.get_participants(group_to_scrape)

    for member in members:
        if member.bot:
            print_colored(f"Skipping bot: {member.username}", "red")
            continue
        if member.username is None:
            print_colored(f"Skipping deleted account: {member.id}", "red")
            continue  

        try:
            await client(functions.channels.InviteToChannelRequest(
                group_to_add, [member]
            ))
            print_colored(f"{member.username} added successfully.", "green")
            time.sleep(1)
        except Exception as e:
            print_colored(f"Failed to add {member.username}: {e}", "red")
            time.sleep(1)  

with client:
    client.loop.run_until_complete(main())
