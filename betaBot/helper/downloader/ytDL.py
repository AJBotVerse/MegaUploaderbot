# !/usr/bin/env python3


"""Importing"""
# Importing External Packages
from pytube import YouTube, exceptions
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Importing Required developer defined data
from helper.uploader import *
from helper.downloader.downloadingData import *


class YTDown:

    def __init__(self, bot, msg, process_msg, url, log_obj):
        self.bot = bot
        self.msg = msg
        self.process_msg = process_msg
        self.url = url
        self.log_obj = log_obj

    async def start(self):

        try:
            self.yt = YouTube(self.url)
            self.qualities = self.yt.streams.filter(adaptive = True)   #Filtering Quality Streams
        except exceptions.VideoUnavailable:
            await self.process_msg.edit_text(BotMessage.ytVideoUnavailable, parse_mode = 'html')
        except Exception as e:
            await self.bot.send_message(OwnerID, f'In ytDL.py {line_number()}\n{e}\n\n{self.url}')
            await self.process_msg.edit_text(BotMessage.unsuccessful_upload, parse_mode = 'html')
        else:
            #Creating Buttons for Selecting Quality
            quality_button = []
            twoButton = []
            for quality in self.qualities:
                if quality.type == "video":
                    value = quality.resolution
                    if not value:
                        continue
                    if quality.fps == 60:
                        value += "60fps"
                    value += ',' + str(int(quality.filesize/1048576)) + 'mb'
                    payload = str((quality.itag, self.url))
                    twoButton.append(InlineKeyboardButton(value, payload))
                    if len(twoButton) == 2:
                        quality_button.append(twoButton)
                        twoButton = []
            if quality_button:
                await self.process_msg.edit_text(BotMessage.choose_quality, parse_mode = 'html', reply_markup=InlineKeyboardMarkup(quality_button))
            else:
                await self.process_msg.edit_text(BotMessage.all_above_limit, parse_mode = 'html')
        finally:
            return

