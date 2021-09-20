#!/usr/bin/env python3


'''Impoting Modules & Credentials'''
from requests import head
from inspect import currentframe, getframeinfo
from os import path
from bot.credentials import host, user, password, database
import mysql.connector


'''Connecting To Database'''
mydb = mysql.connector.connect(
    host = host,
    user = user,
    password = password,
    database = database
)
mycursor = mydb.cursor()


'''Defining Some Functions'''
#Checking User whether he joined channel and group or not joined.
def search_user_in_community(userid):
    #Checking User ID Database
    mycursor.execute(f'Select user_id From channel_members where user_id={userid}')
    channel_membership = mycursor.fetchone()
    if channel_membership:
        mycursor.execute(f'Select user_id From group_members where user_id={userid}')
        return mycursor.fetchone()
    return None

#Adding Login Details To Database
def adding_login_detail_to_database(userid, email, password):
    mycursor.execute(f'Select * from login_details where user_id={userid}') #Checking User in Database
    myresult = mycursor.fetchone()
    #Adding User`s Login Detail in Database
    if myresult:
        mycursor.execute(f'Update login_details Set mega_email="{email}" where user_id={userid}')
        mydb.commit()
        mycursor.execute(f'Update login_details Set mega_password="{password}" where user_id={userid}')
        mydb.commit()
    else:
        mycursor.execute(f'insert into login_details (user_id, mega_email, mega_password) values ({userid}, "{email}", "{password}")')
        mydb.commit()

#Getting Email & Password From Database
def getting_email_pass(userid):
    mycursor.execute(f'select mega_email, mega_password from login_details Where user_id={userid}')
    myresult = mycursor.fetchone()
    if myresult and myresult[0]:
        return myresult
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