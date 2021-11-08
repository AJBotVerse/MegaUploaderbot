# !/usr/bin/env python3


"""Importing"""
# Importing Inbuilt packages
from re import match
from shutil import rmtree
from uuid import uuid4
from os import makedirs

# Importing Credentials & Developer defined modules
from helper.downloader.urlDL import UrlDown
from helper.downloader.tgDL import TgDown
from helper.downloader.ytDL import YTDown
from botModule.botMSG import BotMessage


# Importing Credentials & Required Data
try:
    from testexp.config import Config
except ModuleNotFoundError:
    from config import Config


"""Downloader Class"""
class Downloader:

    def __init__(self, bot, msg, log_obj):
        self.bot = bot
        self.msg = msg
        self.log_obj = log_obj
        slash = '//' if '/'in Config.DOWNLOAD_LOCATION else '\\'
        self.Downloadfolder = Config.DOWNLOAD_LOCATION + slash + str(uuid4()) + slash
        makedirs(self.Downloadfolder)
    
    async def start(self):
        if self.msg.media:  #For Telegram File/media
            self.process_msg = await self.msg.reply_text(BotMessage.processing_file, parse_mode = 'html')
            await self.file_downloader()
        else:
            self.url = self.msg.text
            self.process_msg = await self.msg.reply_text(BotMessage.processing_url, parse_mode = 'html')
            if match('^https://(www.)?youtu(.)?be(.com)?/(.*)', self.url):   #For Youtube Video
                await self.youtube_downloader()
            else:   #Normal Url
                await self.url_downloader()
        return self

    #Downloading Youtube Video
    async def youtube_downloader(self):
        rmtree(self.Downloadfolder, ignore_errors = True)
        ytDl = YTDown(self.bot, self.msg, self.process_msg, self.url, self.log_obj)
        await ytDl.start()
        self.filename = None
        return

    #Downloading From url
    async def url_downloader(self):
        urlDl = UrlDown(self.bot, self.msg, self.process_msg, self.Downloadfolder, self.url)
        await urlDl.start()
        self.filename = urlDl.filename
        if urlDl.filename:
            self.n_msg = urlDl.n_msg
            return
        return

    #Downloading From Telegram File/Media
    async def file_downloader(self):
        tgDl = TgDown(self.bot, self.msg, self.process_msg, self.Downloadfolder)
        await tgDl.start()
        self.filename = tgDl.filename
        if self.filename:
            self.n_msg = tgDl.n_msg
            return
        return

