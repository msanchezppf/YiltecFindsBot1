"""
main.py — Arranca Discord y Telegram a la vez
"""
import threading
import os
from dotenv import load_dotenv

load_dotenv()

def run_discord():
    import bot
    # bot.py ya tiene el bot.run(TOKEN) al final
    os.system("python bot.py")

def run_telegram():
    from telegram_bot import main
    main()

if __name__ == "__main__":
    t1 = threading.Thread(target=run_discord, daemon=True)
    t1.start()
    run_telegram()
