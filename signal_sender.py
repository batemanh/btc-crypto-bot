import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from user_data import load_user_data
import logging

logger = logging.getLogger(__name__)

# Simulated market analysis (replace with real strategy logic later)
def analyze_market(symbol: str, strategy: str):
    """
    Placeholder analysis logic for signals.
    Replace this with your real BATEMAN Method™, TJR, EQ logic.
    Must return None if no setup is valid.
    """
    now = datetime.datetime.utcnow()
    # Example condition (fake): every hour send a long for demo
    if now.minute == 0:
        return {
            "symbol": symbol.upper(),
            "direction": "LONG",
            "entry": "0.5891",
            "tp": "0.6160",
            "sl": "0.5748",
            "timeframe": "4H",
            "confidence": 91,
            "reason": f"{strategy} conditions met (EMA+RSI alignment)."
        }
    return None

def build_signal_text(signal):
    return (
        f"🚨 {signal['direction']} ENTRY | {signal['symbol']} [{signal['timeframe']}]\n"
        f"💎 Confidence: {signal['confidence']}%\n"
        f"Reason: {signal['reason']}\n\n"
        f"💰 Entry: {signal['entry']}\n"
        f"🎯 Take Profit: {signal['tp']}\n"
        f"🛑 Stop Loss: {signal['sl']}\n\n"
        "🧠 What you’re not changing, you’re choosing."
    )

def send_signals_to_users(context):
    """Main function to scan market + DM signals to all onboarded users."""
    all_users = load_user_data()
    for chat_id, data in all_users.items():
        if not data.get("onboarded"):
            continue

        # Go through each coin/strategy the user selected
        for coin in data.get("coins", []):
            for strat in data.get("strategies", []):
                # Analyze market for setups
                signal = analyze_market(coin, strat)
                if signal:
                    try:
                        # Send message
                        text = build_signal_text(signal)
                        keyboard = [[
                            InlineKeyboardButton("📘 Why This Trade?", callback_data='explain_trade'),
                            InlineKeyboardButton("📈 How to Place It", callback_data='help_trade')
                        ]]
                        context.bot.send_message(
                            chat_id=int(chat_id),
                            text=text,
                            reply_markup=InlineKeyboardMarkup(keyboard)
                        )
                    except Exception as e:
                        logger.error(f"Failed to send signal to {chat_id}: {e}")
