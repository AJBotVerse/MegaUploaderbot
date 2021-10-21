#!/usr/bin/env python3


"""Importing"""
# Importing External Packages
from telethon import Button
from telethon.errors import rpcerrorlist
from telethon.tl.functions.channels import GetParticipantRequest
from pymongo import MongoClient
from requests import head

# Importing Inbuilt packages
from inspect import currentframe
from os import path
from __main__ import __file__

# Importing Credentials & Developer defined modules
from bot.botMessages import not_joined_community, dev
from bot.botCreds import connection_string
# from testexp.creds import connection_string


'''Connecting To Database'''
mongo_client = MongoClient(connection_string)
db_login_detail = mongo_client['MegaUploader']
collection_login = db_login_detail['login_details']


'''Defining Some Functions'''
#Function to find error in which file and in which line
def line_number():
    cf = currentframe()
    return f'at line {cf.f_back.f_lineno}'

#Checking User whether he joined channel and group or not joined.
async def search_user_in_community(event, bot):
    try:
        await bot(GetParticipantRequest("@AJPyroVerse", event.sender_id))
        await bot(GetParticipantRequest("@AJPyroVerseGroup", event.sender_id))
    except rpcerrorlist.UserNotParticipantError:
        await event.respond(not_joined_community, parse_mode = 'html', buttons = [Button.url('Join our Channel.','https://t.me/AJPyroVerse'), Button.url('Join our Group.','https://t.me/AJPyroVerseGroup')])
        return
    except Exception as e:
        await bot.send_message(dev, f'In funcs.py {line_number()} {e}')
    else:
        return True

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
async def length_of_file(bot, url):
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
        await bot.send_message(dev, f'In funcs.py {line_number()} {e}')
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