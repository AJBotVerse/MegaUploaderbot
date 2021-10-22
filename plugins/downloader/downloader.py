# !/usr/bin/env python3


"""Importing"""
# Importing Inbuilt packages
from re import match

# Importing Credentials & Developer defined modules
from plugins.downloader.urlDL import UrlDown
from plugins.downloader.tgDL import TgDown
from plugins.downloader.ytDL import YTDown
from plugins.helper import *
from bot.botMessages import *


"""Downloader Class"""
class Downloader:

    def __init__(self, event, message_info, bot):
        self.event = event
        self.message_info = message_info
        self.bot = bot
    
    @classmethod
    async def start(cls, event, message_info, bot, log_object):
        self = cls(event, message_info, bot)
        if message_info.file:  #For Telegram File/media
            process_msg = await event.respond(processing_file, parse_mode = 'html')
            await self.file_downloader(self.event, process_msg, self.bot, message_info)
        else:
            url = message_info.text
            process_msg = await event.respond(processing_url, parse_mode = 'html')
            if match('^https://(www.)?youtu(.)?be(.com)?/(.*)', url):   #For Youtube Video
                await self.youtube_downloader(process_msg, self.bot, url, log_object)
            else:   #Normal Url
                await self.url_downloader(self.event, process_msg, self.bot, url)
        return self

    #Downloading Youtube Video
    async def youtube_downloader(self, process_msg, bot, url, log_object):
        task("Running")
        ytDl = YTDown(self.event, process_msg, bot, url, log_object)
        await ytDl.start()
        self.filename = None
        return

    #Downloading From url
    async def url_downloader(self, event, process_msg, bot, url):
        task("Running")
        urlDl = UrlDown(event, process_msg, bot, url)
        await urlDl.start()
        if urlDl.filename:
            self.filename = urlDl.filename
            self.n_msg = urlDl.n_msg
            return
        self.filename = None
        task("No Task")
        return


    #Downloading From Telegram File/Media
    async def file_downloader(self, event, process_msg, bot, message_info):
        task("Running")
        tgDl = TgDown(message_info, process_msg, bot, event)
        await tgDl.start()
        if tgDl.filename:
            self.filename = tgDl.filename
            self.n_msg = tgDl.n_msg
            return
        self.filename = None
        task("No Task")
        return