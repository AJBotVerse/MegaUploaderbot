#!/usr/bin/env python3


"""Importing"""
# Importing Common Files
from botModule.importCommon import *


#Logout Handler
@Client.on_message(filters.private & filters.command("revoke"))
async def revoke_handler(msg:Message, bot:Update):
    userid = msg.chat.id
    
    #Checking Whether User is Login or not 
    query = {'userid' : userid}
    if collection_login.find_one(query):
        #Removing Login Detail from Database
        collection_login.delete_one(query)
        await msg.reply_text(BotMessage.logged_out, parse_mode = 'html')
    else:
        await msg.reply_text(BotMessage.revoke_failed, parse_mode = 'html')
    return None

    