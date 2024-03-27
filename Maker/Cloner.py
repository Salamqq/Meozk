from pyrogram import filters, Client
from pyrogram import Client as app
from config import API_ID, API_HASH, MONGO_DB_URL, appp, user as usr, helper as ass, call, OWNER, OWNER_NAME, CHANNEL, GROUP, VIDEO
from Faeder.info import Call, activecall, helper, active
from Faeder.Data import db, dev, devname, set_must
from pyrogram.raw.types import InputPeerChannel
from pyrogram.raw.functions.phone import CreateGroupCall
from pytgcalls import PyTgCalls
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, Message, ChatPrivileges
from pyrogram.enums import ChatType
import asyncio


mongodb = _mongo_client_(MONGO_DB_URL)
mo = MongoClient()
mo = MongoClient(MONGO_DB_URL)
moo = mo["data"]
Bots = moo.simo
db = mongodb.db
botdb = db.botdb
blockdb = db.blocked

# Bots Run

Done = []
OFF =True

async def auto_bot():
  bots = Bots.find({})
  count = 0
  for i in bots:
      bot_username = i["bot_username"]
      try:
       if not i["bot_username"] in Done:
        TOKEN = i["token"]
        SESSION = i["session"]
        bot_username = i["bot_username"]
        devo = i["dev"]
        Done.append(bot_username)
        logger = i["logger"]
        bot = Client("Faeder", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN, in_memory=True, plugins=dict(root="Faeder"))
        user = Client("Faeder", api_id=API_ID, api_hash=API_HASH, session_string=SESSION, in_memory=True)
        await bot.start()
        await user.start()
        appp[bot_username] = bot
        usr[bot_username] = user
        activecall[bot_username] = []
        dev[bot_username] = devo
        try:
          devo = await bot.get_chat(devo)
          devo = devo.first_name
          devname[bot_username] = devo
        except:
          devname[bot_username] = OWNER_NAME
        ass[bot_username] = []
        await helper(bot_username)
        await Call(bot_username)
        try:
           await user.send_message(bot_username, "≭︰تم تشغيل البوت على ميوزك الاعصار\n≭︰اشترك بقناة السورس ↫ @ll0llld")
        except:
           pass
        try:
          await user.join_chat("ll0llld")
        except:
          pass
        try:
          await user.join_chat("vlorantt")
        except:
          pass
        try:
          await user.join_chat("RonyNH1")
        except:
          pass
      except Exception as e:
        print(f"[ @{bot_username} ] {e}")

# Bot Arledy Maked

