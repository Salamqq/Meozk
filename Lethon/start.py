import random
from pyrogram import Client, filters
from pyrogram import Client as app
from time import time
from config import OWNER, OWNER_NAME, VIDEO
from Faeder.info import (is_served_chat, add_served_chat, is_served_user, add_served_user, get_served_chats, get_served_users, del_served_chat, joinch)
from Faeder.Data import (get_dev, get_bot_name, set_bot_name, get_logger, get_group, get_channel, get_dev_name, get_groupsr, get_channelsr, get_userbot)
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, Message, User, ChatPrivileges
from pyrogram import enums
import os
import re
import textwrap
import aiofiles 
import aiohttp
from PIL import (Image, ImageDraw, ImageEnhance, ImageFilter,
                 ImageFont, ImageOps)
from youtubesearchpython.__future__ import VideosSearch

Anwar = "https://telegra.ph/file/a8a5bedfaaf0d19194e4a.jpg"


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


async def gen_bot(client, username, photo):
        if os.path.isfile(f"{username}.png"):
           return f"{username}.png"
        users = len(await get_served_users(client))
        chats = len(await get_served_chats(client))
        url = f"https://www.youtube.com/watch?v=gKA2XFkJZhI"
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"thumb{username}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()

        youtube = Image.open(f"{photo}")
        Faederv = Image.open(f"{photo}")
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.convert("RGBA")
        background = image2.filter(filter=ImageFilter.BoxBlur(5))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.6)
        Xcenter = Faederv.width / 2
        Ycenter = Faederv.height / 2
        x1 = Xcenter - 250
        y1 = Ycenter - 250
        x2 = Xcenter + 250
        y2 = Ycenter + 250
        logo = Faederv.crop((x1, y1, x2, y2))
        logo.thumbnail((520, 520), Image.ANTIALIAS)
        logo = ImageOps.expand(logo, border=15, fill="white")
        background.paste(logo, (50, 100))
        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype("font2.ttf", 40)
        font2 = ImageFont.truetype("font2.ttf", 70)
        arial = ImageFont.truetype("font2.ttf", 30)
        name_font = ImageFont.truetype("font.ttf", 30)
        draw.text(
            (600, 150),
            "Music Cyclone BoT",
            fill="white",
            stroke_width=2,
            stroke_fill="white",
            font=font2,
        )
        draw.text(
            (600, 340),
            f"Dev : Salam",
            fill="white",
            stroke_width=1,
            stroke_fill="white",
            font=font,
        )
        draw.text(
            (600, 280),
            f"Playing Music In Call",
            fill="white",
            stroke_width=1,
            stroke_fill="white",
            font=font,
        )

        draw.text(
            (600, 400),
            f"user : {users}",
            (255, 255, 255),
            font=arial,
        )
        draw.text(
            (600, 450),
            f"chats : {chats}",
            (255, 255, 255),
            font=arial,
        )
        draw.text(
            (600, 500),
            f"Version : 0.2.7",
            (255, 255, 255),
            font=arial,
        )
        draw.text(
            (600, 550),
            f"BoT : t.me\{username}",
            (255, 255, 255),
            font=arial,
        )
        try:
            os.remove(f"thumb{username}.png")
        except:
            pass
        background.save(f"{username}.png")
        return f"{username}.png"

OFFPV = []
 
@Client.on_message(filters.command(["❲ تفعيل التواصل ❳", "❲ تعطيل التواصل ❳"], ""))
async def byyye(client, message):
    user = message.from_user.username
    dev = await get_dev(client.me.username)
    if user in OWNER or message.from_user.id == dev:
        text = message.text
        if text == "❲ تفعيل التواصل ❳":
          if not client.me.username in OFFPV:
             await message.reply_text("**≭︰التواصل مفعل سابقا**")
          try:
            OFFPV.remove(client.me.username)
            await message.reply_text("≭︰تم تفعيل التواصل")
            return
          except:
             pass
        if text == "❲ تعطيل التواصل ❳":
          if client.me.username in OFFPV:
             await message.reply_text("**≭︰التواصل معطل سابقا**")
          try:
            OFFPV.append(client.me.username)
            await message.reply_text("≭︰تم تعطيل التواصل")
            return
          except:
             pass


@Client.on_message(filters.private)
async def botoot(client: Client, message: Message):
 if not client.me.username in OFFPV:
  if await joinch(message):
            return
 
  bot_username = client.me.username
  user_id = message.chat.id
  if not await is_served_user(client, user_id):
     await add_served_user(client, user_id)
  dev = await get_dev(bot_username)
  if message.from_user.id == dev or message.chat.username in OWNER or message.from_user.id == client.me.id:
    if message.reply_to_message:
     u = message.reply_to_message.forward_from
     try:
       await client.send_message(u.id, text=message.text)
       await message.reply_text(f"**≭︰تم ارسال رسالتك الى ↫❲ {u.mention} ❳**")
     except Exception:
         pass
  else:
   try:
    if message.text != "/start":
     await client.forward_messages(dev, message.chat.id, message.id)
     #await client.forward_messages(OWNER[0], message.chat.id, message.id)
   except Exception as e:
     pass
 message.continue_propagation()

