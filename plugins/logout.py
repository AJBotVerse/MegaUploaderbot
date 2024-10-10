#!/usr/bin/env python3


### Importing
# Importing Common Files
from botModule.importCom import *

parse_mode=enums.ParseMode.HTML

### Logout Handler
@Client.on_message(filters.private & filters.command("revoke"))
async def revoke_handler(bot:Update, msg:Message):
    userid = msg.chat.id
    query = {
        'userid' : userid
    }

    # If user found in db
    if collection_login.find_one(query):

        #Removing Login Detail from Database
        collection_login.delete_one(query)

        await msg.reply_text(
            "Your account is now logged out🥺.\nTo Login again send your login detail.",
            #parse_mode = 'html' 
             parse_mode
        )
    
    # If user not found in db
    else:
        await msg.reply_text(
            f"<b><u>You are not even logged in😒. So how can I remove your account.</u></b>{common_text}",
            #parse_mode = 'html' 
             parse_mode
        )
    return

