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
                await self.bot.download_media(self.message_info, file = downloadFolder)
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

