#!/usr/bin/env python3


"""Importing"""
# Importing External Packages
from telethon import events
from telethon.sync import TelegramClient

# Importing Inbuilt packages
from logging import basicConfig, WARNING

# Importing Credentials & Developer defined modules
from plugins.downloader.downloader import *
from plugins.login import *
from plugins.upload import Upload
from bot.botCreds import api_id, api_hash, bot_token
# from testexp.creds import api_id, api_hash, bot_token


'''For Displaying Errors&Warnings Better'''
basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',level=WARNING)


'''Login as a Bot'''
bot = TelegramClient('MegaUploader', api_id, api_hash).start(bot_token = bot_token)


''''Defining Some Handlers for Bot'''
#Start Handler
@bot.on(events.NewMessage(pattern = r'/start$'))
async def start_handler(event):
    if await search_user_in_community(event, bot):
        await event.respond(start_msg, parse_mode = 'html')
    return

#Help Handler
@bot.on(events.NewMessage(pattern = r'/help$'))
async def help_handler(event):
    if await search_user_in_community(event, bot):
        await event.respond(help_msg, parse_mode = 'html')
    return

#Accepting Login details
@bot.on(events.NewMessage(pattern = r'\w+\@\w+\.[a-zA-Z]+\,(.+)'))
async def verify_login_detail(event):
    if await search_user_in_community(event, bot):
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

#For Owner Only, Sent message to all Bot Users
@bot.on(events.NewMessage(pattern = r'/broadcast'))
async def broadcast_handler(event):
    if dev == event.sender_id:
        try:
            #Extracting Broadcasting Message
            message = str(event.message.text).split('/broadcast ')[1]
        except IndexError:
            await event.respond(broadcast_failed, parse_mode = 'html')
        except Exception as e:
            await event.respond(f'In __main__.py {line_number()} {e}')
        else:
            #Getting User`s Id from Database
            for userid in [document['userid'] for document in collection_login.find()]:
                try:
                    #Sending Message One By One
                    await bot.send_message(userid[0], message)
                except rpcerrorlist.UserIsBlockedError:
                    pass
                except Exception as e:
                    await event.respond(f'In __main__.py {line_number()} {e}')
    return None

@bot.on(events.NewMessage)
async def upload_handler(event):
    message_info = event.message
    entity = message_info.entities

    if message_info.media or entity:  #Verifying Url And File Media
        if entity:
            if str(type(message_info.entities[0])) not in ("<class 'telethon.tl.types.MessageEntityUrl'>", "<class 'telethon.tl.types.MessageEntityMention'>"):
                return
        if await search_user_in_community(event, bot):
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