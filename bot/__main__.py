#!/usr/bin/env python3


'''Impoting Libraries, Modules & Credentials'''
from telethon import events, Button
from telethon.errors import rpcerrorlist
from telethon.sync import TelegramClient
import cryptg   #For Increasing speed of File Downloading
from bot.login import *
from bot.funcs import *
from bot.upload import *
from bot.perma_var import *
from subprocess import Popen
from pytube import YouTube
from re import match
from os import listdir
from bot.credentials import api_id, api_hash, bot_token
from logging import basicConfig, WARNING


'''Task Status Going On'''
task = False


'''For Displaying Errors&Warnings Better'''
basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',level=WARNING)


'''Login as a Bot'''
bot = TelegramClient('AJTime', api_id, api_hash).start(bot_token = bot_token)


''''Defining Some Handlers for Bot'''
#Start Handler
@bot.on(events.NewMessage(pattern = r'/start$'))
async def start_handler(event):
    if not search_user_in_community(event.sender_id):
        await event.respond(not_joined_community, parse_mode = 'html', buttons = [Button.url('Join our Channel.','https://t.me/AJBotVerse'), Button.url('Join our Group.','https://t.me/AJBotVerseGroup')])
    else:
        await event.respond(start_msg, parse_mode = 'html')
    return None

#Help Handler
@bot.on(events.NewMessage(pattern = r'/help$'))
async def help_handler(event):
    if not search_user_in_community(event.sender_id):
        await event.respond(not_joined_community, parse_mode = 'html', buttons = [Button.url('Join our Channel.','https://t.me/AJBotVerse'), Button.url('Join our Group.','https://t.me/AJBotVerseGroup')])
    else:
        await event.respond(help_msg, parse_mode = 'html')
    return None

#Accepting Login details
@bot.on(events.NewMessage(pattern = r'[a-zA-Z0-9]*\@[a-zA-Z0-9]*\.[a-zA-Z]*\,(.*)'))
async def verify_login_detail(event):
    userid = event.sender_id
    if not search_user_in_community(userid):
        await event.respond(not_joined_community, parse_mode = 'html', buttons = [Button.url('Join our Channel.','https://t.me/AJBotVerse'), Button.url('Join our Group.','https://t.me/AJBotVerseGroup')])
    else:
        #Fetching Email & Password From Message
        login_detail = event.message.text
        email, password = login_detail.split(',')
        email = email.strip()   #Removing Whitespaces
        password = password.strip() #Removing Whitespaces

        #Checking Whether User Already Login or not
        mycursor.execute(f'Select mega_email From login_details Where user_id={userid}')
        myresult = mycursor.fetchone()
        try:
            myresult = myresult[0]
        except TypeError:
            pass
        except Exception as e:
            print(line_number(), e)
        if not myresult:
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
    if not search_user_in_community(userid):
        await event.respond(not_joined_community, parse_mode = 'html', buttons = [Button.url('Join our Channel.','https://t.me/AJBotVerse'), Button.url('Join our Group.','https://t.me/AJBotVerseGroup')])
    else:
        #Checking Whether User is Login or not
        mycursor.execute(f'Select mega_email from login_details where user_id={userid}')
        myresult = mycursor.fetchone()
        try:
            myresult = myresult[0]
        except TypeError:
            pass
        except Exception as e:
            print(line_number(), e)
        if myresult:
            #Removing Login Detail from Database
            mycursor.execute(f'Update login_details Set mega_email=Null where user_id={userid}')
            mydb.commit()
            mycursor.execute(f'Update login_details Set mega_password=Null where user_id={userid}')
            mydb.commit()
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
            print(line_number(), e)
        else:
            #Getting User`s Id from Database
            mycursor.execute('Select user_id from login_details')
            myresult = mycursor.fetchall()
            for userid in myresult:
                try:
                    #Sending Message One By One
                    await bot.send_message(userid[0], message)
                except rpcerrorlist.UserIsBlockedError:
                    pass
                except Exception as e:
                    print(line_number(), e)
    return None

