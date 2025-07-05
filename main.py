# 📦 Install: pip install telethon deep-translator requests

from telethon.sync import TelegramClient, events
from deep_translator import GoogleTranslator
import requests

# 🔐 Configuration
api_id = 22310819
api_hash = '4bbc9600989bc876059c5fa89759c593'
bot_token = '7809362069:AAEx9ssDT50GAYl-UJLF1Dh1x1OimKjaip4'
source_channel = '@winminespro'
target_channel = '@MinesPredictor24_7'

# Telegram Bot Send URL
send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

# Start client
client = TelegramClient('deep_translator_bot', api_id, api_hash)

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    try:
        original = event.raw_text
        translated = GoogleTranslator(source='auto', target='en').translate(original)

        payload = {
            'chat_id': target_channel,
            'text': f"🌍 Translated Message:\n{translated}"
        }

        r = requests.post(send_url, data=payload)
        print(f"✅ Message sent: {translated}")
    except Exception as e:
        print(f"❌ Error: {e}")

print("🚀 Bot is running... Listening for messages.")
client.start()
client.run_until_disconnected()
