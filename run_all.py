
import time
from datetime import datetime
import pytz
from get_price_and_signal import generate_signal
from main import send_trade_signal

# List of symbols to track
SYMBOLS = ["BTCUSDT", "ETHUSDT", "XRPUSDT"]

while True:
    for symbol in SYMBOLS:
        try:
            print(f"[{datetime.now(pytz.UTC)}] Generating signal for {symbol}...")
            confidence, entry, tp, sl, leverage, pnl, reasoning = generate_signal(symbol)

            direction = "LONG" if confidence > 50 else "SHORT"
            send_trade_signal(
                symbol=symbol,
                direction=direction,
                entry=entry,
                leverage=leverage,
                tp=tp,
                sl=sl,
                strategy="BATEMAN Method",
                show_chart=False,
            )

            time.sleep(5)
        except Exception as e:
            print(f"[ERROR] {symbol}: {e}")
            time.sleep(60)