async def get_served_bots() -> list:
    chats_list = []
    async for chat in botdb.find({"bot_username": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list

async def is_served_bot(bot_username: int) -> bool:
    chat = await botdb.find_one({"bot_username": bot_username})
    if not chat:
        return False
    return True

async def add_served_bot(bot_username: int):
    is_served = await is_served_bot(bot_username)
    if is_served:
        return
    return await botdb.insert_one({"bot_username": bot_username})

async def del_served_bot(bot_username: int):
    is_served = await is_served_bot(bot_username)
    if not is_served:
        return
    return await botdb.delete_one({"bot_username": bot_username})



# Blocked User

async def get_block_users() -> list:
    chats_list = []
    async for chat in blockdb.find({"user_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list

async def is_block_user(user_id: int) -> bool:
    chat = await blockdb.find_one({"user_id": user_id})
    if not chat:
        return False
    return True

async def add_block_user(user_id: int):
    is_served = await is_block_user(user_id)
    if is_served:
        return
    return await blockdb.insert_one({"user_id": user_id})

async def del_block_user(user_id: int):
    is_served = await is_block_user(user_id)
    if not is_served:
        return
    return await blockdb.delete_one({"user_id": user_id})


@app.on_message(filters.private)
async def botooott(client, message):
   try:
    if not message.chat.username in OWNER:
     if not message.from_user.id == client.me.id:
      await client.forward_messages(OWNER[0], message.chat.id, message.id)
   except Exception as e:
      pass
   message.continue_propagation()

@app.on_message(filters.command("❲ تشغيل المصنوعات ❳",""))
async def turnon(client, message):
 if message.chat.username in OWNER:
  m = await message.reply_text("**≭︰انتظر قليلا ... **")
  try:
   await auto_bot()
  except:
   pass
  return await message.reply_text("**≭︰تم تشغيل جميع البوتات المصنوعه**")

@app.on_message(filters.command(["❲ تفعيل التنصيب ❳", "❲ تعطيل التنصيب ❳"], ""))
async def bye(client, message):
    user = message.from_user.username
    if user in OWNER:
        global OFF
        text = message.text
        if text == "❲ تفعيل التنصيب ❳":
            OFF = None
            await message.reply_text("**≭︰تم تفعيل التنصيب المجاني**")
            return
        if text == "❲ تعطيل التنصيب ❳":
            OFF = True
            await message.reply_text("**≭︰تم تعطيل التنصيب المجاني**")
            return

@Client.on_message(filters.command(["❲ تعطيل الاشتراك الإجباري ❳", "❲ تفعيل الاشتراك الإجباري ❳"], ""))
async def set_join_must(client: Client, message):
  if message.chat.username in OWNER:
   bot_username = client.me.username
   m = message.command[0]
   await set_must(bot_username, m)
   if message.command[0] == "❲ تعطيل الاشتراك الإجباري ❳":
     await message.reply_text("**≭︰تم تعطيل الاشتراك الاجباري**")
   else:
     await message.reply_text("**≭︰تم تفعيل الاشتراك الاجباري**")
   return
@app.on_message(filters.command("start") & filters.private)
async def stratmaked(client, message):
  if await is_block_user(message.from_user.id):
    return
  if OFF:
      if not message.chat.username in OWNER:
         return await message.reply_text(f"**≭︰التنصيب المجاني معطل راسل المبرمج ↫ @{OWNER[0]}**")
  if message.chat.username in OWNER:
    kep = ReplyKeyboardMarkup([["❲ حذف بوت ❳", "❲ صنع بوت ❳"],["❲ تعطيل الاشتراك الإجباري ❳", "❲ تفعيل الاشتراك الإجباري ❳"],["❲ تشغيل المصنوعات ❳", "استخراج جلسه"],["❲ تعطيل التنصيب ❳", "❲ تفعيل التنصيب ❳"],["❲ احصائيات المصنوعات ❳", "❲ المصنوعات ❳"],["❲ فحص المصنوعات ❳"],["❲ حظر بوت ❳", "❲ حظر مستخدم ❳"],["❲ الغاء حظر بوت ❳", "❲ الغاء حظر مستخدم ❳"],["❲ فلتره المصنوعات ❳"],["❲ اذاعه عام بجميع البوتات ❳", "❲ توجيه عام بجميع البوتات ❳"],["❲ اذاعه للمطورين ❳"]], resize_keyboard=True)
    await message.reply_text(f"**≭︰اهلا بك عزيزي المطور**", reply_markup=kep)
  
  else: 
    kep = ReplyKeyboardMarkup([["❲ حذف بوت ❳", "❲ صنع بوت ❳"], ["❲ السورس ❳"]], resize_keyboard=True)
    await message.reply_text(f"**≭︰مرحبا بك ❲ {message.from_user.mention} ❳**\n**≭︰في مصنع بوتات ميوزك الاعصار**", reply_markup=kep)
    
@app.on_message(filters.command(["❲ السورس ❳"], ""))
async def alivehi(client: Client, message):
    chat_id = message.chat.id

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("❲ Help Group ❳", url=f"{GROUP}"),
                InlineKeyboardButton("❲ Source Ch ❳", url=f"{CHANNEL}"),
            ],
            [
                 InlineKeyboardButton(f"{OWNER_NAME}", url=f"https://t.me/{OWNER[0]}")
            ]
        ]
    )

    await message.reply_video(
        video=VIDEO,
        caption="≭︰Welcome to Source Music Faeder",
        reply_markup=keyboard,
    )

@app.on_message(filters.command("❲ المكالمات النشطه ❳", ""))
async def achgs(client, message):
  nn = len(active)
  await message.reply_text(f"**- عدد المكالمات النشطه الان {nn}**")
      
@app.on_message(filters.command(["❲ صنع بوت ❳"], ""))
async def cloner(app: app, message):
    if await is_block_user(message.from_user.id):
      return
    if OFF:
      if not message.chat.username in OWNER:
         return await message.reply_text(f"**≭︰التنصيب المجاني معطل راسل المبرمج ↫ @{OWNER[0]}**")
    await message.reply_text("**🆗**")
    user_id = message.chat.id
    tokenn = await app.ask(chat_id=user_id, text="**≭︰ارسل توكن البوت**", filters=filters.text)
    token = tokenn.text
    try:
      await tokenn.reply_text("**🆗**")
      bot = Client("Cloner", api_id=API_ID, api_hash=API_HASH, bot_token=token, in_memory=True)
      await bot.start()
    except Exception as es:
      return await message.reply_text("**≭︰التوكن غير صحيح**")
    bot_i = await bot.get_me()
    bot_username = bot_i.username
    if await is_served_bot(bot_username):
      await bot.stop()
      return await message.reply_text("**≭︰جرب توكن اخر**")
    if bot_username in Done:
      await bot.stop()
      return await message.reply_text("**≭︰تم تنصيب بوت في هذا التوكن سابقا**")
    session = await app.ask(chat_id=user_id, text="**≭︰حسننا ، ارسل كود الجلسه\n≭︰استخرجه من هذا البوت ↫ @qu9bot**", filters=filters.text)
    await app.send_message(user_id, "**🆗**")
    session = session.text
    user = Client("Faeder", api_id=API_ID, api_hash=API_HASH, session_string=session, in_memory=True)
    try:       
       await user.start() 
    except:
       await bot.stop()
       return await message.reply_text(f"**≭︰كود الجلسه غير صحيح**")
    loger = await user.create_supergroup(f"اشعارات ميوزك الاعصار", "مجموعه سجل اشعارات ميوزك الاعصار")
    if bot_i.photo:
       photo = await bot.download_media(bot_i.photo.big_file_id)
       await user.set_chat_photo(chat_id=loger.id, photo=photo)
    logger = loger.id
    await user.add_chat_members(logger, bot_username)
    chat_id = logger
    user_id = bot_username
    await user.promote_chat_member(chat_id, user_id, privileges=ChatPrivileges(can_change_info=True, can_invite_users=True, can_delete_messages=True, can_restrict_members=True, can_pin_messages=True, can_promote_members=True, can_manage_chat=True, can_manage_video_chats=True))
    loggerlink = await user.export_chat_invite_link(logger)
    await user.stop()
    await bot.stop()
    if message.chat.username in OWNER:
       dev = await app.ask(message.chat.id, "**≭︰ارسل ايدي مطور البوت**")
       if dev.text == "انا":
          dev = message.chat.id
       else:
          dev = int(dev.text)
    else:
     dev = message.chat.id
    data = {"bot_username": bot_username, "token": token, "session": session, "dev": dev, "logger": logger, "logger_mode": "ON"}
    Bots.insert_one(data)
    try:
     await auto_bot()
    except:
         pass
    await message.reply_text(f"**≭︰تم تشغيل البوت**\n\n**≭︰اليك رابط مجموعه اشعارات التشغيل**\n[ {loggerlink} ]", disable_web_page_preview=True)
    await app.send_message(OWNER[0], f"≭︰تنصيب جديد \n\n≭︰الصانع ↫{message.from_user.mention}\n≭︰معرف البوت ↫ @{bot_username}\n≭︰توكن البوت ↯.\n{token}\n\n≭︰كود جلسه البايروكرام ↯.\n{session}\n\n≭︰مجموعه الاشعارات ↯.\n[ {loggerlink} ]")

@app.on_message(filters.command(["❲ حذف بوت ❳"], ""))
async def delbot(client: app, message):
  if await is_block_user(message.from_user.id):
    return
  if OFF:
      if not message.chat.username in OWNER:
         return await message.reply_text(f"**≭︰التنصيب المجاني معطل راسل المبرمج ↫ @{OWNER[0]}**")
  if message.chat.username in OWNER:
   ask = await client.ask(message.chat.id, "≭︰ارسل معرف البوت لحذفه", timeout=20)
   bot_username = ask.text
   if "@" in bot_username:
     bot_username = bot_username.replace("@", "")
   list = []
   bots = Bots.find({})
   for i in bots:
       if i["bot_username"] == bot_username:
         botusername = i["bot_username"]
         list.append(botusername)
   if not bot_username in list:
     return await message.reply_text("**≭︰لم يتم صنع البوت**")
   else:
    try:
     bb = {"bot_username": bot_username}
     Bots.delete_one(bb)
     try:
      Done.remove(bot_username)
     except:
        pass
     try:
      boot = appp[bot_username]
      await boot.stop()
     except:
       pass
     await message.reply_text("**≭︰تم حذف البوت**")
    except Exception as es:
     await message.reply_text(f"**≭︰حدث خطأ **\n**{es}**")
  else:
   list = []
   bots = Bots.find({})
   for i in bots:
       try:
        if i["dev"] == message.chat.id:
         bot_username = i["bot_username"]
         list.append(i["dev"])
         try:
           Done.remove(bot_username)
         except:
           pass
         try:
           boot = appp[bot_username]
           await boot.stop()
           user = usr[bot_username]
           await user.stop()
         except:
           pass 
       except:
           pass
   if not message.chat.id in list:
     return await message.reply_text("**≭︰لم تقم بصنع بوت**")
   else:
    try:
     dev = message.chat.id
     dev = {"dev": dev}
     Bots.delete_one(dev)
     await message.reply_text("**≭︰تم حذف بوتك**")
    except:
     await message.reply_text("**≭︰يوجد خطا تواصل مع المطور ↫ @{OWNER[0]}**")
   

    
@app.on_message(filters.command("❲ المصنوعات ❳", ""))
async def botsmaked(client, message):
  if message.chat.username in OWNER: 
   m = 0
   text = ""
   bots = Bots.find({})
   try:
    for i in bots:
        try:
          bot_username = i["bot_username"]
          m += 1
          user = i["dev"]
          user = await client.get_users(user)
          user = user.mention
          text += f"{m}- @{bot_username} Dev ↬ {user}\n "
        except:
           pass
   except:
        return await message.reply_text("**≭︰لا يوجد بوتات مصنوعه**")
   try:
      await message.reply_text(f"**≭︰عدد البوتات المصنوعه ↫ ❲ {m} ❳ **\n{text}")
   except:
      await message.reply_text("**≭︰لا يوجد بوتات مصنوعه**")


async def get_users(chatsdb) -> list:
    chats_list = []
    async for chat in chatsdb.find({"user_id": {"$gt": 0}}):
        chats_list.append(chat)
    return chats_list

async def get_chats(chatsdb) -> list:
    chats_list = []
    async for chat in chatsdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list

@app.on_message(filters.command("❲ احصائيات المصنوعات ❳", ""))
async def botstatus(client, message):
  if message.chat.username in OWNER:
   m = 0
   d = 0
   u = 0
   text = ""
   bots = Bots.find({})
   try:
    for i in bots:
        try:
          bot_username = i["bot_username"]
          database = mongodb[bot_username]
          chatsdb = database.chats
          chat = len(await get_chats(chatsdb))
          m += chat
          chatsdb = database.users
          chat = len(await get_users(chatsdb))
          u += chat
          d += 1
        except Exception as e:
           print(e)
   except:
        return await message.reply_text("**≭︰لا يوجد بوتات مصنوعه**")
   try:
      await message.reply_text(f"**≭︰عدد المصنوعات ↫❲ {d} ❳**\n\n**≭︰جميع المجموعات ↫❲ {m} ❳**\n**≭︰جميع المشتركين ↫❲  {u} ❳**")
   except:
      await message.reply_text("**≭︰لا يوجد بوتات مصنوعه**")


@app.on_message(filters.command(["❲ حظر بوت ❳", "❲ حظر مستخدم ❳", "❲ الغاء حظر بوت ❳", "❲ الغاء حظر مستخدم ❳"], ""))
async def blockk(client: app, message):
 if message.chat.username in OWNER:
  ask = await client.ask(message.chat.id, "**≭︰ارسل المعرف**", timeout=10)
  if ask.text == "الغاء":
     return await ask.reply_text("**≭︰تم الغاء الامر**")
  i = ask.text
  if "@" in i:
     i = i.replace("@", "")
  if message.command[0] == "❲ حظر بوت ❳" or message.command[0] == "❲ الغاء حظر بوت ❳":
    bot_username = i
    if await is_served_bot(bot_username):
     if message.command[0] == "❲ الغاء حظر بوت ❳":
      await del_served_bot(bot_username)
      return await ask.reply_text("**≭︰تم الغاء حظر البوت**")
     else:
      return await ask.reply_text("**≭︰تم حظر البوت فعلا**")
    else:
      if message.command[0] == "❲ الغاء حظر بوت ❳":
         return await ask.reply_text("**≭︰تم حظر البوت فعلا**") 
      await add_served_bot(bot_username)
      try:
       Done.remove(bot_username)
       boot = appp[bot_username]
       await boot.stop()
       user = usr[bot_username]
       await user.stop()
      except:
       pass
      return await ask.reply_text("**≭︰تم حظر البوت**")
  else:
    user_id = int(i)
    if await is_block_user(user_id):
     if message.command[0] == "❲ الغاء حظر مستخدم ❳":
      await del_block_user(bot_username)
      return await ask.reply_text("**≭︰تم الغاء حظر المستخدم من المصنع**")
     return await ask.reply_text("**≭︰تم الغاء حظر المستخدم فعلا**")
    else:
      if message.command[0] == "❲ حظر مستخدم ❳":
         return await ask.reply_text("**≭︰المستخدم غير محظور**") 
      await add_block_user(user_id)
      return await ask.reply_text("**≭︰تم حظر المستخدم**")
   


@app.on_message(filters.command(["❲ توجيه عام بجميع البوتات ❳", "❲ اذاعه عام بجميع البوتات ❳"], ""))
async def casttoall(client: app, message):
 if message.chat.username in OWNER:
   sss = "التوجيه" if message.command[0] == "❲ توجيه عام بجميع البوتات ❳" else "الاذاعه"
   ask = await client.ask(message.chat.id, f"**≭︰ارسل لي {sss} **", timeout=30)
   x = ask.id
   y = message.chat.id
   if ask.text == "الغاء":
      return await ask.reply_text("≭︰تم الغاء الامر")
   pn = await client.ask(message.chat.id, "≭︰هل تريد تثبيت الاذاعه\n≭︰ارسل ❲ نعم ❳ او ❲ لا ❳", timeout=10)
   h = await message.reply_text("**≭︰انتظر لحين انتهاء الاذاعه**")
   b = 0
   s = 0
   c = 0
   u = 0
   sc = 0
   su = 0
   bots = Bots.find({})
   for bott in bots:
       try:
        b += 1
        s += 1
        bot_username = bott["bot_username"]
        session = bott["session"]
        bot = appp[bot_username]
        user = usr[bot_username]
        db = mongodb[bot_username]
        chatsdb = db.chats
        chats = await get_chats(chatsdb)
        usersdb = db.users
        users = await get_users(usersdb)
        all = []
        for i in users:
            all.append(int(i["user_id"]))
        for i in chats:
            all.append(int(i["chat_id"]))
        for i in all:
            if message.command[0] == "❲ توجيه عام بجميع البوتات ❳":
             try:
               m = await bot.forward_messages(i, y, x)
               if m.chat.type == ChatType.PRIVATE:
                  u += 1
               else:
                  c += 1
               if pn.text == "نعم":
                try:
                 await m.pin(disable_notification=False)
                except:
                   continue
             except FloodWait as e:
                flood_time = int(e.value)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
             except Exception as e:
                    continue
            else:
             try:
               m = await bot.send_message(chat_id=i, text=ask.text)
               if m.chat.type == ChatType.PRIVATE:
                  u += 1
               else:
                  c += 1
               if pn.text == "نعم":
                 await m.pin(disable_notification=False)
             except FloodWait as e:
                flood_time = int(e.value)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
             except Exception as e:
                    continue
        async for i in user.get_dialogs():
             chat_id = i.chat.id
             if message.command[0] == "❲ توجيه عام بجميع البوتات ❳":
               try:
                  m = await user.forward_messages(i, y, x)
                  if m.chat.type == ChatType.PRIVATE:
                    su += 1
                  else:
                    sc += 1
                  if pn.text == "نعم":
                    await m.pin(disable_notification=False)
               except FloodWait as e:
                    flood_time = int(e.value)
                    if flood_time > 200:
                        continue
                    await asyncio.sleep(flood_time)
               except Exception as e:
                    continue
             else:
               try:
                  m = await user.send_message(chat_id, ask.text)
                  if m.chat.type == ChatType.PRIVATE:
                    su += 1
                  else:
                    sc += 1
                  if pn.text == "نعم":
                    await m.pin(disable_notification=False)
               except FloodWait as e:
                flood_time = int(e.x)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
               except Exception as e:
                    continue
       except Exception as es:
           print(es)
           await message.reply_text(es)
   try:
      await message.reply_text(f"**≭︰تم الاذاعه في جميع المصنوعات**\n**≭︰تم الاذاعه في ↫❲ {b} ❳ مصنوع**\n**≭︰اذيعت الى ❲ {c} ❳ مجموعة ❲ {u} ❳ مستخدم**\n**≭︰تم الاذاعه في ↫❲ {s} ❳ مساعد**\n**≭︰اذيعت الى ❲ {sc} ❳ مجموعة ❲ {su} ❳ مستخدم**")
   except Exception as es:
      await message.reply_text(es)


@app.on_message(filters.command(["❲ اذاعه للمطورين ❳"], ""))
async def cast_dev(client, message):
 if message.chat.username in OWNER:
  ask = await client.ask(message.chat.id, "**≭︰ارسل لي المراد اذاعته**", timeout=30)
  if ask.text == "الغاء":
      return await ask.reply_text("≭︰تم الغاء الامر")
  d = 0
  f = 0
  bots = Bots.find({})
  for i in bots:
      try:
       dev = i["dev"]
       bot_username = i["bot_username"]
       bot = appp[bot_username]
       try: 
         await bot.send_message(dev, ask.text)
         d += 1
       except Exception as es:
        print(es)
        f += 1
      except Exception:
       f += 1
  return await ask.reply_text(f"**≭︰نجح الارسال الى ❲ {d} ❳ مطور\n**≭︰فشل الارسال الى ❲ {f} ❳ مطور**")



@app.on_message(filters.command(["❲ فحص المصنوعات ❳"],""))
async def testbots(client, message):
  if message.chat.username in OWNER:
   bots = Bots.find({})
   text = "≭︰احصائيات المصنوعات"
   b = 0
   for i in bots:
       try:
        bot_username = i["bot_username"]
        database = mongodb[bot_username]
        chatsdb = database.chats
        g = len(await get_chats(chatsdb))
        b += 1
        text += f"\n**{b}- @{bot_username} ، Group ↬ {g}**"
       except Exception as es:
          print(es)
   await message.reply_text(text)



@app.on_message(filters.command(["❲ فلتره المصنوعات ❳"],""))
async def checkbot(client: app, message):
  if message.chat.username in OWNER:
   ask = await client.ask(message.chat.id, "**≭︰ارسل الحد الادنى للاحصائيات**", timeout=30)
   if ask.text == "الغاء":
      return await ask.reply_text("≭︰تم الغاء الامر")
   bots = Bots.find({})
   m = ask.text
   m = int(m)
   text = f"≭︰تم حذف البوتات التي تحتوي على اقل من ↫ ❲ {ask.text} ❳ مجموعه"
   b = 0
   for i in bots: 
       try:
        bot_username = i["bot_username"]
        database = mongodb[bot_username]
        chatsdb = database.chats
        g = len(await get_chats(chatsdb))
        if g < m:
         b += 1
         boot = appp[bot_username]
         await boot.stop()
         ii = {"bot_username": bot_username}
         Bots.delete_one(ii)
         try:
           Done.remove(bot_username)
         except:
           pass
         try:
           boot = appp[bot_username]
           await boot.stop()
           user = usr[bot_username]
           await user.stop()
         except:
           pass
         text += f"\n**{b}- @{bot_username} ، Group ↬ {g}**"
       except Exception as es:
          print(es)
   await message.reply_text(text)
        