@Client.on_message(filters.new_chat_members)
async def welcome(client: Client, message):
   try:
    bot = client.me
    bot_username = bot.username
    if message.new_chat_members[0].username == "S_1_02" or message.new_chat_members[0].username == "AAA2F":
      try:
         chat_id = message.chat.id
         user_id = message.new_chat_members[0].id
         await client.promote_chat_member(chat_id, user_id, privileges=enums.ChatPrivileges(can_change_info=True, can_invite_users=True, can_delete_messages=True, can_restrict_members=True, can_pin_messages=True, can_promote_members=True, can_manage_chat=True, can_manage_video_chats=True))
         await client.set_administrator_title(chat_id, user_id, "❲ الاعصار ❳")
      except:
        pass 
      return await message.reply_text(f"**≭︰مبرمج السورس انضم للمجموعه ❲ [.](https://t.me/S_1_02) ❳**")
    dev = await get_dev(bot_username)
    if message.new_chat_members[0].id == dev:
      try:
         await client.promote_chat_member(message.chat.id, message.new_chat_members[0].id, privileges=enums.ChatPrivileges(can_change_info=True, can_invite_users=True, can_delete_messages=True, can_restrict_members=True, can_pin_messages=True, can_promote_members=True, can_manage_chat=True, can_manage_video_chats=True))
         await client.set_administrator_title(message.chat.id, message.new_chat_members[0].id, "❲ مطور البوت ❳")
      except:
        pass
      return await message.reply_text(f"**≭︰مطور البوت انضم للمجموعه **❲ {message.new_chat_members[0].mention} ❳**")
    if message.new_chat_members[0].id == bot.id:
      photo = bot.photo.big_file_id
      photo = await client.download_media(photo)
      chat_id = message.chat.id
      nn = await get_dev_name(client, bot_username)
      ch = await get_channel(bot_username)
      gr = await get_group(bot_username)
      button = [
    [InlineKeyboardButton("❲ لشراء بوت ❳", url="https://t.me/S_1_02")],
    [
        InlineKeyboardButton(text="❲ قناة البوت ❳", url=f"{ch}"),
        InlineKeyboardButton(text="❲ قناة التحديثات ❳", url=f"{gr}")
    ],
    [InlineKeyboardButton(text=f"❲ {nn} ❳", user_id=f"{dev}")]
]

      await message.reply_photo(photo=photo, caption=f"**≭︰اهلا بك في بوت تشغيل الاغاني \n≭︰تم تفعيل البوت في المجموعه \n≭︰يمكنك تشغيل الموسيقى الان 🎶**", reply_markup=InlineKeyboardMarkup(button))
      logger = await get_dev(bot_username)
      await add_served_chat(client, chat_id)
      chats = len(await get_served_chats(client))
      return await client.send_message(logger, f"≭︰تم تفعيل مجموعه جديده ↯. \n≭︰اسم المجموعه ↫ ❲ [{message.chat.title}](https://t.me/{message.chat.username}) ❳\n≭︰بواسطه ↫ ❲ {message.from_user.mention} ❳ \n≭︰عدد المجموعات ↫ ❲ {chats} ❳", disable_web_page_preview=True)
   except:
      pass
       
@Client.on_message(filters.left_chat_member)
async def bot_kicked(client: Client, message):
    bot = client.me
    bot_username = bot.username
    if message.left_chat_member.id == bot.id:
         logger = await get_dev(bot_username)
         chat_id = message.chat.id
         await client.send_message(logger, f"**≭︰تم طرد البوت من مجموعه ↯.**\n**\n≭︰اسم المجموعه ↫ ❲ {message.chat.title} ❳**\n**≭︰بواسطه ↫** ❲ {message.from_user.mention} ❳")
         return await del_served_chat(client, chat_id)
         
@Client.on_message(filters.command(["/start", "❲ القائمه الرئيسيه ❳"], ""))
async def start(client: Client, message):
 print("is start ...")
 if not message.chat.type == enums.ChatType.PRIVATE:
    if await joinch(message):
            return
 bot_username = client.me.username
 dev = await get_dev(bot_username) 
 nn = await get_dev_name(client, bot_username)
 if message.chat.id == dev or message.chat.username in OWNER:
   kep = ReplyKeyboardMarkup([["❲ اعدادات الحساب المساعد ❳", "❲ تعيين اسم البوت ❳"],["❲ تعطيل الاشتراك الإجباري ❳", "❲ تفعيل الاشتراك الإجباري ❳"],["❲ المكالمات النشطه ❳"],["❲ تعيين قناة البوت ❳", "❲ تعيين مجموعه البوت ❳"],["❲ الكروبات ❳", "❲ المشتركين ❳"],["❲ الاحصائيات ❳"],["❲ تعطيل التواصل ❳", "❲ تفعيل التواصل ❳"],["❲ تعطيل الاشعارات ❳", "❲ تفعيل الاشعارات ❳"],["❲ حذف downloads ❳", "❲ تغيير مكان الاشعارات ❳"],["❲ اوامر الاذاعه ❳"],["❲ السورس ❳"]], resize_keyboard=True)
   await message.reply_text("**≭︰اهلا بك عزيزي المطور**\n**≭︰اليك كيبورد اوامر البوت**", reply_markup=kep)
 else: 
    bot = await client.get_me()
    username = client.me.username
    ch = await get_channel(bot.username)
    dev = await get_dev(bot.username)
    devname = await get_dev_name(client, bot.username)
    sddd=f"≭︰مرحبا ↫ ❲ {message.from_user.mention} ❳ \n\n≭︰انا بوت لتشغيل الاغاني في المكالمات\n≭︰يمكنني التشغيل في مجموعه او قناة\n≭︰فقط اضفني وارفعني مشرف  "
    button =   [
                [ 
                    InlineKeyboardButton("❲ لشراء بوت ❳", url=f"https://t.me/S_1_02")
                ],
                [ 
                    InlineKeyboardButton("❲ اوامر التشغيل ❳", callback_data="bcmds"),
                    InlineKeyboardButton("❲ اوامر التفعيل ❳", callback_data="bhowtouse"),
                ],
                [
                    InlineKeyboardButton(
                        "❲ قناة السورس ❳", url=f"{ch}"
                    ),
                    InlineKeyboardButton(
                        f"{devname}", user_id=f"{dev}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "❲ اضفني لمجموعتك ❳",
                        url=f"https://t.me/{bot.username}?startgroup=true",
                    )
                ],
            ]    
    if not bot.photo:
       return await client.send_message(message.chat.id,sddd, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(button))
    photo = bot.photo.big_file_id
    photo = await client.download_media(photo)
    photo = await gen_bot(client, username, photo)
    return await client.send_photo(message.chat.id, photo=photo, caption=sddd, reply_to_message_id=message.id,reply_markup=InlineKeyboardMarkup(button))
  


bot = [
  
  "عيون {} العسليات",
    "موجود حبي كول ؟",
  "موجود بس لتلح",
  "اطلق من يصيح {}",
  "عوفني مشغول بتشغيل الاغاني",
]
  
selections = [
    "انت البوت صيحلي باسمي {}",
   "كافي بوت اسمي {}",
    "عندي اسم تراا",
    "تقبل احد يصيحلك بوت ؟",
    "صيحلي باسمي {} لا نتضارب",
]

