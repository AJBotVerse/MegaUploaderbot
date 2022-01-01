#!/usr/bin/env python3


### Importing
# Importing Common Files
from botModule.importCom import *


### Email & Password handler
@Client.on_message(filters.private & filters.regex('[\w\.]+@[\w\.]+(\s*),(\s*)[\S]+'))
async def start_handler(bot:Update, msg:Message):
    if await search_user_in_community(bot, msg):

        userid = msg.chat.id
        query = {
            'userid' : userid
        }

        # If not already logged in
        if not collection_login.find_one(query):

            #Fetching Email & Password From Message
            login_detail = msg.text
            email, password = login_detail.split(',')
            email = email.strip()   #Removing Whitespaces
            password = password.strip() #Removing Whitespaces

            log_msg = await msg.reply_text("BotMessage.trying_to_login", parse_mode = 'html')

            # Trying to login
            mlog = loginInstance(email, password, bot)

            # Unable to login
            if isinstance(mlog, int):
                if mlog == -2:
                    nmsg = "Email or Password is incorrect."
                elif mlog == -9:
                    nmsg = "Email or Password is invalid"
                else:
                    nmsg = "Email or Password is invalid"
            
            # Something went wrong
            elif not mlog:
                nmsg = "Something Went Wrong."
            
            # Successfully logged in
            else:
                nmsg = "Successfully Logged in."

                # Adding in db
                collection_login.insert_one(
                    {
                        'userid' : userid,
                        'email' : email,
                        'password' : password
                    }
                )
            await log_msg.edit_text(
                nmsg,
                parse_mode = 'html'
            )
        
        # If already logged in
        else:
            await msg.reply_text("Already Logged in.", parse_mode = 'html')
    return

