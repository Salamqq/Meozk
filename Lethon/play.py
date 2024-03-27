from pyrogram import Client, filters
from youtubesearchpython.__future__ import VideosSearch 
import os
import aiohttp
import requests
import random 
import asyncio
import yt_dlp 
from datetime import datetime, timedelta
from youtube_search import YoutubeSearch
import pytgcalls
from pytgcalls.types.input_stream.quality import (HighQualityAudio,
                                                  HighQualityVideo,
                                                  LowQualityAudio,
                                                  LowQualityVideo,
                                                  MediumQualityAudio,
                                                  MediumQualityVideo)
from typing import Union
from pyrogram import Client, filters 
from pyrogram import Client as client
from pyrogram.errors import (ChatAdminRequired,
                             UserAlreadyParticipant,
                             UserNotParticipant)
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType, ChatMemberStatus
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.exceptions import (AlreadyJoinedError,
                                  NoActiveGroupCall,
                                  TelegramServerError)
from pytgcalls.types import (JoinedGroupCallParticipant,
                             LeftGroupCallParticipant, Update)
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.stream import StreamAudioEnded
from config import API_ID, API_HASH, MONGO_DB_URL, PHOTO, OWNER, OWNER_NAME, LOGS, GROUP, CHANNEL
from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_
from pymongo import MongoClient
from bot import bot as man
from Faeder.info import (db, add, is_served_call, add_active_video_chat, add_served_call, add_active_chat, gen_thumb, download, remove_active, joinch)
from Faeder.Data import (get_logger, get_userbot, get_call, get_logger_mode, get_group, get_channel)
import asyncio 
             
mongodb = _mongo_client_(MONGO_DB_URL)
pymongodb = MongoClient(MONGO_DB_URL)
Bots = pymongodb.Bots

async def join_assistant(client, chat_id, message_id, userbot, file_path):
        join = None
        try:
            try:
                user = userbot.me
                user_id = user.id
                get = await client.get_chat_member(chat_id, user_id)
            except ChatAdminRequired:
                await client.send_message(chat_id, f"**≭︰ارفع البوت ادمن اولا**", reply_to_message_id=message_id)
            if get.status == ChatMemberStatus.BANNED:
                await client.send_message(chat_id, f"≭︰الغي الحظر عن المساعد لتتمكن من التشغيل\n≭︰الحساب المساعد ↫ ❲ @{user.username} ❳", reply_to_message_id=message_id)
            else:
              join = True
        except UserNotParticipant:
            chat = await client.get_chat(chat_id)
            if chat.username:
                try:
                    await userbot.join_chat(chat.username)
                    join = True
                except UserAlreadyParticipant:
                    join = True
                except Exception:
                 try:
                  invitelink = (await client.export_chat_invite_link(chat_id))
                  if invitelink.startswith("https://t.me/+"):
                        invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
                  await asyncio.sleep(3)
                  await userbot.join_chat(invitelink)
                  join = True
                 except ChatAdminRequired:
                    return await client.send_message(chat_id, f"**≭︰اعطي البوت صلاحيه دعوه مستخدمين عبر الرابط**", reply_to_message_id=message_id)
                 except Exception as e:
                   await client.send_message(chat_id, f"**≭︰حدثت مشكله جرب مره اخرى او تواصل مع المطور**", reply_to_message_id=message_id)
            else:
                try:
                    try:
                       invitelink = chat.invite_link
                       if invitelink is None:
                          invitelink = (await client.export_chat_invite_link(chat_id))
                    except Exception:
                        try:
                          invitelink = (await client.export_chat_invite_link(chat_id))
                        except ChatAdminRequired:
                          await client.send_message(chat_id, f"**≭︰اعطي البوت صلاحيه دعوه مستخدمين عبر الرابط**", reply_to_message_id=message_id)
                        except Exception as e:
                          await client.send_message(chat_id, f"**≭︰حدثت مشكله جرب مره اخرى او تواصل مع المطور**", reply_to_message_id=message_id)
                    m = await client.send_message(chat_id, "**≭︰جاري تفعيل البوت**")
                    if invitelink.startswith("https://t.me/+"):
                        invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
                    await userbot.join_chat(invitelink)
                    join = True
                    await m.edit(f"≭︰انضم الحساب المساعد\n≭︰بدء تشغيل الموسيقى \n≭︰الحساب المساعد ↫❲[ {user.mention} ]❳")
                except UserAlreadyParticipant:
                    join = True
                except Exception as e:
                    await client.send_message(chat_id, f"**≭︰حدثت مشكله جرب مره اخرى او تواصل مع المطور**", reply_to_message_id=message_id)
        return join        

