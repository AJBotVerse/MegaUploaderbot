# !/usr/bin/env python3


"""Importing"""
from pyrogram.errors import exceptions

# Importing Required developer defined data
from helper.downloader.downloadingData import *


class TgDown:

    def __init__(self, bot, msg, process_msg, Downloadfolder):
        self.msg = msg
        self.bot = bot
        self.process_msg = process_msg
        self.Downloadfolder = Downloadfolder

    async def start(self):
        
        async def __editProgressMsg(current, total):
            completedFloat = (current/1024)/1024
            completed = int(completedFloat)
            stream = current/total
            progress = int(18*stream)
            progress_bar = '■' * progress + '□' * (18 - progress)
            percentage = int((stream)*100)
            speed = round((completedFloat/(time() - t1)), 1)
            if speed == 0:
                speed = 0.1
            remaining = int((((total - current)/1024)/1024)/speed)
            
            try:
                self.process_msg = await self.process_msg.edit_text(f"<b>Downloading... !! Keep patience...\n {progress_bar}\n📊Percentage: {percentage}%\n✅Completed: {completed} MB\n🚀Speed: {speed} MB/s\n⌚️Remaining Time: {remaining} seconds</b>", parse_mode = 'html')
            except exceptions.bad_request_400.MessageNotModified:
                pass
            finally:
                sleep(1)

        def __progressBar(current, total):
            self.bot.loop.create_task(__editProgressMsg(current, total))   

        global t1
        t1 = time()
        self.filename = self.msg.download(progress = __progressBar)
        if self.filename:
            try:
                self.n_msg = self.process_msg.edit_text(BotMessage.uploading_msg, parse_mode = 'html')
            except exceptions.bad_request_400.MessageNotModified:
                pass
            return True
        else:
            rmtree(self.Downloadfolder)
            await self.process_msg.delete()
            await self.msg.reply_text(BotMessage.uploading_unsuccessful, parse_mode = 'html')
            return