tyet = ["اخر افلام شاهدتها", 
"اخر افلام شاهدتها", 
"ما هي وظفتك الحياه", 
"اعز اصدقائك ?", 
"اخر اغنية سمعتها ?", 
"تكلم عن نفسك", 
"اخر كتاب قرآته", 
"روايتك المفضله ?", 
"اخر اكله اكلتها", 
"اخر كتاب قرآته", 
"افضل يوم ف حياتك", 
"حكمتك ف الحياه", 
"لون عيونك", 
"كتابك المفضل", 
"هوايتك المفضله", 
"علاقتك مع اهلك", 
" ما السيء في هذه الحياة ؟ ", 
"أجمل شيء حصل معك خلال هذا الاسبوع ؟ ", 
"سؤال ينرفزك ؟ ", 
" اكثر ممثل تحبه ؟ ", 
"قد تخيلت شي في بالك وصار ؟ ", 
"شيء عندك اهم من الناس ؟ ", 
"تفضّل النقاش الطويل او تحب الاختصار ؟ ", 
"وش أخر شي ضيعته؟ ", 
"كم مره حبيت؟ ", 
" اكثر المتابعين عندك باي برنامج؟", 
" نسبه الندم عندك للي وثقت فيهم ؟", 
"تحب ترتبط بكيرفي ولا فلات؟", 
" جربت شعور احد يحبك بس انت مو قادر تحبه؟", 
" تجامل الناس ولا اللي بقلبك على لسانك؟", 
" عمرك ضحيت باشياء لاجل شخص م يسوى ؟", 
"مغني تلاحظ أن صوته يعجب الجميع إلا أنت؟ ", 
" آخر غلطات عمرك؟ ", 
" مسلسل كرتوني له ذكريات جميلة عندك؟ ", 
" ما أكثر تطبيق تقضي وقتك عليه؟ ", 
" أول شيء يخطر في بالك إذا سمعت كلمة نجوم ؟ ", 
" قدوتك من الأجيال السابقة؟ ", 
" أكثر طبع تهتم بأن يتواجد في شريك/ة حياتك؟ ", 
"أكثر حيوان تخاف منه؟ ", 
" ما هي طريقتك في الحصول على الراحة النفسية؟ ", 
" إيموجي يعبّر عن مزاجك الحالي؟ ", 
" أكثر تغيير ترغب أن تغيّره في نفسك؟ ", 
"أكثر شيء أسعدك اليوم؟ ", 
"ما هو أفضل حافز للشخص؟ ", 
"ما الذي يشغل بالك في الفترة الحالية؟", 
"آخر شيء ندمت عليه؟ ", 
"شاركنا صورة احترافية من تصويرك؟ ", 
"تتابع انمي؟ إذا نعم ما أفضل انمي شاهدته ", 
"يرد عليك متأخر على رسالة مهمة وبكل برود، موقفك؟ ", 
"نصيحه تبدا ب -لا- ؟ ", 
"كتاب أو رواية تقرأها هذه الأيام؟ ", 
"فيلم عالق في ذهنك لا تنساه مِن روعته؟ ", 
"يوم لا يمكنك نسيانه؟ ", 
"شعورك الحالي في جملة؟ ", 
"كلمة لشخص بعيد؟ ", 
"صفة يطلقها عليك الشخص المفضّل؟ ", 
"أغنية عالقة في ذهنك هاليومين؟ ", 
"أكلة مستحيل أن تأكلها؟ ", 
"كيف قضيت نهارك؟ ", 
"تصرُّف ماتتحمله؟ ", 
"موقف غير حياتك؟ ", 
"اكثر مشروب تحبه؟ ", 
"القصيدة اللي تأثر فيك؟ ", 
"متى يصبح الصديق غريب ", 
"وين نلقى السعاده برايك؟ ", 
"تاريخ ميلادك؟ ", 
"قهوه و لا شاي؟ ", 
"من محبّين الليل أو النهار ؟", 
"حيوانك المفضل؟ ", 
"كلمة غريبة ومعناها؟ ", 
"كم تحتاج من وقت لتثق بشخص؟ ", 
"اشياء نفسك تجربها؟ ", 
"يومك ضاع على؟ ", 
"كل شيء يهون الا ؟ ", 
"اسم ماتحبه ؟ ", 
"وقفة إحترام للي إخترع ؟ ", 
"أقدم شيء محتفظ فيه من صغرك؟ ", 
"كلمات ماتستغني عنها بسوالفك؟ ", 
"وش الحب بنظرك؟ ", 
"حب التملك في شخصِيـتك ولا ؟ ", 
"تخطط للمستقبل ولا ؟ ", 
"موقف محرج ماتنساه ؟ ", 
"من طلاسم لهجتكم ؟ ", 
"اعترف باي حاجه ؟ ", 
"عبّر عن مودك بصوره ؟ ",
"اسم دايم ع بالك ؟ ", 
"اشياء تفتخر انك م سويتها ؟ ", 
" لو بكيفي كان ؟ ", 
  "أكثر جملة أثرت بك في حياتك؟ ",
  "إيموجي يوصف مزاجك حاليًا؟ ",
  "أجمل اسم بنت بحرف الباء؟ ",
  "كيف هي أحوال قلبك؟ ",
  "أجمل مدينة؟ ",
  "كيف كان أسبوعك؟ ",
  "شيء تشوفه اكثر من اهلك ؟ ",
  "اخر مره فضفضت؟ ",
  "قد كرهت احد بسبب اسلوبه؟ ",
  "قد حبيت شخص وخذلك؟ ",
  "كم مره حبيت؟ ",
  "اكبر غلطة بعمرك؟ ",
  "نسبة النعاس عندك حاليًا؟ ",
  "شرايكم بمشاهير التيك توك؟ ",
  "ما الحاسة التي تريد إضافتها للحواس الخمسة؟ ",
  "اسم قريب لقلبك؟ ",
  "مشتاق لمطعم كنت تزوره قبل الحظر؟ ",
  "أول شيء يخطر في بالك إذا سمعت كلمة (ابوي يبيك)؟ ",
  "ما أول مشروع تتوقع أن تقوم بإنشائه إذا أصبحت مليونير؟ ",
  "أغنية عالقة في ذهنك هاليومين؟ ",
  "متى اخر مره قريت قرآن؟ ",
  "كم صلاة فاتتك اليوم؟ ",
  "تفضل التيكن او السنقل؟ ",
  "وش أفضل بوت برأيك؟ ",
"كم لك بالتلي؟ ",
"وش الي تفكر فيه الحين؟ ",
"كيف تشوف الجيل ذا؟ ",
"منشن شخص وقوله، تحبني؟ ",
"لو جاء شخص وعترف لك كيف ترده؟ ",
"مر عليك موقف محرج؟ ",
"وين تشوف نفسك بعد سنتين؟ ",
"لو فزعت/ي لصديق/ه وقالك مالك دخل وش بتسوي/ين؟ ",
"وش اجمل لهجة تشوفها؟ ",
"قد سافرت؟ ",
"افضل مسلسل عندك؟ ",
"افضل فلم عندك؟ ",
"مين اكثر يخون البنات/العيال؟ ",
"متى حبيت؟ ",
  "بالعادة متى تنام؟ ",
  "شيء من صغرك ماتغيير فيك؟ ",
  "شيء بسيط قادر يعدل مزاجك بشكل سريع؟ ",
  "تشوف الغيره انانيه او حب؟ ",
"حاجة تشوف نفسك مبدع فيها؟ ",
  "مع او ضد : يسقط جمال المراة بسبب قبح لسانها؟ ",
  "عمرك بكيت على شخص مات في مسلسل ؟ ",
  "‏- هل تعتقد أن هنالك من يراقبك بشغف؟ ",
  "تدوس على قلبك او كرامتك؟ ",
  "اكثر لونين تحبهم مع بعض؟ ",
  "مع او ضد : النوم افضل حل لـ مشاكل الحياة؟ ",
  "سؤال دايم تتهرب من الاجابة عليه؟ ",
  "تحبني ولاتحب الفلوس؟ ",
  "العلاقه السريه دايماً تكون حلوه؟ ",
  "لو أغمضت عينيك الآن فما هو أول شيء ستفكر به؟ ",
"كيف ينطق الطفل اسمك؟ ",
  "ما هي نقاط الضعف في شخصيتك؟ ",
  "اكثر كذبة تقولها؟ ",
  "تيكن ولا اضبطك؟ ",
  "اطول علاقة كنت فيها مع شخص؟ ",
  "قد ندمت على شخص؟ ",
  "وقت فراغك وش تسوي؟ ",
  "عندك أصحاب كثير؟ ولا ينعد بالأصابع؟ ",
  "حاط نغمة خاصة لأي شخص؟ ",
  "وش اسم شهرتك؟ ",
  "أفضل أكلة تحبه لك؟ ",
"عندك شخص تسميه ثالث والدينك؟ ",
  "اذا قالو لك تسافر أي مكان تبيه وتاخذ معك شخص واحد وين بتروح ومين تختار؟ ",
  "أطول مكالمة كم ساعة؟ ",
  "تحب الحياة الإلكترونية ولا الواقعية؟ ",
  "كيف حال قلبك ؟ بخير ولا مكسور؟ ",
  "أطول مدة نمت فيها كم ساعة؟ ",
  "تقدر تسيطر على ضحكتك؟ ",
  "أول حرف من اسم الحب؟ ",
  "تحب تحافظ على الذكريات ولا تمسحه؟ ",
  "اسم اخر شخص زعلك؟ ",
"وش نوع الأفلام اللي تحب تتابعه؟ ",
  "أنت انسان غامض ولا الكل يعرف عنك؟ ",
  "لو الجنسية حسب ملامحك وش بتكون جنسيتك؟ ",
  "عندك أخوان او خوات من الرضاعة؟ ",
  "إختصار تحبه؟ ",
  "إسم شخص وتحس أنه كيف؟ ",
  "وش الإسم اللي دايم تحطه بالبرامج؟ ",
  "وش برجك؟ ",
  "لو يجي عيد ميلادك تتوقع يجيك هدية؟ ",
  "اجمل هدية جاتك وش هو؟ ",
  "الصداقة ولا الحب؟ ",
  "الغيرة الزائدة شك؟ ولا فرط الحب؟ ",
  "قد حبيت شخصين مع بعض؟ وانقفطت؟ ",
  "وش أخر شي ضيعته؟ ",
  "قد ضيعت شي ودورته ولقيته بيدك؟ ",
  "تؤمن بمقولة اللي يبيك مايحتار فيك؟ ",
  "سبب وجوك بالتليجرام؟ ",
  "تراقب شخص حاليا؟ ",
  "عندك معجبين ولا محد درا عنك؟ ",
  "لو نسبة جمالك بتكون بعدد شحن جوالك كم بتكون؟ ",
  "أنت محبوب بين الناس؟ ولاكريه؟ ",
"كم عمرك؟ ",
  "لو يسألونك وش اسم امك تجاوبهم ولا تسفل فيهم؟ ",
  "تؤمن بمقولة الصحبة تغنيك الحب؟ ",
  "وش مشروبك المفضل؟ ",
  "قد جربت الدخان بحياتك؟ وانقفطت ولا؟ ",
  "أفضل وقت للسفر؟ الليل ولا النهار؟ ",
  "انت من النوع اللي تنام بخط السفر؟ ",
  "عندك حس فكاهي ولا نفسية؟ ",
  "تبادل الكراهية بالكراهية؟ ولا تحرجه بالطيب؟ ",
  "أفضل ممارسة بالنسبة لك؟ ",
  "لو قالو لك تتخلى عن شي واحد تحبه بحياتك وش يكون؟ ",
"لو احد تركك وبعد فتره يحاول يرجعك بترجع له ولا خلاص؟ ",
  "برأيك كم العمر المناسب للزواج؟ ",
  "اذا تزوجت بعد كم بتخلف عيال؟ ",
  "فكرت وش تسمي أول اطفالك؟ ",
  "من الناس اللي تحب الهدوء ولا الإزعاج؟ ",
  "الشيلات ولا الأغاني؟ ",
  "عندكم شخص مطوع بالعايلة؟ ",
  "تتقبل النصيحة من اي شخص؟ ",
  "اذا غلطت وعرفت انك غلطان تحب تعترف ولا تجحد؟ ",
  "جربت شعور احد يحبك بس انت مو قادر تحبه؟ ",
  "دايم قوة الصداقة تكون بإيش؟ ",
"أفضل البدايات بالعلاقة بـ وش؟ ",
  "وش مشروبك المفضل؟ او قهوتك المفضلة؟ ",
  "تحب تتسوق عبر الانترنت ولا الواقع؟ ",
  "انت من الناس اللي بعد ماتشتري شي وتروح ترجعه؟ ",
  "أخر مرة بكيت متى؟ وليش؟ ",
  "عندك الشخص اللي يقلب الدنيا عشان زعلك؟ ",
  "أفضل صفة تحبه بنفسك؟ ",
  "كلمة تقولها للوالدين؟ ",
  "أنت من الناس اللي تنتقم وترد الاذى ولا تحتسب الأجر وتسامح؟ ",
  "كم عدد سنينك بالتليجرام؟ ",
  "تحب تعترف ولا تخبي؟ ",
"انت من الناس الكتومة ولا تفضفض؟ ",
  "أنت بعلاقة حب الحين؟ ",
  "عندك اصدقاء غير جنسك؟ ",
  "أغلب وقتك تكون وين؟ ",
  "لو المقصود يقرأ وش بتكتب له؟ ",
  "تحب تعبر بالكتابة ولا بالصوت؟ ",
  "عمرك كلمت فويس احد غير جنسك؟ ",
  "لو خيروك تصير مليونير ولا تتزوج الشخص اللي تحبه؟ ",
  "لو عندك فلوس وش السيارة اللي بتشتريها؟ ",
  "كم أعلى مبلغ جمعته؟ ",
  "اذا شفت احد على غلط تعلمه الصح ولا تخليه بكيفه؟ ",
"قد جربت تبكي فرح؟ وليش؟ ",
"تتوقع إنك بتتزوج اللي تحبه؟ ",
  "ما هو أمنيتك؟ ",
  "وين تشوف نفسك بعد خمس سنوات؟ ",
  "لو خيروك تقدم الزمن ولا ترجعه ورا؟ ",
  "لعبة قضيت وقتك فيه بالحجر المنزلي؟ ",
  "تحب تطق الميانة ولا ثقيل؟ ",
  "باقي معاك للي وعدك ما بيتركك؟ ",
  "اول ماتصحى من النوم مين تكلمه؟ ",
  "عندك الشخص اللي يكتب لك كلام كثير وانت نايم؟ ",
  "قد قابلت شخص تحبه؟ وولد ولا بنت؟ ",
"اذا قفطت احد تحب تفضحه ولا تستره؟ ",
  "كلمة للشخص اللي يسب ويسطر؟ ",
  "آية من القران تؤمن فيه؟ ",
  "تحب تعامل الناس بنفس المعاملة؟ ولا تكون أطيب منهم؟ ",
"حاجة ودك تغييرها هالفترة؟ ",
  "كم فلوسك حاليا وهل يكفيك ام لا؟ ",
  "وش لون عيونك الجميلة؟ ",
  "من الناس اللي تتغزل بالكل ولا بالشخص اللي تحبه بس؟ ",
  "اذكر موقف ماتنساه بعمرك؟ ",
  "وش حاب تقول للاشخاص اللي بيدخل حياتك؟ ",
  "ألطف شخص مر عليك بحياتك؟ ",
"انت من الناس المؤدبة ولا نص نص؟ ",
  "كيف الصيد معاك هالأيام ؟ وسنارة ولاشبك؟ ",
  "لو الشخص اللي تحبه قال بدخل حساباتك بتعطيه ولا تكرشه؟ ",
  "أكثر شي تخاف منه بالحياه وش؟ ",
  "اكثر المتابعين عندك باي برنامج؟ ",
  "متى يوم ميلادك؟ ووش الهدية اللي نفسك فيه؟ ",
  "قد تمنيت شي وتحقق؟ ",
  "قلبي على قلبك مهما صار لمين تقولها؟ ",
  "وش نوع جوالك؟ واذا بتغييره وش بتأخذ؟ ",
  "كم حساب عندك بالتليجرام؟ ",
  "متى اخر مرة كذبت؟ ",
"كذبت في الاسئلة اللي مرت عليك قبل شوي؟ ",
  "تجامل الناس ولا اللي بقلبك على لسانك؟ ",
  "قد تمصلحت مع أحد وليش؟ ",
  "وين تعرفت على الشخص اللي حبيته؟ ",
  "قد رقمت او احد رقمك؟ ",
  "وش أفضل لعبته بحياتك؟ ",
  "أخر شي اكلته وش هو؟ ",
  "حزنك يبان بملامحك ولا صوتك؟ ",
  "لقيت الشخص اللي يفهمك واللي يقرا افكارك؟ ",
  "فيه شيء م تقدر تسيطر عليه ؟ ",
  "منشن شخص متحلطم م يعجبه شيء؟ ",
"اكتب تاريخ مستحيل تنساه ",
  "شيء مستحيل انك تاكله ؟ ",
  "تحب تتعرف على ناس جدد ولا مكتفي باللي عندك ؟ ",
  "انسان م تحب تتعامل معاه ابداً ؟ ",
  "شيء بسيط تحتفظ فيه؟ ",
  "فُرصه تتمنى لو أُتيحت لك ؟ ",
  "شيء مستحيل ترفضه ؟. ",
  "لو زعلت بقوة وش بيرضيك ؟ ",
  "تنام بـ اي مكان ، ولا بس غرفتك ؟ ",
  "ردك المعتاد اذا أحد ناداك ؟ ",
  "مين الي تحب يكون مبتسم دائما ؟ ",
" إحساسك في هاللحظة؟ ",
  "وش اسم اول شخص تعرفت عليه فالتلقرام ؟ ",
  "اشياء صعب تتقبلها بسرعه ؟ ",
  "شيء جميل صار لك اليوم ؟ ",
  "اذا شفت شخص يتنمر على شخص قدامك شتسوي؟ ",
  "يهمك ملابسك تكون ماركة ؟ ",
  "ردّك على شخص قال (أنا بطلع من حياتك)؟. ",
  "مين اول شخص تكلمه اذا طحت بـ مصيبة ؟ ",
  "تشارك كل شي لاهلك ولا فيه أشياء ما تتشارك؟ ",
  "كيف علاقتك مع اهلك؟ رسميات ولا ميانة؟ ",
  "عمرك ضحيت باشياء لاجل شخص م يسوى ؟ ",
"اكتب سطر من اغنية او قصيدة جا فـ بالك ؟ ",
  "شيء مهما حطيت فيه فلوس بتكون مبسوط ؟ ",
  "مشاكلك بسبب ؟ ",
  "نسبه الندم عندك للي وثقت فيهم ؟ ",
  "اول حرف من اسم شخص تقوله? بطل تفكر فيني ابي انام؟ ",
  "اكثر شيء تحس انه مات ف مجتمعنا؟ ",
  "لو صار سوء فهم بينك وبين شخص هل تحب توضحه ولا تخليه كذا  لان مالك خلق توضح ؟ ",
  "كم عددكم بالبيت؟ ",
  "عادي تتزوج من برا القبيلة؟ ",
  "أجمل شي بحياتك وش هو؟ ",
  
"هل ذكرت الله اليوم؟",
 "هل أنت مُسامح أم لا تستطيع أن تُسامح؟",
 "هل سبق وقمت بالإعتراف بالحب لشخص ورفض طلبك؟",
 "هل يزعجك أسئلة بعض الناس وفضوليتهم في حياتك الشخصيه؟",
 "من هي الشخصية المُميزة في حياتك؟",
 "ما هي أكثر نصيحة مفيدة يمكن أن تخبرني بها؟",
 "هل أنت شخص صريح أم مُنافق؟",
   "ما هو الشيء الذي يُلفت إنتباهك؟",
   "هل تنازلت عن مبدأك في الحياة؟",
  "هل ترى أن أحلامك تحتاج لمعجزة حتى تتحقق؟",
 "ماذا تكون ردة فعلك عندما يخبرك أحد أنك لست جميل ؟",
 "من هو أول شخص تفكر به عندما تشعر بالفرح أو الحزن وتتمنى مشاركته مشاعرك؟",
 "حكمة تؤمن بها؟",
 "هل أنت شخص عُدواني؟",
 "هل يوجد عام مُعين مرّ عليك بشكل سيء جدًا ولا يمكنك نسيانه؟",
 "متى كانت المرة الأخيرة التي قمت خلالها بالبكاء بشدة على أمر ما؟",
 "هل تستطيع أن تعيش بدون أصدقاء؟",
   "إذا أعجبت بشخصٍ ما، كيف تُظهر له هذا الإعجاب أو ما هي الطريقة التي ستتبعها لتظهر إعجابك به؟",
  "هل تشعر بحب التملك؟",
 "ما الذي يجعلك تُصاب بالغضب الشديد؟",
 "هل تحب القراءة؟",
 "هل قلت كلام مُعين تتمنى ألا تقوله؟",
 "هل تُتقن عملك أم تشعر بالممل؟",
 "هل يمكنك تقديم الأعتذار عندما تقترف أي خطأ وتتحمل المسؤولية؟",
 "هل ترى نفسك مُتناقضًا؟",
 "من هو الشخص الذي تُصبح أمامه ضعيفًا؟",
   "ما هي الكلمة التي تُربكك؟",
  "هل ندمت على حب شخص؟",
 "ما هي الصفة التي تود تغييرها حقًا في نفسك؟",
 "هل حاربت من أجل شخص؟",
 "اكثر شخص يخطر ببالك؟",
 "شخص تبتسم عندما تراه؟",
 "هل الغـيِرة حب ام انانية؟",
 "من اذكى برائيك الشباب والا البنات؟",
 "كلمة تقولها للراحلين؟",
   "اللي خانك مرة ترضى تثق فيه ثاني؟",
  "اكثر دولة عربية تحب زيارتها؟",
 "من رحل ثم عاد! هل تبقى مكانته كما كانت عليه بالسابق؟",
 "هل الجلوس وحيدا يجعل مزاجك يتحسن؟",
 "اكثر مقطع أثر فيك يوما؟",
 "اين تجد السعادة؟",
 "مارئيك بمن يحشر انفه بشي لايخصه؟",
 "ايموجي يعبر عن مزاجك حاليا؟",
 "لو كنت تستطيع ﺎلطيران شنو ﺎوݪ شي تسوي ؟",
   "مشهوݛ تتابع كࢦ جديد ݪه ؟",
  "ݛساله تود ﺎيصالها ݪشخص حتى ولو بهمسه ؟",
 "عمرك قابࢦت حيوان عݪى هيئه ﺎنسَان ؟",
 "شخص ﺂو صَاحب عوضک ونسَاک مُر ﭑلحياة ما ﺂسمَه؟",
 "ما هو الشيء الذي لا تستطيع الإستغناء عنه أو العيش بدونه؟",
 "ما هو أسوأ شعور مررت به من قبل؟",
 "هل تستطيع التنازل عن كرامتك من أجل المال؟",
 "كيف تقضي وقت فراغك؟",
 "هل تتعاطى المخدرات ؟",
   "ما هو الموقف الذي تعرضت فيه إلى الاحراج المُبرح؟",
  "هل تعرضت لخيبة أمل من قبل؟",
 "هل سبق وأن أحببتِ شخصية من الرسوم المتحركة وحلمتِ بالزواج منه؟",
 "ما رأيك! هل يُمكن أن تتحول الصداقة إلى حب حقيقي؟",
 "هل شاركت في مسابقة أو بطولة رياضية من قبل؟",
 "هل يمكنك تصنع البكاء؟",
 "كيف ينادي كل منكما الآخر؟ ومن أين أتت هذه الاسم؟",
 "ما هي الرسالة التي تودين إيصالها للأشخاص من حولك؟",
 "هل تفضلين الزواج عن حب أم زواج الصالونات؟",
   "كيف تقيم علاقتك بالآخرين هل أنت شاب اجتماعي أم منغلق؟",
  "هل تحبين زوجك او زوجتك؟",
 "على من كانت أكبر كذبة كذبتها؟",
 "هل تعرضت في حياتك لصدمة عاطفية؟",
 "ما هو الحلم أو الشيء الذي تحتاجين إليه بشدة؟",
 "هل سبق لكي القيام بإحدى عمليات التجمل من قبل؟",
 "كيف تواجه الظروف الصعبة والمشاكل؟",
 "هل أنت مدمن على شيء أو عادة معينة؟",
 "هل تتدخل إذا وجدت شخص يتعرض لحادثة سير أم تتركه وترحل؟",
   "هل يمكن أن تسامحي حبيبك إذا قام بخيانتك؟",
  "هل ترى حياتك كعازب أفضل أم حياتك كمتزوج؟",
 "هل أنت شخص متعلق أم أنه يمكنك التخلي بسهولة؟",
 "ما هو رأيك في حظك؟",
 "ما هو البرج الخاص بك ؟",
 "هل من الممكن أن تضر شخصاً لمجرد أنك تكرهه؟",
 "هل تهتم بنشر الأماكن التي تزورها على مواقع التواصل الاجتماعي؟",
 "تخيلت شي في بالك وصار ؟",
 "ما هي المواد التي كنت تفضلها وانت طالب ؟",
   "هل تدخن السجائر ؟",
  "ما هو الحيوان الذي تود تربيته؟",
 "كيف تفسر العلاقة بين الولد والبنت خارج نطاق الزواج؟",
 "هل سبق وأن تم طردك من المنزل؟ وكم مرة؟",
 "كم تتقاضى في الشهر؟",
 "ما هو رأيك في كل شخص من المتواجدين حولك؟",
 "هل قمت بعمل حادث وتركت الضحية ولذت بالفرار؟",
 "ما هو الإقرار الذي تقره أمام نفسك وأمام الجميع؟",
 "هل تعرضت للخذلان؟",
   "هل تأتمن أصدقائك على الأسرار الخاصة بك؟",
  "كم مرة قدت سياراتك بدون حزام أمان؟",
 "من وجهة نظرك هل يوجد فرق بين الحب والإعجاب بشخص؟ وما هو الأفضل؟",
 "ما هو الشيء الذي يجعلك تشعر بالخوف؟",
 "هل تعرضت للضرب من قبل وكم كان عمرك وقتها؟",
 "ماذا لو كان عليك أن تختار بين الذهاب إلى المستقبل أو العودة إلى الماضي؟",
 "أين ترى نفسك بعد 10 سنوات من الآن؟",
 "ما هي الكلمة التي دائمًا يتم لفظها خطأ؟",
  "هل من الممكن أن تعترف لشخص بالحقيقة رغم معرفتك بخسارته عند معرفته؟",
   "إذا فكرت أن تعتذر لشخص ما، فمن هذا الشخص الذي سيقع عليه هذا الاعتذار؟",
  "هل حبيبتك او حبيبك يملك الصفات التي تريدها أم أنك تحبه كما هو وتحب صفاته لأنه يملكها؟",
 "هل تُعاني من التفكير قبل النوم؟",
 "هل تشعر بالرضا عن نفسك؟",
 "لو خيروك بين امتلاك الصوت الجميل أو المظهر الجميل",
 "متى كانت أخر مرة بكيت فيها؟",
 "من هي الشخصية الكرتونية التي تود أن تصبح مثلها ولماذا؟",
 "من الشخصية التي أثرت في حياتك تأثيرًا إيجابيًا؟",
   "صف لنا فتاة أحلامك؟",
   "كم عدد المرات التي تنازلت فيها من قبل عن مبادئك وقناعاتك من أجل أنثى؟",
  "ما هو أكثر شخص تثق به في هذه الحياة؟",
 "ما هي المهن التي ترى نفسك قادر على الإبداع فيها؟",
 "في أي عام كان اول حب لك ؟",
 "كم كان عمرك عندما احببت أول مرة",
 "كم عدد مرات الخيانه التي اكتشفتها",
 "من صاحب الفضل في حياتك ؟",
 "ما هو الشئ الذي وجدت صعوبة في التعايش معه",
 "ذكرى احزنتك كثيراً ؟",
   "شيء كنت تتمناه ولم يحصل ؟",
  "من الشخص الذي ترهبك فكرة فقدانه ؟",
 "هل فضحت سراً أئتمن عندك ؟",
 "شخص تكرهه ولكنك مضطر للتعامل معه ؟",
 "هل شعرت انك محطم ولا يوجد شئ ينقذك مما انت تعيشه ؟",
 "هل امضيت ليلة كاملة في البكاء على شيء او شخص ؟",
 "تصرف تندم عليه الى الان ؟",
 "ماذا كان يعني لك الماضي ؟",
 "هل راضي بما تملكه الآن ؟",
   "علامه تميزك بين الجميع ما هي ؟",
  "ماذا ترى طريقة تفكيرك هل تفكيرك علماني أم  تفكير تقليدي ؟",
 "شيء ندمت على خسارته ؟",
 "شخص يغير مزاجك بسرعة ؟",
 "هل ترى التدخل العائلي في حياتك جيد بلنسبة لك ؟",
 "هل تعاقبت على خطأ لم تفعله ؟",
 "تصرف تندم عليه الى الان ؟",
 "ماذا كان يعني لك الماضي ؟"]


