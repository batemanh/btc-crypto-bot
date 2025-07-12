import requests

# Replace these with your actual token and chat ID
TOKEN = "7545012974:AAFIcvjj33l-fsQZLRMQqdyHc7EOvCyLBkc"
CHAT_ID = "1020455648493"
MESSAGE = "🚀 Your bot is ALIVE and connected to Telegram!"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def main():
    try:
        response = requests.post(url, data={"chat_id": CHAT_ID, "text": MESSAGE})
        if response.status_code == 200:
            print("✅ Message sent successfully.")
        else:
            print(f"❌ Failed to send message. Status code: {response.status_code}")
            print("Response:", response.text)
    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    main()
