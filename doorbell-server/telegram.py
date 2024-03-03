from telegram import Bot
from telegram.error import NetworkError, Unauthorized

# Substitua pelo token do seu bot
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

def send_photo(chat_id, photo_path):
    bot = Bot(TOKEN)
    try:
        bot.send_photo(chat_id=chat_id, photo=open(photo_path, 'rb'))
    except (NetworkError, Unauthorized) as e:
        print(f"Erro ao enviar foto: {e}")

def send_audio(chat_id, audio_path):
    bot = Bot(TOKEN)
    try:
        bot.send_audio(chat_id=chat_id, audio=open(audio_path, 'rb'))
    except (NetworkError, Unauthorized) as e:
        print(f"Erro ao enviar áudio: {e}")

if __name__ == "__main__":
    # Substitua pelo seu chat_id
    CHAT_ID = 'YOUR_CHAT_ID'
    send_photo(CHAT_ID, 'visitor_image.jpg')
    send_audio(CHAT_ID, 'visitor_audio.wav')