#Downloading From url
async def url_downloader(userid, event, url):
    len_file = await length_of_file(url)
    if len_file == 'Valid':
        msg = await bot.edit_message(process_msg, starting_to_download, parse_mode = 'html')
        try:
            files_before = listdir()

            #Downloading File From Url
            output = Popen(['wget', url])
            output.wait()
        except Exception as e:
            print(line_number(), e)
            await bot.delete_messages(None, msg)
            await bot.send_message(userid, unsuccessful_upload, parse_mode = 'html')
            files_after = listdir()
            try:
                #Getting InComplete Filename
                filename = str([i for i in files_after if i not in files_before][0])
            except IndexError:
                pass
            except Exception as e:
                print(line_number(), e)
            else:
                #Reomving Incomplete File
                remove(filename)
                return None
        else:
            files_after = listdir()
            try:
                filename = str([i for i in files_after if i not in files_before][0])
            except IndexError:  #When File Not Downloaded
                await bot.delete_messages(None, msg)
                await bot.send_message(userid, unsuccessful_upload, parse_mode = 'html')
            except Exception as e:
                print(line_number(), e)
            else:
                if 'html' in filename:  #Source Of Website(html file)
                    remove(filename)
                    await bot.delete_messages(None, msg)
                    await bot.send_message(userid, unsuccessful_upload, parse_mode = 'html')
                else:
                    #File Downloaded Successfully
                    global n_msg
                    n_msg = await bot.edit_message(msg, uploading_msg, parse_mode = 'html')
                    return filename
    elif len_file == 'Not Valid':
        await bot.edit_message(process_msg, unsuccessful_upload, parse_mode = 'html')
    else:
        await bot.edit_message(process_msg, f'This filesize is **{len_file}mb**. {file_limit}', parse_mode = 'html')
    task = False
    return None

#Downloading Youtube Video
async def youtube_downloader(userid, event, url, log_object):
    try:
        yt = YouTube(url)
        qualities = yt.streams.filter(progressive = True)   #Filtering Streams Having Audio & Video
    except Exception as e:
        task = False
        print(line_number(), e)
        await bot.edit_message(process_msg, unsuccessful_upload, parse_mode = 'html')
    else:
        #Creating Buttons for Selecting Quality
        quality_button = [Button.inline(f'{quality.resolution}, {int(quality.filesize/1048576)}mb', quality.itag) for quality in qualities if quality.filesize <= 419430400]
        if quality_button:
            msg = await bot.edit_message(process_msg, choose_quality, parse_mode = 'html', buttons = quality_button)
            
            #CallBackQuery For Youtube Video Uploader
            @bot.on(events.CallbackQuery)
            async def Youtube_Video_CallBack(event):
                #Getting String Value From event.data
                itag = event.data.decode('utf-8')
                files_before = listdir()
                stream = yt.streams.get_by_itag(itag)

                #Trying To Download Video To Server
                await bot.edit_message(msg, starting_to_download, parse_mode = 'html')
                try:
                    stream.download()
                except Exception as e:
                    task = False
                    files_after = listdir()
                    print(line_number(), e)
                    await bot.edit_message(msg, unsuccessful_upload, parse_mode = 'html')
                    try:
                        filename = str([i for i in files_after if i not in files_before][0])
                    except IndexError:
                        pass
                    except Exception as e:
                        print(line_number(), e)
                    else:
                        #Deleting Incomplete File
                        remove(filename)
                else:
                    files_after = listdir()
                    try:
                        filename = str([i for i in files_after if i not in files_before][0])
                    except IndexError:
                        #File Not Downloaded
                        task = False
                        await bot.edit_message(msg, unsuccessful_upload, parse_mode = 'html')
                    except Exception as e:
                        task = False
                        print(line_number(), e)
                    else:
                        #File Downloaded Successfully to Server
                        global n_msg
                        n_msg = await bot.edit_message(msg, uploading_msg, parse_mode = 'html')

                        #Uploading File to Mega Drive
                        upload = Upload(filename, log_object)
                        if upload.result:   #Successfully Uploaded
                            await bot.delete_messages(None, n_msg)
                            await bot.send_message(userid, successful_uploaded, parse_mode = 'html')
                        else:   #Not Uploaded
                            await bot.delete_messages(None, n_msg)
                            await bot.send_message(userid, uploading_unsuccessful, parse_mode = 'html')
                        task = False
        else:
            task = False
            await bot.edit_message(process_msg, all_above_limit, parse_mode = 'html')
    return None

