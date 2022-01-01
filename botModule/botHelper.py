#!/usr/bin/env python3


### Importing
# Importing External Packages
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import exceptions, UserNotParticipant
from pyrogram.types import Update, Message
from pymongo import MongoClient
from mega import *
from mega.errors import RequestError

# Importing inbuilt
import string
import random
import time

# Importing Credentials & Required Data
try:
    from testexp.config import Config
except ModuleNotFoundError:
    from config import Config
finally:
    mongoSTR = Config.MONGO_STR


### Global Variable
common_text = '\n\n<b><u>If you are facing any problem😫, so report📝 at @AJPyroVerseGroup</u></b>'
to_login = '<b>If you are not logged in then, send login detail in this format email,password.</b>\n'


### Connecting To Database
mongo_client = MongoClient(mongoSTR)
db_login_detail = mongo_client['MegaUploader']
collection_login = db_login_detail['login_details']


### Defining some functions
#Checking User whether he joined channel and group or not joined.
async def search_user_in_community(
    bot : Update,
    msg : Message
    ):
    try:
        userChannel = await bot.get_chat_member(
            '@AJPyroVerse',
            msg.chat.id
        )
        userGroup = await bot.get_chat_member(
            '@AJPyroVerseGroup',
            msg.chat.id
        )
        if "kicked" in (userGroup.status, userChannel.status):
            await msg.reply_text(
                "<b>You are Banned🚫 from AJPyroVerse Community.\nContact @AJTimePyro (Owner of AJPyroVerse)</b>",
                parse_mode = 'html'
            )
            return
    except UserNotParticipant:
        await msg.reply_text(
            f"<b>To use this bot, you need to Join our channel and Group😁🤪.</b>{common_text}",
            parse_mode = 'html',
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            'Join our Channel.',
                            url = 'https://t.me/AJPyroVerse'
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            'Join our Group.',
                            url = 'https://t.me/AJPyroVerseGroup'
                        )
                    ]
                ]
            )
        )
        return
    except exceptions.bad_request_400.ChatAdminRequired:
        return True
    except Exception as e:
        await bot.send_message(Config.OWNER_ID, "")
        return True
    else:
        return True

def loginInstance(email, password, bot):
    m = Mega()
    try:
        mlog = m.login(email, password)
    except RequestError as e:
        tmpCode = e.code
        if tmpCode == -9:
            print("Email or password is incorrect")
        elif tmpCode == -2:
            print("Email or Password is invalid")
        else:
            print("Something New")
        print(e.message)
        return tmpCode
    except Exception as e:
        bot.send_message(
            Config.OWNER_ID,
            f"Something went Wrong While Login account.\n{e}"
        )
        return None
    else:
        return mlog

# Getting Email & Password From Database
def getting_email_pass(userid):
    myresult  = collection_login.find_one({'userid' : userid})
    if myresult:
        return myresult['email'], myresult['password']
    else:
        return None

def randomChar(size):
    allchar = string.ascii_letters
    char = ''
    for i in range(size):
        char += random.choice(allchar)
    return char

def editProgressMsg(current, total, pmsg, t1):
    completedFloat = (current/1024)/1024
    completed = int(completedFloat)
    stream = current/total
    progress = int(18*stream)
    progress_bar = '■' * progress + '□' * (18 - progress)
    percentage = int((stream)*100)
    speed = round((completedFloat/(time.time() - t1)), 1)
    if speed == 0:
        speed = 0.1
    remaining = int((((total - current)/1024)/1024)/speed)
    
    try:
        pmsg.edit_text(f"<b>Downloading... !! Keep patience...\n {progress_bar}\n📊Percentage: {percentage}%\n✅Completed: {completed} MB\n🚀Speed: {speed} MB/s\n⌚️Remaining Time: {remaining} seconds</b>", parse_mode = 'html')
    except exceptions.bad_request_400.MessageNotModified:
        pass
    finally:
        time.sleep(3)

