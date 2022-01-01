#!/usr/bin/env python3


### Importing
# Importing Common Files
from botModule.importCom import *


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

        await msg.reply_text("BotMessage.logged_out", parse_mode = 'html')
    
    # If user not found in db
    else:
        await msg.reply_text("BotMessage.revoke_failed", parse_mode = 'html')
    return

