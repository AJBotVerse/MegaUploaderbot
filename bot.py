

'''Importing modules and library'''
from telethon import *
from mega import *
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from csv import reader, writer
from requests import head, get
from logging import basicConfig, WARNING
from os import listdir, remove
from subprocess import Popen
from credentials import *


'''For Hidden Error'''
basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',level=WARNING)


'''Mega Instance'''
mega = Mega()


'''Some permanent Variables defined'''
dev = (1116098563) #AJTimePyro
common_text = "\n\n<u>If you facing any problem, so report at @AJTimePyro</u>"
start1 = "<i>To login your account send login detail in this format email,password.</i>\n"
start_msg = f"<b>I am a Bot.</b>\n\n{start1}\nWe will store your login detail so that you don't have to login everytime you use. So provide your temporary account for your security.{common_text}"
help_msg = f"{start1}\nAfter login send direct downloading link.\n\nTo remove your account use /revoke.{common_text}"
not_joined_channel = '**To use this bot, you need to Join our channel.**'
already_login = f"<b>You are already login.</b>{common_text}"
invalid_login = f"<b>Please provide a valid login detail.</b>{common_text}"
logged_in = "**Congratulations**, __Your account is successfully logged in.__"
trying_to_login = "I am trying to login your account.\n**So Please Wait...**"
not_loggin = f"Your account is not logged in so I am unable to upload file.{common_text}"
login_detail_changed = f"Seems like your <b>login detail is changed.</b> /revoke this account. And add new login detail.{common_text}"
starting_to_download = "Starting to Upload the file.... Have Some Patience!!!"
unsuccessful_upload = f"Uploading went <b>unsuccessful</b>, maybe url has problem.{common_text}"
successful_uploaded = "Your file is **successfully uploaded**"
file_limit = "**Send only those whose size is less than 250mb.**"
revoke_failed = f"You are not even logged in. So how can I remove your account.{common_text}"
logged_out = "**Your account is now logged out from this bot.**"


'''Login as a Bot and Userbot'''
bot = TelegramClient('AJTime', api_id, api_hash).start(bot_token = bot_token)
client = TelegramClient(phone, api_id, api_hash)
client.connect()

'''Adding Functionalityto Bot!'''
#Checking whether user is joined the Channel
async def search_user_in_channel(userid):
    '''if not await client.is_user_authorized():
        await client.send_code_request(phone)
        me = await client.sign_in(phone, input('Enter code: '))'''
    users = await client.get_participants('AJBotVerse')
    for user in users:
        if str(user.id) == str(userid):
            return True
    await bot.send_message(int(userid), not_joined_channel, buttons = Button.url('Join our Channel','https://t.me/AJBotVerse'))
    return False

#Adding user who are logged in
def add_logged_in_user(userid, email, password):
    with open('userdata.csv','a') as userdata:
        writer1 = writer(userdata)
        writer1.writerow((userid, email, password))
        return None

#Check User that is he logged in or not
def searchuserid(userid):
    with open('userdata.csv','r') as udata:
        csv_reader = reader(udata)
        for uid in csv_reader:
            if uid[0] == userid:
                return (uid[1], uid[2])
        else:
            return None

#Sending msg to user that his login detail is invalid
async def invalid(event, message):
    await bot.edit_message(message, invalid_login, parse_mode = 'html')
    userid = str(event.sender_id)
    return None

#it will check the length of file
async def length_of_file(event, url):
    try:
        h = head(url, allow_redirects=True)
        header = h.headers
        content_length = int(header.get('content-length'))
        file_length = round((content_length/1048576),3)
        lenres = content_length > 262144000
        userid = str(event.sender_id)
        if lenres:
            await event.respond((f'This filesize is **{file_length}mb**. {file_limit}'))
            return False
        else:
            return True
    except Exception as e:
        print(e)
        return False

#Start Handler
@bot.on(events.NewMessage(pattern = r'/start'))
async def start_handler(event):
    if event.message.text == '/start':
        userid = event.sender_id
        if await search_user_in_channel(userid):
            await event.respond(start_msg, parse_mode = 'html')
    return None

#Help Handler
@bot.on(events.NewMessage(pattern = r'/help'))
async def help_handler(event):
    if event.message.text == '/help':
        userid = event.sender_id
        if await search_user_in_channel(str(userid)):
            await event.respond(help_msg, parse_mode = 'html')
            data = f'{userid} used the help command\n'
    return None

