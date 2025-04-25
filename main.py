import os
import asyncio
from datetime import datetime
from pytz import timezone
import random

from pyrogram import Client
from telegram.ext import Updater, CommandHandler

# لیست فونت‌های زیبا برای ساعت
fonts = [
    "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡",
    "𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫",
    "⓪①②③④⑤⑥⑦⑧⑨",
    "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗",
    "𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿",
    "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵"
]

# تابع زیباسازی ساعت
def fontify(text):
    x = "0123456789"
    y = random.choice(fonts)
    return text.translate(str.maketrans(x, y))

# گرفتن مقادیر از متغیرهای محیطی
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_NAME = "my_account"

# وضعیت اجرا
running = False

# تابع آپدیت کردن بیو
async def update_bio_loop():
    global running
    app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)
    async with app:
        while running:
            now = datetime.now(timezone('Asia/Tehran'))
            current_time = now.strftime("%H:%M")
            fancy_time = fontify(current_time)
            bio_text = f"『{fancy_time}』"
            await app.update_profile(bio=bio_text)
            await asyncio.sleep(60)

# شروع با دستور /start
def start(update, context):
    global running
    if not running:
        running = True
        update.message.reply_text("⏱ ساعت فعال شد.")
        asyncio.get_event_loop().create_task(update_bio_loop())
    else:
        update.message.reply_text("ساعت از قبل فعال است.")

# توقف با دستور /stop
def stop(update, context):
    global running
    running = False
    update.message.reply_text("❌ ساعت غیرفعال شد.")

# راه‌اندازی ربات
def run_bot():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    run_bot()