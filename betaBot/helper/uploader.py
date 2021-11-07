#!/usr/bin/env python3


'''It will Handle Uploading of File'''


"""Importing"""
# Importing Inbuilt packages
from shutil import rmtree

# Importing Credentials & Developer defined modules
from botModule.botHelper import line_number
from botModule.botMSG import BotMessage

# Importing Credentials & Required Data
try:
    from testexp.config import Config
except ModuleNotFoundError:
    from config import Config


fileName = 'uploader.py'
'''Creating Class For Uploading The File'''
class Upload:

    #Construtor
    def __init__(self, filename, login_obj, bot, userid, Downloadfolder, msg, slash = '//'):
        self.filename = filename
        self.login = login_obj
        self.bot = bot
        self.userid = userid
        self.Downloadfolder = Downloadfolder
        self.msg = msg
        self.slash = slash
        self.filePath = f'{self.Downloadfolder}{self.slash}{self.filename}'
    
    #Uploading File
    async def start(self):
        mlog = self.login
    
        try:    #Trying To Upload the File
            mlog.upload(self.filePath)
        except Exception as e:  #Not Uploaded
            self.result = False
            rmtree(self.Downloadfolder)
            await self.bot.send_message(Config.OWNER_ID, f'{line_number(fileName)}\n{e}\n\n{self.url}')
            await self.msg.delete()
            await self.bot.send_message(self.userid, BotMessage.uploading_unsuccessful, parse_mode = 'html')
        else:   #Successfully Uploaded
            rmtree(self.Downloadfolder)
            await self.msg.delete()
            await self.bot.send_message(self.userid, BotMessage.successful_uploaded, parse_mode = 'html')
        finally:
            return
    
    