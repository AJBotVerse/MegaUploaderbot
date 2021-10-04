#!/usr/bin/env python3


'''Impoting Libraries, Modules & Credentials'''
from telethon import events
from telethon.errors import rpcerrorlist
from telethon.sync import TelegramClient
from bot.modules.downloader import *
from bot.modules.login import *
from bot.credentials import api_id, api_hash, bot_token
from logging import basicConfig, WARNING


'''For Displaying Errors&Warnings Better'''
basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',level=WARNING)


'''Login as a Bot'''
bot = TelegramClient('MegaUploader', api_id, api_hash).start(bot_token = bot_token)

''''Defining Some Handlers for Bot'''
#Start Handler
@bot.on(events.NewMessage(pattern = r'/start$'))
async def start_handler(event):
    await event.respond(start_msg, parse_mode = 'html')
    return None

#Help Handler
@bot.on(events.NewMessage(pattern = r'/help$'))
async def help_handler(event):
    await event.respond(help_msg, parse_mode = 'html')
    return None

#Accepting Login details
@bot.on(events.NewMessage(pattern = r'\w+\@\w+\.[a-zA-Z]+\,(.+)'))
async def verify_login_detail(event):
    userid = event.sender_id

    #Checking Whether User Already Login or not
    if not collection_login.find_one({'userid' : userid}):
        #Fetching Email & Password From Message
        login_detail = event.message.text
        email, password = login_detail.split(',')
        email = email.strip()   #Removing Whitespaces
        password = password.strip() #Removing Whitespaces
        log_msg = await event.respond(trying_to_login, parse_mode = 'html')

        #Verifying Login detail
        login_object = Login(email, password)
        if login_object.result:
            await bot.edit_message(log_msg, logged_in, parse_mode = 'html')

            #Adding Login Detail To Database
            adding_login_detail_to_database(userid, email, password)
        else:
            await bot.edit_message(log_msg, invalid_login, parse_mode = 'html')
    else:
        await event.respond(already_login, parse_mode = 'html')
    return None

#Logout Handler
@bot.on(events.NewMessage(pattern = r'/revoke$'))
async def revoke_handler(event):
    userid = event.sender_id
    
    #Checking Whether User is Login or not 
    query = {'userid' : userid}
    if collection_login.find_one(query):
        #Removing Login Detail from Database
        collection_login.delete_one(query)
        await event.respond(logged_out, parse_mode = 'html')
    else:
        await event.respond(revoke_failed, parse_mode = 'html')
    return None

@bot.on(events.NewMessage)
async def upload_handler(event):
    message_info = event.message
    
    if message_info.media or message_info.entities:  #Verifying Url And File Media
        userid = event.sender_id
        login_detail = getting_email_pass(userid)
        if login_detail:
            email, password = login_detail  #Getting Login Details
            login_instance = Login(email, password)
            if login_instance.result:
                log_obj = login_instance.log
                if task() == "Running":
                    await event.respond(task_ongoing, parse_mode = 'html')
                else:
                    downloader = await Downloader.start(event, message_info, bot, log_obj)
                    filename = downloader.filename

                    if filename:    #Uploading File
                        msg = downloader.n_msg
                        await Upload.start(filename, log_obj, bot, msg, userid)
                task("No Task")
            else:   #Login Detail is Changed
                await event.respond(login_detail_changed, parse_mode = 'html')
        else:   #Not Logged in
            await event.respond(not_loggin, parse_mode = 'html')
    return None


'''Bot is Started to run all time'''
print('Bot is Started!')
bot.start()
bot.run_until_disconnected()