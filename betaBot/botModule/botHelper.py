#!/usr/bin/env python3


"""Importing"""
# Importing External Packages
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import exceptions, UserNotParticipant
from pymongo import MongoClient
from requests import head

# Importing Inbuilt Packages
import __main__
from inspect import currentframe

# Importing Credentials & Required Data
from botModule.botMSG import BotMessage
try:
    from testexp.config import Config
except ModuleNotFoundError:
    from config import Config
finally:
    mongoSTR = Config.MONGO_STR


fileName = 'botHelper'


'''Connecting To Database'''
mongo_client = MongoClient(mongoSTR)
db_login_detail = mongo_client['MegaUploader']
collection_login = db_login_detail['login_details']


'''Defining Some Functions'''
#Function to find error in which file and in which line
def line_number(fileName, e= ''):
    cf = currentframe()
    return f'In {fileName}.py at line {cf.f_back.f_lineno} {e}'

#Checking User whether he joined channel and group or not joined.
async def search_user_in_community(bot, update):
    try:
        userChannel = await bot.get_chat_member('@AJPyroVerse', update.chat.id)
        userGroup = await bot.get_chat_member('@AJPyroVerseGroup', update.chat.id)
        if "kicked" in (userGroup.status, userChannel.status):
            await update.reply_text(BotMessage.userBanned, parse_mode = 'html')
            return
    except UserNotParticipant:
        await update.reply_text(BotMessage.not_joined_community, parse_mode = 'html',reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton('Join our Channel.',url = 'https://t.me/AJPyroVerse')],
        [InlineKeyboardButton('Join our Group.',url = 'https://t.me/AJPyroVerseGroup')]
        ]))
        return
    except exceptions.bad_request_400.ChatAdminRequired:
        return True
    except Exception as e:
        await update.send_message(Config.OWNER_ID, line_number(fileName, e))
        return True
    else:
        return True

#Adding Login Details To Database
def adding_login_detail_to_database(userid, email, password):
    collection_login.insert_one({
        'userid' : userid,
        'email' : email,
        'password' : password
    })

#Getting Email & Password From Database
def getting_email_pass(userid):
    myresult  = collection_login.find_one({'userid' : userid})
    if myresult:
        return myresult['email'], myresult['password']
    else:
        return None

#it will check the length of file
async def length_of_file(bot, url, userid):
    try:
        h = head(url, allow_redirects=True)
        header = h.headers
        content_length = int(header.get('content-length'))
        file_length = int(content_length/1048576)     #Getting Length of File
    except TypeError:
        return 'Not Valid'
    except Exception as e:  #File is not Exist in Given URL
        await bot.send_message(Config.OWNER_ID, line_number(fileName, e))
        return 'Not Valid'
    else:
        if content_length > 2097152000:  #File`s Size is more than Telegram Limit
            return 'Telegram Limit'
        return 'Valid'
        
        