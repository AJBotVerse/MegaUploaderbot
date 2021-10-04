#!/usr/bin/env python3


'''Impoting Modules & Credentials'''
from pymongo import MongoClient
from requests import head
from bot.credentials import *
from inspect import currentframe
from os import path
import __main__


'''Connecting To Database'''
mongo_client = MongoClient(mongo_connection_string)
db_login_detail = mongo_client['megadb']
collection_login = db_login_detail['mega_collection']


'''Defining Some Functions'''
#Adding Login Details To Database
def adding_login_detail_to_database(userid, email, password):
    collection_login.insert_one({
        'userid' : userid,
        'email' : email,
        'password' : password
    })

#Getting Email & Password From Database
def getting_email_pass(userid):
    myresult  = collection_login.find_one({'userid' : userid})
    if myresult:
        return myresult['email'], myresult['password']
    else:
        return None

#it will check the length of file
async def length_of_file(url):
    try:
        h = head(url, allow_redirects=True)
        header = h.headers
        content_length = int(header.get('content-length'))
        file_length = int(content_length/1048576)     #Getting Length of File
        if content_length > 419430400:  #File`s Size is more than Limit 
            return file_length
        else:   #File`s Size is in the Limit
            return 'Valid'
    except Exception as e:  #File is not Exist in Given URL
        print(e)
        return 'Not Valid'

#Task Updating or Status Checking
def task(status=None):
    if status:
        with open('task.txt', 'w') as newfile:
            newfile.writelines([status])
    else:
        try:
            with open('task.txt') as file:
                return file.readlines()[0]
        except FileNotFoundError:
            return "No Task"

#Function to find error in which file and in which line
def line_number():
    cf = currentframe()
    return f'In File {path.basename(__main__.__file__)} at line {cf.f_back.f_lineno}'

