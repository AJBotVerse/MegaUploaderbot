# !/usr/bin/env python3


"""Importing"""
# Importing Required developer defined data
from plugins.downloader.downloadingData import *


class TgDown:

    def __init__(self, message_info, process_msg, bot, event) -> None:
        self.event = event
        self.bot = bot
        self.message_info = message_info
        self.process_msg = process_msg

    async def start(self):

        #Editing Progress Bar
        async def edit_msg(progress_bar, percentage, completed, speed, remaining):
            self.msg = await self.bot.edit_message(self.msg, f"<b>Downloading... !! Keep patience...\n [ {progress_bar}]\n📊Percentage: {percentage}%\n✅Completed: {completed} MB\n🚀Speed: {speed} MB/s\n⌚️Remaining Time: {remaining} seconds</b>", parse_mode = 'html')

        def progress_function(current, total):
            progress = int(18*current)
            progress_bar = '■' * progress + '□' * (18 - progress)
            percentage = int(current*100)
            completed = int((current/1024)/1024)
            time_taken = int(time()) - t1
            speed = round(completed/time_taken, 2)
            if speed == 0:
                speed = 0.1
            remaining = int((((total - current)/1024)/1024)/speed)
            self.bot.loop.create_task(edit_msg(progress_bar, percentage, completed, speed, remaining))
            pass

        size_of_file = self.message_info.file.size/1024  #Getting Size of File
        if int(self.message_info.file.size) >= 419430400:    #File Size is more than Limit
            await self.bot.edit_message(self.process_msg, f'This filesize is {size_of_file}mb. {file_limit}', parse_mode = 'html')
        else:
            userid = self.event.sender_id
            try:
                files_before = listdir(downloadFolder)
                self.msg = await self.bot.edit_message(self.process_msg, starting_to_download, parse_mode = 'html')
                global t1
                t1 = time()
                #Trying to Download File to Server
                await self.bot.download_media(self.message_info, file = downloadFolder, progress_callback = progress_function)
            except Exception as e:  #Downlading Failed
                task("No Task")
                await self.bot.delete_messages(None, self.msg)
                await self.bot.send_message(userid, uploading_unsuccessful, parse_mode = 'html')
                await self.bot.send_message(dev, f'In tgDL.py {line_number()} {e}')
                files_after = listdir(downloadFolder)
                try:
                    filename = str([i for i in files_after if i not in files_before][0])
                except IndexError:
                    pass
                else:
                    remove(f'{downloadFolder}{filename}')
            else:
                files_after = listdir(downloadFolder)
                try:
                    filename = str([i for i in files_after if i not in files_before][0])
                except IndexError:  #Dowloading Failed
                    task("No Task")
                    await self.bot.delete_messages(None, self.msg)
                    await self.bot.send_message(userid, uploading_unsuccessful, parse_mode = 'html')
                else:   #File Downloaded Successfully
                    n_msg = await self.bot.edit_message(self.msg, uploading_msg, parse_mode = 'html')
                    self.n_msg, self.filename = n_msg, filename
                    return True

