from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl import functions
import asyncio
import os

# 🔑 API Credentials
api_id = 23877053
api_hash = '989c360358b981dae46a910693ab2f4c'

# 🎨 Text Styling
def print_colored(text, color):
    colors = {
        'green': '\033[92m',
        'red': '\033[91m',
        'cyan': '\033[96m',
        'reset': '\033[0m'
    }
    print(f"{colors.get(color, '')}{text}{colors['reset']}")

# 🖼️ Banner Display
def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = r"""
██╗░░░░░░█████╗░██████╗░░█████╗░░██████╗
██║░░░░░██╔══██╗╚════██╗██╔══██╗██╔════╝
██║░░░░░██║░░██║░░███╔═╝██║░░██║╚█████╗░
██║░░░░░██║░░██║██╔══╝░░██║░░██║░╚═══██╗
███████╗╚█████╔╝███████╗╚█████╔╝██████╔╝
╚══════╝░╚════╝░╚══════╝░╚════╝░╚═════╝░
"""
    print_colored(banner, 'cyan')
    print_colored("                           TOOL MADE BY FARAZ", 'green')
    print()

# 📡 Telegram Client Setup
client = TelegramClient('session_name', api_id, api_hash, timeout=15, connection_retries=5)

# 🚀 Main Logic
async def main():
    print_banner()

    group_to_scrape = input("🔍 Group to scrape members from (without @): ")
    group_to_add = input("➕ Group to add members to (without @): ")

    try:
        # 🔐 Authorization
        if not await client.is_user_authorized():
            phone_number = input("📱 Enter your phone number: ")
            await client.send_code_request(phone_number)
            otp = input("🔢 Enter OTP: ")
            try:
                await client.sign_in(phone_number, otp)
            except SessionPasswordNeededError:
                password = input("🔐 Enter 2FA password: ")
                await client.sign_in(password=password)
            print_colored("✅ Login successful", "green")
        else:
            print_colored("⚡ Already logged in", "green")

        # 🔍 Fetch group entities
        group_to_scrape = await client.get_entity(group_to_scrape)
        group_to_add = await client.get_entity(group_to_add)

        # 👥 Fetch members
        members = await client.get_participants(group_to_scrape)
        print_colored(f"📥 Found {len(members)} members", "cyan")

        # ➕ Add members
        for member in members:
            if member.bot:
                print_colored(f"🤖 Skipping bot: {member.username}", "red")
                continue
            if member.username is None:
                print_colored(f"🗑️ Skipping deleted user: {member.id}", "red")
                continue

            try:
                await client(functions.channels.InviteToChannelRequest(
                    group_to_add, [member]
                ))
                print_colored(f"✅ {member.username} added", "green")
                await asyncio.sleep(1)
            except Exception as e:
                print_colored(f"❌ Failed to add {member.username}: {e}", "red")
                await asyncio.sleep(1)

    except Exception as e:
        print_colored(f"🚨 Unexpected error: {e}", "red")

# 🧠 Safe Execution
async def run():
    try:
        await client.connect()
        await main()
    except Exception as e:
        print_colored(f"🚫 Connection issue: {e}", "red")
    finally:
        await client.disconnect()

# 🎬 Run It
asyncio.run(run())
