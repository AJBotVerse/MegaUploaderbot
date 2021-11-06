#!/usr/bin/env python3


"""Importing"""
# Importing Common Files
from botModule.importCommon import *

# Importing Developer defined modules
from helper.login import *

#Accepting Login details
@Client.on_message(filters.regex(r'\w+\@\w+\.[a-zA-Z]+\,(.+)'))
async def verify_login_detail(msg:Message, bot:Update):
    if await search_user_in_community(bot, msg):
        userid = msg.chat.id

        #Checking Whether User Already Login or not
        if not collection_login.find_one({'userid' : userid}):
            #Fetching Email & Password From Message
            login_detail = msg.text
            email, password = login_detail.split(',')
            email = email.strip()   #Removing Whitespaces
            password = password.strip() #Removing Whitespaces
            log_msg = await msg.reply_text(BotMessage.trying_to_login, parse_mode = 'html')

            #Verifying Login detail
            login_object = Login(email, password)
            if login_object.result:
                await log_msg.edit_text(BotMessage.logged_in , parse_mode= 'html')

                #Adding Login Detail To Database
                adding_login_detail_to_database(userid, email, password)
            else:
                await log_msg.edit_text(BotMessage.invalid_login , parse_mode= 'html')
        else:
            await msg.reply_text(BotMessage.already_login, parse_mode = 'html')
    return None

    