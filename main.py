import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater, CommandHandler, CallbackContext,
    CallbackQueryHandler, MessageHandler, Filters
)
from user_data import (
    load_user_data, save_user_data,
    set_user_coins, set_user_strategies
)

# LOGGING
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# GLOBALS
user_data = load_user_data()
coin_options = ['BTC', 'ETH', 'XRP', 'SOL']
strategy_options = ['BATEMAN Method™', 'TJR Fake Breakout', 'E.Q Support Bounce']

# --- /START COMMAND ---
def start(update: Update, context: CallbackContext) -> None:
    chat_id = str(update.effective_chat.id)
    user_data[chat_id] = {"coins": [], "strategies": [], "onboarded": False}
    save_user_data(user_data)

    intro = (
        "🧠 This isn’t a bot. This is my brain in code.\n\n"
        "Signals. Mindset. P&L tracking.\n"
        "Everything you need to escape.\n\n"
        "Press start below. Let’s set this up."
    )
    keyboard = [[InlineKeyboardButton("🚀 Let’s Begin", callback_data='start_setup')]]
    update.message.reply_text(intro, reply_markup=InlineKeyboardMarkup(keyboard))

# --- SETUP STEPS ---
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
        set_user_coins(chat_id, user_data[chat_id]["coins"])
        send_coin_selection(query, edit=True)

    elif query.data == "done_coins":
        user_data[chat_id]["step"] = "select_strategies"
        save_user_data(user_data)
        send_strategy_selection(query)

    elif query.data.startswith("strat_"):
        strat = query.data.split("_")[1]
        toggle_selection(user_data[chat_id]["strategies"], strat)
        set_user_strategies(chat_id, user_data[chat_id]["strategies"])
        send_strategy_selection(query, edit=True)

    elif query.data == "done_strategies":
        user_data[chat_id]["onboarded"] = True
        save_user_data(user_data)
        query.edit_message_text(
            "✅ Setup complete. From now on, signals will DM you the moment they trigger."
        )

# --- SIGNAL SENDER PLACEHOLDER (REAL-TIME) ---
def send_signal(context: CallbackContext, chat_id: str, signal: dict):
    """
    This is where real-time signal delivery happens.
    `signal` is a dictionary containing:
    {symbol, direction, entry, tp, sl, timeframe, confidence, reason}
    """
    text = (
        f"🚨 {signal['direction']} | {signal['symbol']} [{signal['timeframe']}]\n"
        f"💎 Confidence: {signal['confidence']}%\n"
        f"Reason: {signal['reason']}\n\n"
        f"💰 Entry: {signal['entry']}\n"
        f"🎯 TP: {signal['tp']}\n"
        f"🛑 SL: {signal['sl']}\n"
    )

    keyboard = [[
        InlineKeyboardButton("📘 Why This Trade?", callback_data='explain_trade')
    ]]

    context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- HELPERS ---
def toggle_selection(selection_list, item):
    if item in selection_list:
        selection_list.remove(item)
    else:
        selection_list.append(item)

def send_coin_selection(query, edit=False):
    chat_id = str(query.message.chat.id)
    selected = user_data[chat_id]["coins"]
    buttons = [[InlineKeyboardButton(f"{'✅' if c in selected else '➕'} {c}", callback_data=f"coin_{c}")] for c in coin_options]
    buttons.append([InlineKeyboardButton("✔️ Done", callback_data="done_coins")])
    msg = "📊 Select coins you want signals for:"

    if edit:
        query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        query.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(buttons))

def send_strategy_selection(query, edit=False):
    chat_id = str(query.message.chat.id)
    selected = user_data[chat_id]["strategies"]
    buttons = [[InlineKeyboardButton(f"{'✅' if s in selected else '➕'} {s}", callback_data=f"strat_{s}")] for s in strategy_options]
    buttons.append([InlineKeyboardButton("✔️ Done", callback_data="done_strategies")])
    msg = "🧠 Choose strategies:"

    if edit:
        query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        query.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(buttons))

# --- MAIN ---
def main():
    updater = Updater("YOUR_BOT_TOKEN", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