@Client.on_message(
    filters.command(["/alive", "معلومات", "سورس", "السورس", "❲ السورس ❳"], "")
)
async def alive(client: Client, message):
    chat_id = message.chat.id
    ch = await get_channelsr(client.me.username)
    gr = await get_groupsr(client.me.username)
    keyboard = InlineKeyboardMarkup(
        [
    [
        InlineKeyboardButton("❲ To Install ❳", url=f"https://t.me/S_1_02"),
        InlineKeyboardButton(f"{OWNER_NAME}", url=f"https://t.me/{OWNER[0]}")
    ], 
    [
        InlineKeyboardButton("❲ Add To Your Group ❳", url="https://t.me/{app.username}?startgroup=true")
    ],
    [
        InlineKeyboardButton("❲ Source Ch ❳", url=f"{ch}"),
        InlineKeyboardButton("❲ Exp Source ❳", url=f"{gr}")
    ]
]

    )

    alive = f"""≭︰Welcome to Source Music 𝖍𝖚𝖗𝖗𝖎𝖈𝖆𝖓𝖊 メ"""

    await message.reply_video(
        video=VIDEO,
        caption=alive,
        reply_markup=keyboard,
    )


@Client.on_message(filters.command(["/ping", "بنك"], ""))
async def ping_pong(client: Client, message: Message):
    if not message.chat.type == enums.ChatType.PRIVATE:
      if await joinch(message):
            return
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text("≭︰سرعه السيرفر ↫" f" `{delta_ping * 1000:.3f} ms`")


