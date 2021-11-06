# !/usr/bin/env python3


"""Importing"""
from telethon.errors import rpcerrorlist

# Importing Required developer defined data
from plugins.downloader.downloadingData import *


class TgDown:

    def __init__(self, message_info, process_msg, bot, event, Downloadfolder):
        self.event = event
        self.bot = bot
        self.message_info = message_info
        self.process_msg = process_msg
        self.Downloadfolder = Downloadfolder

    async def start(self):
        
        async def editProgressMsg(btyes, total):
            
            completedFloat = (btyes/1024)/1024
            completed = int(completedFloat)
            current = btyes/total
            progress = int(18*current)
            progress_bar = '■' * progress + '□' * (18 - progress)
            percentage = int((current)*100)
            speed = round((completedFloat/(time() - t1)), 1)
            if speed == 0:
                speed = 0.1
            remaining = int((((total - btyes)/1024)/1024)/speed)
            try:
                self.msg = await self.bot.edit_message(self.msg, f"<b>Downloading... !! Keep patience...\n {progress_bar}\n📊Percentage: {percentage}%\n✅Completed: {completed} MB\n🚀Speed: {speed} MB/s\n⌚️Remaining Time: {remaining} seconds</b>", parse_mode = 'html')
            except rpcerrorlist.MessageNotModifiedError:
                pass
            finally:
                sleep(1)

        def progressBar(bytes, total):
            self.bot.loop.create_task(editProgressMsg(bytes, total))   

        size_of_file = self.message_info.file.size/1024  #Getting Size of File
        if int(self.message_info.file.size) >= 419430400:    #File Size is more than Limit
            await self.bot.edit_message(self.process_msg, f'This filesize is {size_of_file}mb. {file_limit}', parse_mode = 'html')
        else:
            userid = self.event.sender_id
            try:
                files_before = listdir(self.Downloadfolder)
                self.msg = await self.bot.edit_message(self.process_msg, starting_to_download, parse_mode = 'html')
                global t1
                t1 = time()
                #Trying to Download File to Server
                await self.bot.download_media(self.message_info, file = self.Downloadfolder, progress_callback = progressBar)
            except Exception as e:  #Downlading Failed
                await self.bot.delete_messages(None, self.msg)
                await self.bot.send_message(userid, uploading_unsuccessful, parse_mode = 'html')
                await self.bot.send_message(dev, f'In tgDL.py {line_number()} {e}')
                files_after = listdir(self.Downloadfolder)
                try:
                    filename = str([i for i in files_after if i not in files_before][0])
                except IndexError:
                    pass
                else:
                    rmtree(self.Downloadfolder)
            else:
                files_after = listdir(self.Downloadfolder)
                try:
                    filename = str([i for i in files_after if i not in files_before][0])
                except IndexError:  #Dowloading Failed
                    await self.bot.delete_messages(None, self.msg)
                    await self.bot.send_message(userid, uploading_unsuccessful, parse_mode = 'html')
                else:   #File Downloaded Successfully
                    n_msg = await self.bot.edit_message(self.msg, uploading_msg, parse_mode = 'html')
                    self.n_msg, self.filename = n_msg, filename
                    return True

