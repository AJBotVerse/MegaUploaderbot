#!/usr/bin/env python3


'''Impoting Modules & Credentials'''
from requests import head
from inspect import currentframe
from os import path
from bot.credentials import mongo_connection_string, database_name, collection_name
from pymongo import MongoClient

'''Connecting To Database'''
mongo_client = MongoClient(mongo_connection_string)
db_login_detail = mongo_client[database_name]
collection_login = db_login_detail[collection_name]


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

def line_number():
    cf = currentframe()
    return f'In File {path.basename(__file__)} at line {cf.f_back.f_lineno}'
