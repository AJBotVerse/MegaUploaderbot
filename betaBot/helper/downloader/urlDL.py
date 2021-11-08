# !/usr/bin/env python3


"""Importing"""
# Importing External Packages
from pySmartDL import SmartDL
from pyrogram.errors import exceptions

# Importing Required developer defined data
from helper.downloader.downloadingData import *


class UrlDown:

    def __init__(self, bot, msg, process_msg, Downloadfolder, url):
        self.bot = bot
        self.msg = msg
        self.process_msg = process_msg
        self.Downloadfolder = Downloadfolder
        self.url = url

    async def start(self):
        len_file = await length_of_file(self.bot, self.url)
        if len_file == 'Valid':
            try:
                self.process_msg = await self.process_msg.edit_text(BotMessage.starting_to_download, parse_mode = 'html')
            except exceptions.bad_request_400.MessageNotModified:
                pass
            
            downObj = SmartDL(self.url, dest = self.Downloadfolder)
            downObj.start(blocking = False)

            while not downObj.isFinished():
                progress_bar = downObj.get_progress_bar().replace('#', '■').replace('-', '□')
                completed = downObj.get_dl_size(human=True)
                speed = downObj.get_speed(human=True)
                remaining = downObj.get_eta(human=True)
                percentage = int(downObj.get_progress()*100)

                try:
                    self.process_msg = await self.process_msg.edit_text(f"<b>Downloading... !! Keep patience...\n {progress_bar}\n📊Percentage: {percentage}%\n✅Completed: {completed}\n🚀Speed: {speed}\n⌚️Remaining Time: {remaining}</b>", parse_mode = 'html')
                except exceptions.bad_request_400.MessageNotModified:
                    pass
                finally:
                    sleep(1)
            
            if downObj.isSuccessful():
                try:
                    n_msg = await self.process_msg.edit_text(BotMessage.uploading_msg, parse_mode = 'html')
                except exceptions.bad_request_400.MessageNotModified:
                    pass
                self.n_msg = n_msg
                self.filename = path.basename(downObj.get_dest())
                return True
            else:
                try:
                    rmtree(self.Downloadfolder)
                except Exception as e:
                    await self.process_msg.delete()
                    await self.msg.reply_text(BotMessage.unsuccessful_upload, parse_mode = 'html')
                    for e in downObj.get_errors():
                        await self.bot.send_message(OwnerID, f'In urlDL.py {line_number()} {str(e)}\n\n{self.url}')
                else:
                    await self.bot.send_message(OwnerID, f'In urlDL.py {line_number()}\n\n{self.url}')

        elif len_file == 'Not Valid':
            try:
                await self.process_msg.edit_text(BotMessage.unsuccessful_upload, parse_mode = 'html')
            except exceptions.bad_request_400.MessageNotModified:
                pass
        else:
            try:
                await self.process_msg.edit_text(f'This filesize is **{len_file}mb**. {BotMessage.file_limit}', parse_mode = 'html')
            except exceptions.bad_request_400.MessageNotModified:
                pass
        self.filename = None