async def join_call(
        client,
        message_id,
        chat_id,
        bot_username,
        file_path,
        link,
        vid: Union[bool, str] = None):
        userbot = await get_userbot(bot_username)
        Done = None
        try:
          call = await get_call(bot_username)
        except:
          return Done
        file_path = file_path
        audio_stream_quality = MediumQualityAudio()
        video_stream_quality = MediumQualityVideo()
        stream = (AudioVideoPiped(file_path, audio_parameters=audio_stream_quality, video_parameters=video_stream_quality) 
        if vid else AudioPiped(file_path, audio_parameters=audio_stream_quality))
        try:
            await call.join_group_call(chat_id, stream, stream_type=StreamType().pulse_stream)
            Done = True
        except NoActiveGroupCall:
                 h = await join_assistant(client, chat_id, message_id, userbot, file_path)
                 if h:
                  try:
                   await call.join_group_call(chat_id, stream, stream_type=StreamType().pulse_stream)
                   Done = True
                  except Exception:
                      await client.send_message(chat_id, "**≭︰قم ببدأ مكالمه اولا**", reply_to_message_id=message_id)
        except AlreadyJoinedError:
             await client.send_message(chat_id, "**≭︰اغلق الاتصال وقم بانشاء مكالمه جديده**", reply_to_message_id=message_id)
        except TelegramServerError:
             await client.send_message(chat_id, "**≭︰اغلق الاتصال وقم بانشاء مكالمه جديده**", reply_to_message_id=message_id)
        except Exception as a:
            print(a)
            return Done 
        return Done

def seconds_to_min(seconds):
    if seconds is not None:
        seconds = int(seconds)
        d, h, m, s = (
            seconds // (3600 * 24),
            seconds // 3600 % 24,
            seconds % 3600 // 60,
            seconds % 3600 % 60,
        )
        if d > 0:
            return "{:02d}:{:02d}:{:02d}:{:02d}".format(d, h, m, s)
        elif h > 0:
            return "{:02d}:{:02d}:{:02d}".format(h, m, s)
        elif m > 0:
            return "{:02d}:{:02d}".format(m, s)
        elif s > 0:
            return "00:{:02d}".format(s)
    return "-"


async def logs(bot_username, client, message):
  try:
   if await get_logger_mode(bot_username) == "OFF":
     return
   logger = await get_logger(bot_username)
   log = LOGS
   if message.chat.type == ChatType.CHANNEL:
     chat = f"[{message.chat.title}](t.me/{message.chat.username})" if message.chat.username else message.chat.title
     name = f"{message.author_signature}" if message.author_signature else chat
     text = f"**≭︰بدأ تشغيل اغنيه ↯.\n\n≭︰اسم الكروب ↫ ❲ {chat} ❳\n≭︰ايدي الكروب ↫ ❲ {message.chat.id} ❳\n≭︰اسم المشغل : ↫❲ {name} ❳\n\n≭︰امر التشغيل ↫ ❲ {message.text} ❳**"
   else:
     chat = f"[{message.chat.title}](t.me/{message.chat.username})" if message.chat.username else message.chat.title
     user = f"≭︰معرف المشغل ↫ ❲ @{message.from_user.username} ❳" if message.from_user.username else f"≭︰ايدي المشغل ↫ ❲ {message.from_user.id} ❳"
     text = f"**≭︰بدأ تشغيل اغنيه **\n\n**≭︰اسم الكروب ↫ ❲ {chat} ❳**\n**≭︰ايدي الكروب ↫ ❲ {message.chat.id} ❳**\n**≭︰اسم المشغل ↫ ❲ {message.from_user.mention} ❳**\n**{user}**\n\n**≭︰امر التشغيل ↫ ❲ {message.text} ❳**"
   await client.send_message(logger, text=text, disable_web_page_preview=True)
   return await man.send_message(log, text=f"[ @{bot_username} ]\n{text}", disable_web_page_preview=True)
  except:
    pass