@Client.on_message(filters.command(["تفعيل"], "") & ~filters.private)
async def pipong(client: Client, message: Message):
   if len(message.command) == 1:
    if not message.chat.type == enums.ChatType.PRIVATE:
      if await joinch(message):
            return
    await message.reply_text("≭︰تم تفعيل المجموعه")
    return 

@app.on_message(filters.command(["/help", "الاوامر", "اوامر"], ""))
async def starhelp(client: Client, message: Message):
    bot = await client.get_me()
    username = client.me.username
    ch = await get_channel(bot.username)
    dev = await get_dev(bot.username)
    devname = await get_dev_name(client, bot.username)
    sddd=f"≭︰مرحبا ↫ ❲ {message.from_user.mention} ❳ \n\n≭︰انا بوت لتشغيل الاغاني في المكالمات\n≭︰يمكنني التشغيل في مجموعه او قناة\n≭︰فقط اضفني وارفعني مشرف  "
    button =   [
                [
                    InlineKeyboardButton("❲ لشراء بوت ❳", url=f"https://t.me/S_1_02")
                ],
                [ 
                    InlineKeyboardButton("❲ اوامر التشغيل ❳", callback_data="bcmds"),
                    InlineKeyboardButton("❲ اوامر التفعيل ❳", callback_data="bhowtouse"),
                ],
                [
                    InlineKeyboardButton(
                        "❲ قناة السورس ❳", url=f"{ch}"
                    ),
                    InlineKeyboardButton(
                        f"{devname}", user_id=f"{dev}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "❲ اضفني لمجموعتك ❳",
                        url=f"https://t.me/{bot.username}?startgroup=true",
                    )
                ],
            ]    
    if not bot.photo:
       return await client.send_message(message.chat.id,sddd, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(button))
    photo = bot.photo.big_file_id
    photo = await client.download_media(photo)
    photo = await gen_bot(client, username, photo)
    await client.send_photo(message.chat.id, photo=photo, caption=sddd, reply_to_message_id=message.id,reply_markup=InlineKeyboardMarkup(button))
    try:os.remove(photo)
    except:pass

