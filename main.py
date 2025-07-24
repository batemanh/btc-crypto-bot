import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater, CommandHandler, CallbackContext,
    CallbackQueryHandler, MessageHandler, Filters
)
import json

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load or create user preferences
USER_DATA_FILE = 'user_data.json'

def load_user_data():
    try:
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_user_data(data):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

user_data = load_user_data()

# Define coins and strategies
coin_options = ['BTC', 'ETH', 'XRP', 'SOL']
strategy_options = ['BATEMAN Method™', 'TJR Fake Breakout', 'E.Q Support Bounce']

# /start command
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    chat_id = update.effective_chat.id

    user_data[str(chat_id)] = {
        "coins": [],
        "strategies": [],
        "onboarded": False
    }
    save_user_data(user_data)

    intro = (
        f"🧠 Welcome to **Mini Bateman**.\n\n"
        "This isn’t a bot — this is an extension of my brain.\n"
        "You’re about to unlock a level of trading, mindset, and wealth-building that most people never even touch.\n\n"
        "🚨 I built this for total beginners. That means no more:\n"
        "• YouTube rabbit holes\n"
        "• Confusing chart calls\n"
        "• Clueless entries\n\n"
        "**This is me walking you through every step.**\n"
        "Tap below to begin your setup. Let’s build your empire."
    )

    keyboard = [[InlineKeyboardButton("🚀 Let’s Begin", callback_data='start_setup')]]
    update.message.reply_text(intro, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

# Start setup
def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    chat_id = str(query.message.chat.id)
    step = user_data.get(chat_id, {}).get("step", None)

    if query.data == "start_setup":
        user_data[chat_id]["step"] = "select_coins"
        save_user_data(user_data)
        send_coin_selection(query)

    elif query.data.startswith("coin_"):
        coin = query.data.split("_")[1]
        toggle_selection(user_data[chat_id]["coins"], coin)
        save_user_data(user_data)
        send_coin_selection(query, edit=True)

    elif query.data == "done_coins":
        user_data[chat_id]["step"] = "select_strategies"
        save_user_data(user_data)
        send_strategy_selection(query)

    elif query.data.startswith("strat_"):
        strat = query.data.split("_")[1]
        toggle_selection(user_data[chat_id]["strategies"], strat)
        save_user_data(user_data)
        send_strategy_selection(query, edit=True)

    elif query.data == "done_strategies":
        user_data[chat_id]["onboarded"] = True
        save_user_data(user_data)
        query.edit_message_text("✅ Setup complete.\n\nFrom this moment forward, signals will hit your inbox based on real market conditions — not guesses.\n\n**Watch your inbox. Mini Bateman moves in silence.**", parse_mode="Markdown")

# Toggle selection utility
def toggle_selection(selection_list, item):
    if item in selection_list:
        selection_list.remove(item)
    else:
        selection_list.append(item)

# Coin selection UI
def send_coin_selection(query, edit=False):
    chat_id = str(query.message.chat.id)
    selected = user_data[chat_id]["coins"]
    buttons = [[InlineKeyboardButton(f"{'✅' if c in selected else '➕'} {c}", callback_data=f"coin_{c}")] for c in coin_options]
    buttons.append([InlineKeyboardButton("✔️ Done", callback_data="done_coins")])
    msg = "📊 Select the coins you want to trade. You can pick more than one."

    if edit:
        query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        query.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(buttons))

# Strategy selection UI
def send_strategy_selection(query, edit=False):
    chat_id = str(query.message.chat.id)
    selected = user_data[chat_id]["strategies"]
    buttons = [[InlineKeyboardButton(f"{'✅' if s in selected else '➕'} {s}", callback_data=f"strat_{s}")] for s in strategy_options]
    buttons.append([InlineKeyboardButton("✔️ Done", callback_data="done_strategies")])
    msg = "🧠 Choose your strategies. These are the minds you’ll be using to strike."

    if edit:
        query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        query.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(buttons))

# Error logging
def error_handler(update: object, context: CallbackContext) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# Launch bot
def main():
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN", use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button_handler))
    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
