#!/usr/bin/env python3


'''It will Handle Uploading of File'''


'''Importing "remove" Module'''
from os import remove
from bot.funcs import line_number


'''Creating Class For Uploading The File'''
class Upload:

    def __init__(self, filename, login_obj):
        self.filename = filename    #Name Of File
        self.login = login_obj  #Login Session
        
        self.mega()
    
    def mega(self):
        mlog = self.login
        try:    #Trying To Upload the File
            mlog.upload(self.filename)
        except Exception as e:  #Not Uploaded
            self.result = False
            remove(self.filename)
            print(line_number(), e)
        else:   #Successfully Uploaded
            remove(self.filename)
            self.result = True
        return None
    
    