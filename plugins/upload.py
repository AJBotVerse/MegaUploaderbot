#!/usr/bin/env python3


'''It will Handle Uploading of File'''


"""Importing"""
# Importing Inbuilt packages
from shutil import rmtree

# Importing Credentials & Developer defined modules
from plugins.helper import line_number
from bot.botMessages import successful_uploaded, uploading_unsuccessful, dev


'''Creating Class For Uploading The File'''
class Upload:

    #Construtor
    def __init__(self, filename, login_obj, bot, msg, userid, Downloadfolder):
        self.filename = filename
        self.login = login_obj
        self.bot = bot
        self.msg = msg
        self.userid = userid
        self.Downloadfolder = Downloadfolder
    
    #Uploading File
    async def start(self):
        mlog = self.login
        # self.filePath = f'{self.Downloadfolder}\\{self.filename}'
        self.filePath = f'{self.Downloadfolder}/{self.filename}'
        try:    #Trying To Upload the File
            mlog.upload(self.filePath)
        except Exception as e:  #Not Uploaded
            self.result = False
            rmtree(self.Downloadfolder)
            await self.bot.send_message(dev, f'In funcs.py {line_number()} {e}')
            await self.bot.delete_messages(None, self.msg)
            await self.bot.send_message(self.userid, uploading_unsuccessful, parse_mode = 'html')
        else:   #Successfully Uploaded
            rmtree(self.Downloadfolder)
            await self.bot.delete_messages(None, self.msg)
            await self.bot.send_message(self.userid, successful_uploaded, parse_mode = 'html')
        finally:
            return
    
    