#!/usr/bin/env python3


'''It will Handle Uploading of File'''


'''Importing Modules and Libraries'''
from os import remove
from bot.modules.funcs import line_number, task
from bot.perma_var import successful_uploaded, uploading_unsuccessful


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
        try:    #Trying To Upload the File
            mlog.upload(self.filename)
        except Exception as e:  #Not Uploaded
            self.result = False
            remove(self.filename)
            print(line_number(), e)
            await bot.delete_messages(None, msg)
            await bot.send_message(userid, uploading_unsuccessful, parse_mode = 'html')
        else:   #Successfully Uploaded
            remove(self.filename)
            await bot.delete_messages(None, msg)
            await bot.send_message(userid, successful_uploaded, parse_mode = 'html')
        task("No Task")
        return None
    
    