@Client.on_message(filters.command(["عشوائي", "تشغيل عشوائي"], ""))
async def aii(client: Client, message):
   if await joinch(message):
            return
   try:
    chat_id = message.chat.id
    bot_username = client.me.username
    rep = await message.reply_text("**≭︰انتظر جاري الاختيار العشوائي**")
    try:
          call = await get_call(bot_username)
    except:
          await remove_active(bot_username, chat_id)
    try:
       await call.get_call(message.chat.id)
    except pytgcalls.exceptions.GroupCallNotFound: 
       await remove_active(bot_username, chat_id)
    message_id = message.id 
    user = await get_userbot(bot_username)
    req = message.from_user.mention if message.from_user else message.chat.title
    raw_list = []
    async for msg in user.get_chat_history("FaederMUSIC"):
        if msg.audio:
          raw_list.append(msg)
    x = random.choice(raw_list)
    file_path = await x.download()
    file_name = x.audio.title
    title = file_name
    dur = x.audio.duration
    duration = seconds_to_min(dur)
    photo = PHOTO
    vid = True if x.video else None
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else "S_1_02"
    videoid = None
    link = None
    await add(message.chat.id, bot_username, file_path, link, title, duration, videoid, vid, user_id)
    if not await is_served_call(client, message.chat.id): 
      await add_active_chat(chat_id)
      await add_served_call(client, chat_id)
      if vid:
        await add_active_video_chat(chat_id)
      link = None
      c = await join_call(client, message_id, chat_id, bot_username, file_path, link, vid)
      if not c:
            await remove_active(bot_username, chat_id)
            return await rep.delete()
    await rep.delete()
    gr = await get_group(bot_username) 
    ch = await get_channel(bot_username)
    
    button = [ 
       [InlineKeyboardButton(text=f"{title}",url=f"{ch}")
       ],[
       InlineKeyboardButton(text="❲ استئناف ⏸ ❳", callback_data=f"resume"),
       InlineKeyboardButton(text="❲ ايقاف مؤقت ▶️ ❳", callback_data=f"pause")
       ],[
       InlineKeyboardButton(text="❲ ايقاف ⏺ ❳", callback_data=f"stop")
       ],[
       InlineKeyboardButton(text="❲ Channel Bot ❳", url=f"{ch}")
       
       ]] 
    await message.reply_photo(photo=photo, caption=f"**≭︰بدأ التشغيل العشوائي 🎶 **\n\n**≭︰مده الاغنيه ↫ ❲ {duration} ❳**\n**≭︰طلبت من ↫ ❲ {req} ❳**", reply_markup=InlineKeyboardMarkup(button))
    await logs(bot_username, client, message)
    await asyncio.sleep(4)
    os.system('rm -rf ./downloads/*')
   except Exception as es:
    pass

