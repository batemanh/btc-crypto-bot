import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
MESSAGE = "✅ Your crypto bot is alive and secured using .env!"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def main():
    response = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": MESSAGE
    })

    if response.status_code == 200:
        print("✅ Message sent successfully.")
    else:
        print(f"❌ Failed to send message: {response.status_code} - {response.text}")

if __name__ == "__main__":
    main()
