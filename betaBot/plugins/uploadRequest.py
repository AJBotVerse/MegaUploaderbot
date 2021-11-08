#!/usr/bin/env python3


"""Importing"""
# Importing Common Files
from botModule.importCommon import *

# Importing Developer defined modules
from helper.login import *
from helper.downloader.downloadRequest import *
from helper.uploader import *


"""Some Global Variable"""
listTask = ['']
global counter
counter = 0


"""Request Handler"""
@Client.on_message(filters.private)
async def upload_handler(bot:Update, msg:Message):
    
    if msg.media or msg.entities[0].type == "url":
        if await search_user_in_community(bot, msg):
            userid = msg.chat.id
            login_detail = getting_email_pass(userid)
            if login_detail:
                email, password = login_detail  #Getting Login Details
                login_instance = Login(email, password)
                if login_instance.result:
                    log_obj = login_instance.log
                    global counter
                    counter += 1
                    listTask.append(Multitask(bot, msg, log_obj, userid))
                    bot.loop.create_task(listTask[counter].start())
                else:   #Login Detail is Changed
                    await msg.reply_text(BotMessage.login_detail_changed, parse_mode = 'html')
            else:   #Not Logged in
                await msg.reply_text(BotMessage.not_loggin, parse_mode = 'html')
    return None

""""For Parallel Uploading"""
class Multitask:

    def __init__(self, bot, msg, log_obj, userid):
        self.bot = bot
        self.msg = msg
        self.log_obj = log_obj
        self.userid = userid

    async def start(self):
        downloader = Downloader(self.bot, self.msg, self.log_obj)
        await downloader.start()
        filename = downloader.filename
        Downloadfolder = downloader.Downloadfolder
        if filename:    #Uploading File
            print('uploading')
            self.Uploader = Upload(filename, self.log_obj, self.bot, self.userid, Downloadfolder, downloader.n_msg)
            await self.Uploader.start()
            return

