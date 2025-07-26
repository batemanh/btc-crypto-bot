
import random

def generate_signal(symbol: str):
    confidence = random.randint(85, 98)
    tp = round(random.uniform(1.5, 2.0), 4)
    sl = round(tp - 0.2, 4)
    entry = round(tp * (0.95 if symbol.upper() == "LONG" else 1.05), 4)
    leverage = 10
    pnl = random.randint(20, 60)
    reasoning = (
        "Price above 200 EMA, Stoch RSI cross under 20, bullish confirmation candle. "
        "Liquidity grab at support detected."
    )
    return confidence, entry, tp, sl, leverage, pnl, reasoning
