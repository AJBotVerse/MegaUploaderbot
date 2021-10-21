#!/usr/bin/env python3


'''It will Handle Uploading of File'''


"""Importing"""
# Importing Inbuilt packages
from os import remove

# Importing Credentials & Developer defined modules
from plugins.helper import line_number, task
from bot.botMessages import successful_uploaded, uploading_unsuccessful, downloadFolder, dev


'''Creating Class For Uploading The File'''
class Upload:

    #Construtor
    def __init__(self, filename, login_obj, bot, msg, userid):
        self.filename = filename
        self.login = login_obj
        self.bot = bot
        self.msg = msg
        self.userid = userid

    #Starter
    @classmethod
    async def start(cls, filename, log_obj, bot, msg, userid):
        self = cls(filename, log_obj, bot, msg, userid)
        await self.upload_start(self.bot, self.msg, self.userid)
    
    #Uploading File
    async def upload_start(self, bot, msg, userid):
        mlog = self.login
        self.filePath = f'{downloadFolder}{self.filename}'
        try:    #Trying To Upload the File
            mlog.upload(self.filePath)
        except Exception as e:  #Not Uploaded
            self.result = False
            remove(self.filePath)
            await bot.send_message(dev, f'In funcs.py {line_number()} {e}')
            await bot.delete_messages(None, msg)
            await bot.send_message(userid, uploading_unsuccessful, parse_mode = 'html')
        else:   #Successfully Uploaded
            remove(self.filePath)
            await bot.delete_messages(None, msg)
            await bot.send_message(userid, successful_uploaded, parse_mode = 'html')
        finally:
            task("No Task")
            return
    
    