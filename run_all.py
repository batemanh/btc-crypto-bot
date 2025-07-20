# run_all.py
import time
from get_price_and_signal import get_trade_signal, get_exit_signal
from main import send_trade_signal, send_trade_exit

# Set your trading symbols and strategies here
symbols = ['BTC', 'ETH', 'XRP']
timeframe = '4h'
strategy = 'top_ai'  # or 'tjr', 'eq', etc.

# Optional: prevent duplicate alerts
open_positions = {}

while True:
    for symbol in symbols:
        try:
            signal = get_trade_signal(symbol, timeframe, strategy)

            if signal and symbol not in open_positions:
                send_trade_signal(
                    symbol=symbol,
                    entry_price=signal['entry'],
                    tp=signal['tp'],
                    sl=signal['sl'],
                    direction=signal['direction'],
                    leverage=signal['leverage'],
                    strategy=strategy,
                    show_chart=True
                )
                open_positions[symbol] = signal

            # Check for exit
            elif symbol in open_positions:
                exit_info = get_exit_signal(symbol, strategy)
                if exit_info:
                    send_trade_exit(
                        symbol=symbol,
                        entry_price=open_positions[symbol]['entry'],
                        exit_price=exit_info['exit_price'],
                        direction=open_positions[symbol]['direction'],
                        pnl=exit_info['pnl'],
                        strategy=strategy
                    )
                    del open_positions[symbol]

        except Exception as e:
            print(f"[ERROR] {symbol} - {e}")

    time.sleep(60)  # wait 1 minute before next scan
