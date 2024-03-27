import asyncio
from config import OWNER, OWNER_NAME, PHOTO
from pyrogram import Client, filters
from Faeder.info import (remove_active, is_served_call, joinch)
from Faeder.Data import (get_call, get_dev, get_group, get_channel)
from Faeder.info import (add, db, download, gen_thumb)
from pytgcalls import PyTgCalls, StreamType
from pyrogram.enums import ChatType, ChatMemberStatus
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import (HighQualityAudio,
                                                  HighQualityVideo,
                                                  LowQualityAudio,
                                                  LowQualityVideo,
                                                  MediumQualityAudio,
                                                  MediumQualityVideo)

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import CallbackQuery
import os

@Client.on_callback_query(
    filters.regex(pattern=r"^(pause|skip|stop|resume|skip)$")
)
async def admin_risghts(client: Client, CallbackQuery):
  try:
    a = await client.get_chat_member(CallbackQuery.message.chat.id, CallbackQuery.from_user.id)
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if not a.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
     if not CallbackQuery.from_user.id == dev:
      if not CallbackQuery.from_user.username in OWNER:
        return await CallbackQuery.answer("≭︰انت لست مشرف", show_alert=True)
    command = CallbackQuery.matches[0].group(1)
    chat_id = CallbackQuery.message.chat.id
    if not await is_served_call(client, chat_id):
        return await CallbackQuery.answer("≭︰لم تقم بتشغيل شي", show_alert=True)
    call = await get_call(bot_username)
    chat_id = CallbackQuery.message.chat.id
    if command == "pause":
        await call.pause_stream(chat_id)
        await CallbackQuery.answer("≭︰تم ايقاف التشغيل موقتا", show_alert=True)
        await CallbackQuery.message.reply_text(f"{CallbackQuery.from_user.mention} **≭︰تم ايقاف التشغيل بواسطه ↫**")
    if command == "resume":
        await call.resume_stream(chat_id)
        await CallbackQuery.answer("≭︰تم استئناف التشغيل", show_alert=True)
        await CallbackQuery.message.reply_text(f"{CallbackQuery.from_user.mention} **≭︰تم استئناف التشغيل بواسطه ↫**")
    if command == "stop":
        try:
         await call.leave_group_call(chat_id)
        except:
          pass
        await remove_active(bot_username, chat_id)
        await CallbackQuery.answer("≭︰تم ايقاف التشغيل ", show_alert=True)
        await CallbackQuery.message.reply_text(f"{CallbackQuery.from_user.mention} **≭︰تم انهاء التشغيل بواسطه ↫**")
    if command == "skip" :
       chat = f"{bot_username}{chat_id}"
       check = db.get(chat)
       popped = check.pop(0)
       if not check:
         await call.leave_group_call(chat_id)
         await remove_active(bot_username, chat_id)
         return await CallbackQuery.message.reply_text("**≭︰لا يوجد شئ في قائمه التشغيل**")
       file = check[0]["file_path"]
       title = check[0]["title"]
       dur = check[0]["dur"]
       video = check[0]["vid"]
       videoid = check[0]["videoid"]
       user_id = check[0]["user_id"]
       link = check[0]["link"]
       audio_stream_quality = MediumQualityAudio()
       video_stream_quality = MediumQualityVideo()
       if file:
         file_path = file
       else:     
         try:
            file_path = await download(bot_username, link, video)
         except:
            return client.send_message(chat_id, "**≭︰حدثت مشكله اثناء تشغيل المقطع التالي**")
       stream = (AudioVideoPiped(file_path, audio_parameters=audio_stream_quality, video_parameters=video_stream_quality) if video else AudioPiped(file_path, audio_parameters=audio_stream_quality))
       try:
           await call.change_stream(chat_id, stream)
       except Exception:
            return await client.send_message(chat_id, "**≭︰حدثت مشكله اثناء تشغيل المقطع التالي**")
       userx = await client.get_users(user_id)
       if videoid:
         if userx.photo:
            photo_id = userx.photo.big_file_id
         else:
            Anwar = await client.get_chat("S_1_02")
            photo_id = Anwar.photo.big_file_id
         photo = await client.download_media(photo_id)
         img = await gen_thumb(videoid, photo)
       else:
         img = PHOTO
       requester = userx.mention       
       gr = await get_group(bot_username)
       ch = await get_channel(bot_username)
       button = [
           [
           InlineKeyboardButton(text=f"{title}",url=f"{ch}")
           ],[
           InlineKeyboardButton(text="❲ ايقاف ⏺ ❳", callback_data=f"stop")
           ],[
           InlineKeyboardButton(text="❲ ايقاف مؤقت ▶️ ❳", callback_data=f"pause"),
           InlineKeyboardButton(text="❲ استئناف ⏸ ❳", callback_data=f"resume")
           ],[
           InlineKeyboardButton(text="❲ تخطي ⏯ ❳", callback_data=f"skip")
           ],[ 
           InlineKeyboardButton(text="❲ Channel Bot ❳", url=f"{ch}")
           ]] 
       await CallbackQuery.message.reply_photo(photo=img, caption=f"**≭︰تم التخطي الى التالي **\n\n**≭︰مدة الاغنيه** ↫❲ {dur} ❳\n**≭︰طلبت من** ↫❲ {requester} ❳", reply_markup=InlineKeyboardMarkup(button)) 
       os.system('rm -rf ./downloads/*')
  except:
     pass