#Downloading From Telegram File/Media
async def file_downloader(userid, event, message_info):
    #Getting Size of File
    size_of_file = message_info.file.size/1024
    if int(message_info.file.size) >= 419430400: #File Size is more than Limit
        await bot.edit_message(process_msg, f'This filesize is {size_of_file}mb. {file_limit}', parse_mode = 'html')
    else:
        try:
            files_before = listdir()
            msg = await bot.edit_message(process_msg, starting_to_download, parse_mode = 'html')

            #Trying to Download File to Server
            await bot.download_media(message_info)
        except Exception as e:  #Downlading Failed
            await bot.delete_messages(None, msg)
            await bot.send_message(userid, uploading_unsuccessful, parse_mode = 'html')
            print(line_number(), e)
            files_after = listdir()
            try:
                filename = str([i for i in files_after if i not in files_before][0])
            except IndexError:
                pass
            except Exception as e:
                print(line_number(), e)
            else:
                remove(filename)
        else:
            files_after = listdir()
            try:
                filename = str([i for i in files_after if i not in files_before][0])
            except IndexError:  #Dowloading Failed
                await bot.delete_messages(None, msg)
                await bot.send_message(userid, uploading_unsuccessful, parse_mode = 'html')
            except Exception as e:
                print(line_number(), e)
            else:   #File Downloaded Successfully
                global n_msg
                n_msg = await bot.edit_message(msg, uploading_msg, parse_mode = 'html')
                return filename
    task = False
    return None

@bot.on(events.NewMessage)
async def upload_handler(event):

    userid = event.sender_id
    message_info = event.message
    url = message_info.text
    
    if message_info.media:  #Verifying Url And File Media
        if not search_user_in_community(userid):
            await event.respond(not_joined_community, parse_mode = 'html', buttons = [Button.url('Join our Channel.','https://t.me/AJBotVerse'), Button.url('Join our Group.','https://t.me/AJBotVerseGroup')])
        else:
            login_detail = getting_email_pass(userid)
            if login_detail:
                email, password = login_detail  #Getting Login Details
                login_instance = Login(email, password)
                if login_instance.result:
                    log_object = login_instance.log
                    global task
                    if task:
                        await event.respond(task_ongoing, parse_mode = 'html')
                    else:
                        task = True
                        global process_msg
                        if url: #For Url
                            process_msg = await event.respond(processing_url, parse_mode = 'html')
                            if match('^https://(www.)?youtu(.)?be(.com)?/(.*)', url):   #For Youtube Video
                                return await youtube_downloader(userid, event, url, log_object)
                            else:   #Normal Url
                                filename = await url_downloader(userid, event, str(url))
                        else:   #Telegram File
                            process_msg = await event.respond(processing_file, parse_mode = 'html')
                            filename = await file_downloader(userid, event, message_info)
                        if filename:    #Uploading File
                            upload = Upload(filename, log_object)
                            if upload.result:   #Successfully Uploaded
                                await bot.delete_messages(None, n_msg)
                                await bot.send_message(userid, successful_uploaded, parse_mode = 'html')
                            else:   #Not Uploaded
                                await bot.delete_messages(None, n_msg)
                                await bot.send_message(userid, uploading_unsuccessful, parse_mode = 'html')
                else:   #Login Detail is Changed
                    await event.respond(login_detail_changed, parse_mode = 'html')
            else:   #Not Logged in
                await event.respond(not_loggin, parse_mode = 'html')
    return None


'''Bot is Started to run all time'''
print('Bot is Started!')
bot.start()
bot.run_until_disconnected()