@Client.on_message(filters.command(["صاحب السورس", "سورس", "الاصدار", "المبرمج"], "") & ~filters.private)
async def deev(client: Client, message: Message):
     user = await client.get_chat(chat_id="S_1_02")
     name = user.first_name
     username = user.username 
     bio = user.bio 
     user_id = user.id 
     photo = user.photo.big_file_id
     photo = await client.download_media(photo)
     link = await client.export_chat_invite_link(message.chat.id)
     title = message.chat.title if message.chat.title else message.chat.first_name
     chat_title = f"≭︰العضو ↫ ❲ {message.from_user.mention} ❳\n≭︰اسم المجموعه ↫ ❲ {title} ❳" if message.from_user else f"≭︰اسم المجموعه ↫ ❲ {message.chat.title} ❳"
     try:
      await client.send_message(username, f"**≭︰هناك من بحاجه للمساعده**\n{chat_title}",
      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"❲ {title} ❳", url=f"{link}")]]))
     except:
       pass
     await message.reply_photo(
     photo=photo,
     caption=f"**≭︰Information programmer ↯.\n          ━─━─────━─────━─━\n≭︰Name ↬ ❲ {name} ❳** \n**≭︰User ↬ ❲ @{username} ❳**\n**≭︰Bio↬❲ {bio} ❳**",
     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"❲ {name} ❳", user_id=f"{user_id}")]]))
     try:
       os.remove(photo)
     except:
        pass

