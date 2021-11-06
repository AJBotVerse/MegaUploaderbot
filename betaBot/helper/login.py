#!/usr/bin/env python3

'''It will handle All Login Requests'''


'''Some Modules & Library'''
from mega import *
from mega.errors import RequestError
from plugins.helper import line_number


'''Login Class'''
class Login:
    
    def __init__(self, email, password):
        self.email = email  #Email of Mega Account
        self.password = password    #Password of Mega Account
        self.mega_login()
    
    def mega_login(self):
        m = Mega()  #Instance of Mega
        
        try:    #Verifying Login Detail
            mlog = m.login(self.email, self.password)
        except RequestError:    #Invalid Login Detail
            self.result = False
        except Exception as e:  #Anyother Error
            print(line_number(), e)
            self.result = False
        else:   #Valid Login Detail
            self.result = True
            self.log = mlog
        
    