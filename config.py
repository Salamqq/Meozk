import os
from os import getenv
from dotenv import load_dotenv
from OWNER import BOT_TOKEN, OWNER, OWNER_NAME, DATABASE, CHANNEL, GROUP, LOGS, PHOTO, VIDEO

if os.path.exists("local.env"):
    load_dotenv("local.env")

load_dotenv()
admins = {}
user = {}
call = {}
dev = {}
logger = {}
logger_mode = {}
botname = {}
appp = {}
helper = {} 



API_ID = int(getenv("API_ID", "11359665"))
API_HASH = getenv("API_HASH", "df66bc5f7f80d04aecd20ebae3708c4d")
BOT_TOKEN = BOT_TOKEN
MONGO_DB_URL = DATABASE
OWNER = OWNER
OWNER_NAME = OWNER_NAME
CHANNEL = CHANNEL
GROUP = GROUP
PHOTO = PHOTO
LOGS = LOGS
VIDEO = VIDEO