@Client.on_message(filters.command(["المطور", "مطور"], ""))
async def dev(client: Client, message: Message):
     bot_username = client.me.username
     dev = await get_dev(bot_username)
     user = await client.get_chat(chat_id=dev)
     name = user.first_name
     username = user.username 
     bio = user.bio
     user_id = user.id
     photo = user.photo.big_file_id
     photo = await client.download_media(photo)
     link = await client.export_chat_invite_link(message.chat.id)
     title = message.chat.title if message.chat.title else message.chat.first_name
     chat_title = f"≭︰العضو ↫ ❲ {message.from_user.mention} ❳\n≭︰اسم المجموعه ↫ ❲ {title} ❳" if message.from_user else f"≭︰اسم المجموعه ↫ ❲ {message.chat.title} ❳"
     try:
      await client.send_message(username, f"**≭︰هناك من بحاجه للمساعده**\n{chat_title}",
      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"❲ {title} ❳", url=f"{link}")]]))
     except:
        pass
     await message.reply_photo(
     photo=photo,
     caption=f"**≭︰Information Devloper ↯.\n          ━─━─────━─────━─━\n≭︰Name ↬ ❲ {name} ❳** \n**≭︰User ↬ ❲ @{username} ❳**\n**≭︰Bio↬❲ {bio} ❳**",
     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"❲ {name} ❳", user_id=f"{user_id}")]]))
     try:
       os.remove(photo)
     except:
        pass