@Client.on_message(filters.command(["/play", "play", "/vplay", "شغل", "تشغيل", "فيد", "فيديو"], ""))
async def play(client: Client, message):
  if await joinch(message):
            return
  Faeder = message
  bot_username = client.me.username
  chat_id = message.chat.id
  user_id = message.from_user.id if message.from_user else "S_1_02"
  message_id = message.id 
  gr = await get_group(bot_username)
  ch = await get_channel(bot_username)

  if message.chat.type == ChatType.PRIVATE:
       return await message.reply_text("**≭︰لا يمكن تشغيلي هنا اضفني الى مجموعه**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"اضف البوت لمجموعتك ", url=f"https://t.me/{bot_username}?startgroup=True")]]))
  if message.sender_chat:
     if not message.chat.type == ChatType.CHANNEL:
      return await message.reply_text("**≭︰يمكنك التشغيل ب الحساب الشخصي **")
  if not len(message.command) == 1:
    rep = await message.reply_text("**≭︰جاري التشغيل ... انتظر قليلا 🎶**")
  try:
          call = await get_call(bot_username)
  except:
          await remove_active(bot_username, chat_id)
  try:
       await call.get_call(message.chat.id)
  except pytgcalls.exceptions.GroupCallNotFound:
       await remove_active(bot_username, chat_id)
  if not message.reply_to_message:
     if len(message.command) == 1:
      if message.chat.type == ChatType.CHANNEL:
        return await message.reply_text("**≭︰ارسل اسم المقطع لتشغيله**")
      try:
       name = await client.ask(message.chat.id, text="**≭︰ارسل تشغيل مع اسم المقطع او قم بالرد على المقطع**", reply_to_message_id=message.id, filters=filters.user(message.from_user.id), timeout=7)
       name = name.text
       rep = await message.reply_text("**≭︰جاري التشغيل ... انتظر قليلا 🎶**")
      except:
       return
     else:
       name = message.text.split(None, 1)[1]
     try:
      results = VideosSearch(name, limit=1)
     except Exception:
      return await rep.edit("**≭︰لا يوجد نتائج**")
     for result in (await results.next())["result"]:
         title = result["title"]
         duration = result["duration"]
         videoid = result["id"]
         yturl = result["link"]
         thumbnail = result["thumbnails"][0]["url"].split("?")[0]
     if "v" in message.command[0] or "ف" in message.command[0]:
       vid = True
     else:
       vid = None
     await rep.edit("**≭︰جاري التشغيل .... انتظر قليلا 🎶**")
     results = YoutubeSearch(name, max_results=5).to_dict()
     link = f"https://youtube.com{results[0]['url_suffix']}"
     if await is_served_call(client, message.chat.id):
         chat_id = message.chat.id
         title = title.title()
         file_path = None
         await add(message.chat.id, bot_username, file_path, link, title, duration, videoid, vid, user_id)
         chat = f"{bot_username}{chat_id}"
         position = len(db.get(chat)) - 1
         chatname = f"[{message.chat.title}](https://t.me/{message.chat.username})" if message.chat.username else f"{message.chat.title}"
         chatname = f"{message.author_signature}" if message.author_signature else chatname
         requester = chatname if Faeder.views else f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
         if message.from_user:
          if message.from_user.photo:
           photo_id = message.from_user.photo.big_file_id
           photo = await client.download_media(photo_id)
          elif message.chat.photo:
           photo_id = message.chat.photo.big_file_id
           photo = await client.download_media(photo_id)
          else:
           Anwar = await client.get_chat("S_1_02")
           Anwarphoto = Anwar.photo.big_file_id
         elif message.chat.photo:
          photo_id = message.chat.photo.big_file_id
          photo = await client.download_media(photo_id)
         else:
          Anwar = await client.get_chat("S_1_02")
          Anwarphoto = Anwar.photo.big_file_id
          photo = await client.download_media(Anwarphoto)
         photo = await gen_thumb(videoid, photo)
         button = [
           [InlineKeyboardButton(text=f"{title[:18]}",url=f"{ch}")
           ],[
           InlineKeyboardButton(text="❲ ايقاف ⏺ ❳", callback_data=f"stop")
           ],[
           InlineKeyboardButton(text="❲ ايقاف مؤقت ▶️ ❳", callback_data=f"pause"),
           InlineKeyboardButton(text="❲ استئناف ⏸ ❳", callback_data=f"resume")
           ],[
           InlineKeyboardButton(text="❲ تخطي ⏯ ❳", callback_data=f"skip")
           ],[ 
           InlineKeyboardButton(text="❲ Channel Bot ❳", url=f"{ch}")
           ]
           ]
         await message.reply_photo(photo=photo, caption=f"**≭︰تم اضافتها الى قائمه التشغيل ↫ {position}**\n\n**≭︰مدة الاغنيه ↫ ❲ {duration} ❳**\n**≭︰طلبت من ↫ ❲ {requester} ❳**", reply_markup=InlineKeyboardMarkup(button))
         await logs(bot_username, client, message)
     else:
         chat_id = message.chat.id
         title = title.title()
         await add_active_chat(chat_id)
         await add_served_call(client, chat_id)
         if vid:
           await add_active_video_chat(chat_id)
         file_path = await download(bot_username, link, vid)
         await add(message.chat.id, bot_username, file_path, link, title, duration, videoid, vid, user_id)
         c = await join_call(client, message_id, chat_id, bot_username, file_path, link, vid)
         if not c:
            await remove_active(bot_username, chat_id)
            return await rep.delete()
         chatname = f"[{message.chat.title}](https://t.me/{message.chat.username})" if message.chat.username else f"{message.chat.title}"
         chatname = f"{message.author_signature}" if message.author_signature else chatname
         requester = chatname if Faeder.views else f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
         if message.from_user:
          if message.from_user.photo:
           photo_id = message.from_user.photo.big_file_id
           photo = await client.download_media(photo_id)
          elif message.chat.photo:
           photo_id = message.chat.photo.big_file_id
           photo = await client.download_media(photo_id)
          else:
           Anwar = await client.get_chat("S_1_02")
           Anwarphoto = Anwar.photo.big_file_id
         elif message.chat.photo:
          photo_id = message.chat.photo.big_file_id
          photo = await client.download_media(photo_id)
         else: 
          Anwar = await client.get_chat("S_1_02")
          Anwarphoto = Anwar.photo.big_file_id
          photo = await client.download_media(Anwarphoto)
         photo = await gen_thumb(videoid, photo)
         button = [
         
           [InlineKeyboardButton(text=f"{title[:18]}", url=f"{ch}")
           ],[ 
           InlineKeyboardButton(text="❲ ايقاف ⏺ ❳", callback_data=f"stop")
           ],[
           InlineKeyboardButton(text="❲ ايقاف مؤقت ▶️ ❳", callback_data=f"pause"),
           InlineKeyboardButton(text="❲ استئناف ⏸ ❳", callback_data=f"resume")
           ],[
           InlineKeyboardButton(text="❲ تخطي ⏯ ❳", callback_data=f"skip")
           ],[ 
           InlineKeyboardButton(text="❲ Channel Bot ❳", url=f"{ch}")
           ]
           ]
         await message.reply_photo(photo=photo, caption=f"**≭︰بدأ التشغيل 🎶**\n\n**≭︰مدة الاغنيه ↫ ❲ {duration} ❳**\n**≭︰طلبت من ↫ ❲ {requester} ❳**", reply_markup=InlineKeyboardMarkup(button))
         await logs(bot_username, client, message)
     await rep.delete()
  else:
    if not message.reply_to_message.media:
        return
    rep = await message.reply_text("**≭︰جاري تشغيل المقطع 🎶**")
    photo = "https://telegra.ph/file/8ab98f3b6ee6f2d7caf4b.jpg"
    if message.reply_to_message.video or message.reply_to_message.document:
        vid = True
    else:
        vid = None
    file_path = await message.reply_to_message.download()
    if message.reply_to_message.audio:
        file_name = message.reply_to_message.audio
    elif message.reply_to_message.voice:
        file_name = message.reply_to_message.voice
    elif message.reply_to_message.video:
        file_name = message.reply_to_message.video
    else:
        file_name = message.reply_to_message.document
    title = file_name.file_name
    duration = seconds_to_min(file_name.duration)
    link = None
    if await is_served_call(client, message.chat.id):
        chat_id = message.chat.id
        videoid = None
        await add(message.chat.id, bot_username, file_path, link, title, duration, videoid, vid, user_id)
        chat = f"{bot_username}{chat_id}"
        position = len(db.get(chat)) - 1
        chatname = f"[{message.chat.title}](https://t.me/{message.chat.username})" if message.chat.username else f"{message.chat.title}"
        chatname = f"{message.author_signature}" if message.author_signature else chatname
        requester = chatname if Faeder.views else f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        button = [
            [InlineKeyboardButton(text=f"{title[:18]}", url=f"{ch}")],
            [InlineKeyboardButton(text="❲ ايقاف ⏺ ❳", callback_data=f"stop")],
            [InlineKeyboardButton(text="❲ ايقاف مؤقت ▶️ ❳", callback_data=f"pause"),
             InlineKeyboardButton(text="❲ استئناف ⏸ ❳", callback_data=f"resume")],
            [InlineKeyboardButton(text="❲ تخطي ⏯ ❳", callback_data=f"skip")],
            [InlineKeyboardButton(text="❲ Channel Bot ❳", url=f"{ch}")
      ] 
        ]
        await message.reply_photo(photo=photo, caption=f"**≭︰تم اضافتها الى قائمه التشغيل ↫ {position}**\n\n≭︰مدة الاغنيه ↫ ❲ {duration} ❳**\n**≭︰طلبت من ↫ ❲ {requester} ❳**",
                                  reply_markup=InlineKeyboardMarkup(button))
        await logs(bot_username, client, message)
    else:
        chat_id = message.chat.id
        videoid = None
        await add_active_chat(chat_id)
        await add_served_call(client, chat_id)
        if vid:
            await add_active_video_chat(chat_id)
        await add(message.chat.id, bot_username, file_path, link, title, duration, videoid, vid, user_id)
        c = await join_call(client, message_id, chat_id, bot_username, file_path, link, vid)
        if not c:
            await remove_active(bot_username, chat_id)
            return await rep.delete()
        chatname = f"[{message.chat.title}](https://t.me/{message.chat.username})" if message.chat.username else f"{message.chat.title}"
        chatname = f"{message.author_signature}" if message.author_signature else chatname
        requester = chatname if Faeder.views else f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        button = [ 
            [InlineKeyboardButton(text=f"{title}", url=f"{ch}")],
            [InlineKeyboardButton(text="❲ ايقاف ⏺ ❳", callback_data=f"stop")],
            [InlineKeyboardButton(text="❲ ايقاف مؤقت ▶️ ❳", callback_data=f"pause"),
             InlineKeyboardButton(text="❲ استئناف ⏸ ❳", callback_data=f"resume")],
            [InlineKeyboardButton(text="❲ تخطي ⏯ ❳", callback_data=f"skip")],
            [InlineKeyboardButton(text="❲ Channel Bot ❳", url=f"{ch}")
          ]

        ]
        await message.reply_photo(photo=photo, caption=f"**≭︰بدأ التشغيل 🎶 𖦤 .**\n\n**≭︰مدة الاغنيه ↫ ❲ {duration} ❳**\n**≭︰طلبت من ↫❲ {requester} ❳**",
                                  reply_markup=InlineKeyboardMarkup(button))
        await logs(bot_username, client, message)
    os.system('rm -rf ./downloads/*')
    await rep.delete()
