from telethon import TelegramClient
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsRecent
import asyncio

# 🔐 Replace these with your actual Telegram API credentials
api_id = 123456     # ← Your actual API ID
api_hash = 'your_api_hash'  # ← Your actual API Hash
group_username = 'yourgroupusername'  # ← Username of your public group (without @)

async def main():
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start()

    # 📩 Generate invite link
    try:
        invite = await client(ExportChatInviteRequest(group_username))
        print(f"📨 Group Invite Link: {invite.link}")
    except Exception as e:
        print(f"❌ Failed to get invite link: {e}")
        return

    # 👥 Fetch recent members and send them a message
    try:
        users = await client(GetParticipantsRequest(group_username, ChannelParticipantsRecent(), 0, 100, hash=0))
        for user in users.users:
            try:
                await client.send_message(user.id, "🔥 PUBG Event: New zone unlocked! Collect your Surprise Flare Gun now.")
                print(f"✅ Message sent to: {user.username or user.id}")
            except Exception as e:
                print(f"❌ Couldn't message {user.id}: {e}")
    except Exception as e:
        print(f"❌ Failed to fetch group members: {e}")
    
    await client.disconnect()

asyncio.run(main())