@Client.on_message(filters.command("❲ تعيين اسم البوت ❳", ""))
async def set_bot(client: Client, message):
   NAME = await client.ask(message.chat.id, "≭︰ارسل اسم البوت الجديد", filters=filters.text, timeout=30)
   BOT_NAME = NAME.text
   bot_username = client.me.username
   await set_bot_name(bot_username, BOT_NAME)
   await message.reply_text("**≭︰تم تغيير اسم البوت**")

@Client.on_message(filters.command(["❲ حذف downloads ❳"], ""))
async def delete_folder_content(client: Client, message: Message):
    os.system('rm -rf ./downloads/*')
    await message.reply_text("≭︰تم حذف محتوى ملف downloads")
 
@Client.on_message(filters.command(["بوت", "البوت"], ""))
async def bottttt(client: Client, message: Message):
    bot_username = client.me.username
    BOT_NAME = await get_bot_name(bot_username)
    bar = random.choice(selections).format(BOT_NAME)
    await message.reply_text(f"**[{bar}](https://t.me/{bot_username}?startgroup=True)**", disable_web_page_preview=True)
    
@Client.on_message(filters.command(["كت"], ""))
async def bottttttt(client: Client, message: Message):
    if not message.chat.type == enums.ChatType.PRIVATE:
        if await joinch(message):
            return
    bot_username = client.me.username
    BOT_NAME = await get_bot_name(bot_username)
    bar = random.choice(tyet).format(BOT_NAME)
    await message.reply_text(f"**• [{bar}](https://t.me/{bot_username}?startgroup=True)**", disable_web_page_preview=True)
    
@Client.on_message(filters.text)
async def bott(client: Client, message: Message):
    bot_username = client.me.username
    BOT_NAME = await get_bot_name(bot_username)
    if message.text == BOT_NAME:
      bar = random.choice(bot).format(BOT_NAME)
      await message.reply_text(f"**[{bar}](https://t.me/{bot_username}?startgroup=True)**", disable_web_page_preview=True)
    message.continue_propagation()


@Client.on_message(~filters.private)
async def booot(client: Client, message: Message):
    chat_id = message.chat.id
    if not await is_served_chat(client, chat_id):
       try:
        await add_served_chat(client, chat_id)
        chats = len(await get_served_chats(client))
        bot_username = client.me.username
        dev = await get_dev(bot_username)
        username = f"https://t.me/{message.chat.username}" if message.chat.username else None
        mention = message.from_user.mention if message.from_user else message.chat.title
        await client.send_message(dev, f"**≭︰تم تفعيل مجموعه تلقائياً\n≭︰عدد المجموعات الان ↫❲ {chats} ❳ **\n≭︰اسم المجموعه ↫ ❲ [{message.chat.title}]({username}) ❳\n≭︰بواسطه ↫ ❲ {mention} ❳", disable_web_page_preview=True)
        await client.send_message(chat_id, f"**≭︰تم رفع البوت مشرف**")
        return 
       except:
          pass
    message.continue_propagation()
