from telethon.sync import TelegramClient, events
from deep_translator import GoogleTranslator
import requests
import os

# 👇 Change these before running on Render
api_id = 22310819
api_hash = '4bbc9600989bc876059c5fa89759c593'
bot_token = '7809362069:AAEx9ssDT50GAYl-UJLF1Dh1x1OimKjaip4'
source_channel = '@winminespro'
target_channel = '@MinesPredictor24_7'

# 📩 API URL
send_url = f"https://api.telegram.org/bot{bot_token}"

# Start Telegram client
client = TelegramClient('deep_translator_bot', api_id, api_hash)

async def main():
    await client.start()
    print("✅ Telegram login successful!")

    @client.on(events.NewMessage(chats=source_channel))
    async def handler(event):
        try:
            if event.message.sticker:
                file = await event.message.download_media()
                with open(file, 'rb') as f:
                    files = {'sticker': f}
                    data = {'chat_id': target_channel}
                    requests.post(f"{send_url}/sendSticker", data=data, files=files)
                os.remove(file)

            elif event.message.photo or event.message.video or event.message.document:
                file = await event.message.download_media()
                with open(file, 'rb') as f:
                    files = {'document': f}
                    data = {'chat_id': target_channel, 'caption': event.text or ''}
                    requests.post(f"{send_url}/sendDocument", data=data, files=files)
                os.remove(file)

            elif event.raw_text:
                translated = GoogleTranslator(source='auto', target='en').translate(event.raw_text)
                payload = {'chat_id': target_channel, 'text': translated}
                requests.post(f"{send_url}/sendMessage", data=payload)
        except Exception as e:
            print(f"❌ Error: {e}")

    print("🚀 Bot is running on Render...")
    await client.run_until_disconnected()

client.loop.run_until_complete(main())
