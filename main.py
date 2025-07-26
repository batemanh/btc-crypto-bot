import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
from get_price_and_signal import get_signal_for_symbol

# === CONFIG ===
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # replace with your real token
ADMIN_ID = 123456789  # replace with your telegram id for admin testing

# === LOGGING ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# === COMMANDS ===
def start(update, context):
    user = update.message.from_user
    update.message.reply_text(
        f"Welcome {user.first_name}.\n\n"
        f"This is Mini Bateman.\n"
        f"Type /analyze BTC or /analyze BTC ETH XRP to get signals."
    )

def analyze(update, context):
    chat_id = update.message.chat_id
    args = context.args

    if not args:
        update.message.reply_text("Use: /analyze BTC or /analyze BTC ETH")
        return

    for symbol in args:
        try:
            signal = get_signal_for_symbol(symbol.upper())
            if not signal:
                update.message.reply_text(f"No valid setup found for {symbol.upper()}.")
                continue

            text = (
                f"🚨 *{signal['direction']} ENTRY | {signal['symbol']} [{signal['timeframe']}] — {signal['trade_type']}*\n\n"
                f"💎 *Confidence:* {signal['confidence']}%\n"
                f"📈 *Market Sentiment:* {signal['market_sentiment']}\n"
                f"🧠 *Reasoning:* {signal['reasoning']}\n\n"
                f"💰 *Entry:* {signal['entry']}\n"
                f"🎯 *Take Profit:* {signal['tp']}\n"
                f"🛑 *Stop Loss:* {signal['sl']}\n"
                f"⚙️ *Leverage:* {signal['leverage']}x\n"
                f"📊 *PnL Potential:* {signal['pnl']}%\n\n"
                f"_Signal by Mini Bateman | BATEMAN Method™_\n"
                f"“What you’re not changing, you’re choosing.”"
            )

            context.bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.MARKDOWN)

        except Exception as e:
            logger.error(e)
            update.message.reply_text(f"Error analyzing {symbol.upper()}")

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# === MAIN ===
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("analyze", analyze))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
