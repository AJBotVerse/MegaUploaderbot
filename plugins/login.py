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

            log_msg = await msg.reply_text(
                "<code>I am trying to login your account.\nSo Please Wait...</code>",
                parse_mode = 'html'
            )

            # Trying to login
            mlog = loginInstance(email, password, bot)

            # Unable to login
            if isinstance(mlog, int):
                if mlog == -2:
                    nmsg = f"<b>Email or Password is incorrect login detail.</b>{common_text}"
                elif mlog == -9:
                    nmsg = f"<b>Please provide a 😒valid login detail.</b>{common_text}"
                else:
                    nmsg = f"<b>Please provide a 😒valid login detail.</b>{common_text}"
            
            # Something went wrong
            elif not mlog:
                nmsg = f"<b>Something Went Wrong.</b>{common_text}"
            
            # Successfully logged in
            else:
                nmsg = "<b>Congratulations🥳🥳</b>, <i>Your account is successfully logged in😊.</i>"

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
            await msg.reply_text(
                "<b>Your account is already login🤪.</b>",
                parse_mode = 'html'
            )
    return

