import logging
from telegram import Bot
from utils import get_signal_data, get_news_summary, get_chart_screenshot, calculate_pnl
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

bot = Bot(token=TELEGRAM_TOKEN)

logging.basicConfig(level=logging.INFO)

def send_trade_signal(direction, symbol, entry_price, leverage, tp, sl, timeframe, strategy, show_chart=False):
    news = get_news_summary(symbol)
    reasoning = f"{strategy} strategy triggered ({direction.upper()})"

    message = f"""
📊 {symbol.upper()} {direction.upper()} SIGNAL

💰 Entry: {entry_price}
🎯 TP: {tp} 🛑 SL: {sl}
📈 Leverage: {leverage}x ⏱️ Timeframe: {timeframe}
📌 Strategy: {reasoning}
📰 News: {news.strip() if news else "No major headlines"}

⚠️ Always use proper risk management.
""".strip()

    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

    if show_chart:
        screenshot = get_chart_screenshot(symbol)
        if screenshot:
            bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=screenshot)

def send_trade_exit(symbol, direction, entry, exit_price, leverage, sl, tp, strategy, show_chart=False):
    pnl = calculate_pnl(entry, exit_price, direction, leverage)
    news = get_news_summary(symbol)

    message = f"""
✅ {symbol.upper()} {direction.upper()} TRADE CLOSED

📥 Entry: {entry} 📤 Exit: {exit_price}
📈 PnL: {pnl:.2f}%
⚙️ Leverage: {leverage}x 🎯 TP: {tp} 🛑 SL: {sl}
📌 Reason: Exit per {strategy} logic
📰 News: {news.strip() if news else "No major headlines"}
""".strip()

    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

    if show_chart:
        screenshot = get_chart_screenshot(symbol)
        if screenshot:
            bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=screenshot)
