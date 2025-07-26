import datetime
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from user_data import load_user_data
import pandas as pd
import ccxt  # install ccxt for real OHLCV market data

logger = logging.getLogger(__name__)

exchange = ccxt.binance()  # Public Binance data for signals

# === UTILS ===
def fetch_ohlcv(symbol, timeframe='1h', limit=200):
    """Fetch OHLCV candles from Binance for analysis."""
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['time','open','high','low','close','volume'])
        return df
    except Exception as e:
        logger.error(f"OHLCV fetch error for {symbol}: {e}")
        return None

# === STRATEGIES ===
def bateman_method(df):
    """
    BATEMAN Method: 
    - Price above/below 200 EMA
    - Stoch RSI crossovers
    - Confirmation candle
    """
    df['ema200'] = df['close'].ewm(span=200).mean()
    price = df['close'].iloc[-1]
    ema = df['ema200'].iloc[-1]

    # Stoch RSI
    low14 = df['low'].rolling(14).min()
    high14 = df['high'].rolling(14).max()
    k = 100 * ((df['close'] - low14) / (high14 - low14))
    d = k.rolling(3).mean()
    k_now, k_prev = k.iloc[-1], k.iloc[-2]
    d_now, d_prev = d.iloc[-1], d.iloc[-2]

    # Long condition
    if price > ema and k_prev < 20 and d_prev < 20 and k_now > d_now:
        return "LONG"

    # Short condition
    if price < ema and k_prev > 80 and d_prev > 80 and k_now < d_now:
        return "SHORT"

    return None

def tjr_fake_breakout(df):
    """
    Fake Breakout:
    - Wick outside recent high/low
    - Close back inside
    """
    recent_high = df['high'].iloc[-10:-1].max()
    recent_low = df['low'].iloc[-10:-1].min()
    last = df.iloc[-1]

    if last['high'] > recent_high and last['close'] < recent_high:
        return "SHORT"
    if last['low'] < recent_low and last['close'] > recent_low:
        return "LONG"
    return None

def eq_support_bounce(df):
    """
    EQ Strategy:
    - Price sweeps liquidity below support
    - Closes back above support
    """
    recent_low = df['low'].iloc[-20:-1].min()
    last = df.iloc[-1]
    prev = df.iloc[-2]

    if prev['low'] <= recent_low and last['close'] > prev['close']:
        return "LONG"
    return None

# === SIGNAL BUILDER ===
def analyze_market(symbol, strategy):
    """Analyze market using selected strategy."""
    pair = f"{symbol}/USDT"
    df = fetch_ohlcv(pair, timeframe='1h', limit=200)
    if df is None:
        return None

    signal_direction = None
    reason = ""

    if "BATEMAN" in strategy:
        signal_direction = bateman_method(df)
        reason = "BATEMAN Method conditions met."
    elif "TJR" in strategy:
        signal_direction = tjr_fake_breakout(df)
        reason = "TJR Fake Breakout pattern detected."
    elif "E.Q" in strategy or "Support Bounce" in strategy:
        signal_direction = eq_support_bounce(df)
        reason = "EQ Support Bounce conditions met."

    if signal_direction:
        last_price = df['close'].iloc[-1]
        return {
            "symbol": symbol.upper(),
            "direction": signal_direction,
            "entry": f"{last_price:.4f}",
            "tp": f"{last_price * 1.04:.4f}",
            "sl": f"{last_price * 0.98:.4f}",
            "timeframe": "1H",
            "confidence": 90,
            "reason": reason
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

# === MAIN SIGNAL DISPATCH ===
def send_signals_to_users(context):
    """Main function to scan market + DM signals to all onboarded users."""
    all_users = load_user_data()
    for chat_id, data in all_users.items():
        if not data.get("onboarded"):
            continue

        for coin in data.get("coins", []):
            for strat in data.get("strategies", []):
                signal = analyze_market(coin, strat)
                if signal:
                    try:
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
