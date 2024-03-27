from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN
from pyromod import listen



bot = Client(
    "mo",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="Maker")
    ) 

async def start_bot():
    print("[INFO]: جاري تشغيل البوت")
    await bot.start()
    S_1_02 = "S_1_02"
    await bot.send_message(S_1_02, "≭︰تم تشغيل مصنع ميوزك الاعصار")
    print("[INFO]: بدأ تشغيل سورس ميوزك الاعصار")
    await idle()