@Client.on_message(filters.command(["/stop", "/end", "/skip", "/resume", "/pause", "/loop", "ايقاف مؤقت", "استكمال", "تخطي", "انهاء", "اسكت", "ايقاف", "تكرار", "كررها"], "") & ~filters.private)
async def admin_risght(client: Client, message):
  try:
    if await joinch(message):
            return
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if not message.chat.type == ChatType.CHANNEL:
     a = await client.get_chat_member(message.chat.id, message.from_user.id)
     if not a.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
      if not message.from_user.id == dev:
       if not message.from_user.username in OWNER:
        return await message.reply_text("**≭︰انت لست مشرف**")
    command = message.command[0]
    chat_id = message.chat.id
    if not await is_served_call(client, chat_id):
        return await message.reply_text("**≭︰لا يوجد شئ في قائمه التشغيل**")
    call = await get_call(bot_username)
    chat_id = message.chat.id
    if command == "/pause" or command == "ايقاف مؤقت":
        await call.pause_stream(chat_id)
        await message.reply_text(f"**≭︰تم ايقاف التشغيل مؤقتا**")
    elif command == "/resume" or command == "استكمال" or command == "استئناف":
        await call.resume_stream(chat_id)
        await message.reply_text(f"**≭︰تم استئناف التشغيل**")
    elif command == "/stop" or command == "/end" or command == "اسكت" or command == "انهاء" or command == "ايقاف":
        try:
         await call.leave_group_call(chat_id)
        except:
         pass
        await remove_active(bot_username, chat_id)
        await message.reply_text(f"**≭︰تم انهاء التشغيل**")
    elif command == "تكرار" or command == "كررها" or command == "/loop":
            if len(message.text) == 1:
               return await message.reply_text("**≭︰قم بتحديد عدد مرات التكرار**")
            x = message.text.split(None, 1)[1]
            i = x
            if i in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
              x = i
              xx = f"{x} مره"
            elif x == "مره":
              x = 1
              xx = "مره واحده"
            elif x == "مرتين":
              x = 2
              xx = "مرتين"
            else:
              return await message.reply_text("**≭︰استخدام خطا**\n**≭︰طريقه الاستخدام ↫❲ تكرار 4 ❳**")
            chat = f"{bot_username}{chat_id}"
            check = db.get(chat)
            file_path = check[0]["file_path"]
            title = check[0]["title"]
            duration = check[0]["dur"]
            user_id = check[0]["user_id"]
            chat_id = check[0]["chat_id"]
            vid = check[0]["vid"]
            link = check[0]["link"]
            videoid = check[0]["videoid"]
            for i in range(x):
                file_path = file_path if file_path else None
                await add(chat_id, bot_username, file_path, link, title, duration, videoid, vid, user_id)
            await message.reply_text(f"**≭︰تم تحديد التكرار {xx}**")
    elif command == "/skip" or command == "تخطي":
       chat = f"{bot_username}{chat_id}"
       check = db.get(chat)
       popped = check.pop(0)
       if not check:
         await call.leave_group_call(chat_id)
         await remove_active(bot_username, chat_id)
         return await message.reply_text("**≭︰لا يوجد شئ في قائمه التشغيل**")
       file = check[0]["file_path"]
       title = check[0]["title"]
       dur = check[0]["dur"]
       video = check[0]["vid"]
       videoid = check[0]["videoid"]
       user_id = check[0]["user_id"]
       link = check[0]["link"]
       audio_stream_quality = MediumQualityAudio()
       video_stream_quality = MediumQualityVideo()
       if file:
         file_path = file
       else:     
         try:
            file_path = await download(bot_username, link, video)
         except:
            return client.send_message(chat_id, "**≭︰حدثت مشكله اثناء تشغيل المقطع التالي**")
       stream = (AudioVideoPiped(file_path, audio_parameters=audio_stream_quality, video_parameters=video_stream_quality) if video else AudioPiped(file_path, audio_parameters=audio_stream_quality))
       try:
           await call.change_stream(chat_id, stream)
       except Exception:
            return await client.send_message(chat_id, "**≭︰حدثت مشكله اثناء تشغيل المقطع التالي**")
       userx = await client.get_users(user_id)
       if videoid:
         if userx.photo:
            photo_id = userx.photo.big_file_id
         else:
            Anwar = await client.get_chat("S_1_02")
            photo_id = Anwar.photo.big_file_id
         photo = await client.download_media(photo_id)
         img = await gen_thumb(videoid, photo)
       else:
         img = PHOTO
       requester = userx.mention       
       gr = await get_group(bot_username)
       ch = await get_channel(bot_username)
       button = [
           [
           InlineKeyboardButton(text=f"{title}",url=f"{ch}")
           ],[
           InlineKeyboardButton(text="❲ ايقاف ⏺ ❳", callback_data=f"stop")
           ],[
           InlineKeyboardButton(text="❲ ايقاف مؤقت ▶️ ❳", callback_data=f"pause"),
           InlineKeyboardButton(text="❲ استئناف ⏸ ❳", callback_data=f"resume")
           ],[
           InlineKeyboardButton(text="❲ تخطي ⏯ ❳", callback_data=f"skip")
           ],[
           InlineKeyboardButton(text="❲ Channel Bot ❳", url=f"{ch}")
           ]]
       await message.reply_photo(photo=img, caption=f"**≭︰تم التخطي الى التالي **\n\n**≭︰مدة الاغنيه** ↫❲ {dur} ❳\n**≭︰طلبت من** ↫❲ {requester} ❳", reply_markup=InlineKeyboardMarkup(button)) 
       os.system('rm -rf ./downloads/*')
    else:
      await message.reply_text("**≭︰استخدام خطا  .. **")
  except:
    pass