#It will download file for uploading the file, if needed
@bot.on(events.NewMessage(pattern = r'http'))
async def download_handler(event):
    userid = str(event.sender_id)
    search_result = searchuserid(userid)
    if await search_user_in_channel(userid):
        if search_result == None:
            await event.respond(not_loggin, parse_mode = 'html')
            return None
        else:
            email, password = search_result
            try:
                mlog = mega.login(email, password)
            except:
                await event.respond(login_detail_changed, parse_mode = 'html')
                return None
    
        #If url is of mega
        url = str(event.message.text)
        if r'https://mega.nz' in url or r'https://mega.co.nz' in url:
            try:
                message = await event.respond(starting_to_download)
                mlog.import_public_url(url)
            except Exception as e:
                await bot.edit_message(message, unsuccessful_upload, parse_mode = 'html')
                print(e)
                return None
            else:
                await bot.edit_message(message, successful_uploaded)
                return None
    
        #Url is not of mega
        else:
            if await length_of_file(event ,url):
                try:
                    files_before = listdir()
                    message = await event.respond(starting_to_download)
                    output = Popen(['wget', url])
                    output.wait()
                except Exception as e:
                    await bot.edit_message(message, unsuccessful_upload, parse_mode = 'html')
                    print(e)
                    files_after = listdir()
                    filename = str([i for i in files_after if i not in files_before][0])
                    remove(filename)
                    return None
                else:
                    files_after = listdir()
                    try:
                        filename = str([i for i in files_after if i not in files_before][0])
                    except Exception as e:
                        await bot.edit_message(message, unsuccessful_upload, parse_mode = 'html')
                        print(e)
                        return None
                    else:
                        if 'html' in filename:
                            remove(filename)
                            await bot.edit_message(message, unsuccessful_upload, parse_mode = 'html')
                            return None
                        else:
                            await upload(event, filename , mlog, userid, message)
                            return None
            else:
                await event.respond(unsuccessful_upload, parse_mode = 'html')
    return None

#it will try to upload the file to mega
async def upload(event, filename , mlog, userid, message):
    try:
        mlog.upload(filename)
    except:
        await event.respond(unsuccessful_upload, parse_mode = 'html')
        remove(filename)
    else:
        await bot.edit_message(message, successful_uploaded)
        remove(filename)
    return None

#Login the user
@bot.on(events.NewMessage(pattern = "(.*),(.*)"))
async def login_handler(event):
    userid = str(event.sender_id)
    if await search_user_in_channel(userid):
        userid = str(event.sender_id)
        search_result = searchuserid(userid)
        if search_result != None:
            await event.respond(already_login, parse_mode = 'html')
            return None
        else:
            try:
                email, password = str(event.message.text).split(',')
            except Exception as e:
                print(e)
                await event.respond(invalid_login, parse_mode = 'html')
                return None
            else:
                if r'@' not in email or len(password)<8:
                    await invalid(event, message)
                    return None
                else:
                    message = await bot.send_message(int(userid), trying_to_login)
                    try:
                        mlog = mega.login(email, password)
                    except:
                        await invalid(event, message)
                        return None
                    else:
                        await bot.edit_message(message, logged_in)
                        add_logged_in_user(userid, email, password)
    return None

#it will remove user
@bot.on(events.NewMessage(pattern = r'/revoke'))
async def logging_out_handler(event):
    if event.message.text == '/revoke':
        userid = str(event.sender_id)
        login_detail = searchuserid(userid)
        if login_detail == None:
            await event.respond(revoke_failed, parse_mode = 'html')
            return None
        else:
            with open('userdata.csv','r') as userdata:
                lstdata = []
                reader1 = reader(userdata)
                for data in reader1:
                    if data[0] != userid:
                        lstdata.append(data)
            with open('userdata.csv','w') as userdata:
                writer1 = writer(userdata)
                for data in lstdata:
                    writer1.writerow(data)
            await event.respond(logged_out)
    return None

@bot.on(events.NewMessage)
async def file_handler(event):
    userid = str(event.sender_id)
    file_info = event.message
    if file_info.media:
        if await search_user_in_channel(userid):
            userid = str(event.sender_id)
            search_result = searchuserid(userid)
            if search_result == None:
                await event.respond(not_loggin, parse_mode = 'html')
                return None
            else:
                email, password = search_result
                try:
                    mlog = mega.login(email, password)
                except Exception as e:
                    await event.respond(login_detail_changed, parse_mode = 'html')
                    print(e)
                    return None
            
            size_of_file = file_info.file.size/1024
            if int(file_info.file.size) > 262144000:
                await event.respond((f'This filesize is **{size_of_file}mb**. {file_limit}'))
                return None
            else:
                try:
                    files_before = listdir()
                    message = await event.respond(starting_to_download)
                    await event.download_media()
                except Exception as e:
                    await bot.edit_message(message,  '**Something Went Wrong, Try again Later**')
                    print(e)
                    files_after = listdir()
                    try:
                        filename = str([i for i in files_after if i not in files_before][0])
                    except Exception as e:
                        print(e)
                    else:
                        remove(filename)
                else:
                    files_after = listdir()
                    try:
                        filename = str([i for i in files_after if i not in files_before][0])
                    except Exception as e:
                        await bot.edit_message(message,  '**Something Went Wrong, Try again Later**')
                        print(e)
                    else:
                        await upload(event, filename , mlog, userid, message)
    return None


'''Bot is Started to run all time'''
print('Bot is Started!')
bot.start()
bot.run_until_disconnected()