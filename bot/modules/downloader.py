#!/usr/bin/env python3


"""Importing"""
# Importing External Packages
from telethon import Button, events
from pytube import YouTube, exceptions
from pySmartDL import SmartDL

# Importing Inbuilt packages
from os import listdir, remove, path
from re import match
from time import sleep

# Importing Credentials & Developer defined modules
from bot.modules.funcs import *
from bot.modules.upload import *
from bot.perma_var import *


"""Downloader Class"""
class Downloader:

    def __init__(self, event, message_info, bot):
        self.event = event
        self.message_info = message_info
        self.bot = bot
    
    @classmethod
    async def start(cls, event, message_info, bot, log_object):
        self = cls(event, message_info, bot)
        if message_info.file:  #For Telegram File/media
            process_msg = await event.respond(processing_file, parse_mode = 'html')
            await self.file_downloader(self.event, process_msg, self.bot, message_info)
        else:
            url = message_info.text
            process_msg = await event.respond(processing_url, parse_mode = 'html')
            if match('^https://(www.)?youtu(.)?be(.com)?/(.*)', url):   #For Youtube Video
                await self.youtube_downloader(process_msg, self.bot, url, log_object)
            else:   #Normal Url
                await self.url_downloader(self.event, process_msg, self.bot, url)
        return self

    #Downloading Youtube Video
    async def youtube_downloader(self, process_msg, bot, url, log_obj):
        try:
            yt = YouTube(url)
            qualities = yt.streams.filter(progressive = True)   #Filtering Streams Having Audio & Video
        except exceptions.VideoUnavailable:
            task("No Task")
            await bot.edit_message(process_msg, ytVideoUnavailable, parse_mode = 'html')
        except Exception as e:
            task("No Task")
            print(line_number(), e)
            await bot.edit_message(process_msg, unsuccessful_upload, parse_mode = 'html')
        else:
            #Creating Buttons for Selecting Quality
            quality_button = [Button.inline(f'{quality.resolution}, {int(quality.filesize/1048576)}mb', quality.itag) for quality in qualities if quality.filesize <= 419430400]
            task("No Task")
            if quality_button:
                msg = await bot.edit_message(process_msg, choose_quality, parse_mode = 'html', buttons = quality_button)
                
                #CallBackQuery For Youtube Video Uploader
                @bot.on(events.CallbackQuery)
                async def Youtube_Video_CallBack(event):
                    if task() == "No Task":
                        task("Running")

                        #Getting String Value From event.data
                        itag = event.data.decode('utf-8')
                        files_before = listdir(downloadFolder)
                        stream = yt.streams.get_by_itag(itag)

                        #Trying To Download Video To Server
                        await bot.edit_message(msg, starting_to_download, parse_mode = 'html')
                        try:
                            stream.download(output_path = downloadFolder)
                        except Exception as e:
                            task("No Task")
                            files_after = listdir(downloadFolder)
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
                                remove(f'{downloadFolder}{filename}')
                        else:
                            files_after = listdir(downloadFolder)
                            try:
                                filename = str([i for i in files_after if i not in files_before][0])
                                print(filename)
                            except IndexError:
                                #File Not Downloaded
                                task("No Task")
                                await bot.edit_message(msg, unsuccessful_upload, parse_mode = 'html')
                            else:
                                #File Downloaded Successfully to Server
                                n_msg = await bot.edit_message(msg, uploading_msg, parse_mode = 'html')
                                self.n_msg, self.filename = n_msg, filename
                                await Upload.start(filename, log_obj, bot, msg, event.sender_id)
                                return True
                    else:
                        await bot.edit_message(msg, task_ongoing, parse_mode = 'html')
            else:
                await bot.edit_message(process_msg, all_above_limit, parse_mode = 'html')
        self.filename = None
        return None


    #Downloading From url
    async def url_downloader(self, event, process_msg, bot, url):
        task("Running")

        len_file = await length_of_file(url)
        if len_file == 'Valid':
            msg = await bot.edit_message(process_msg, starting_to_download, parse_mode = 'html')
            userid = event.sender_id
            downObj = SmartDL(url, dest = downloadFolder)
            downObj.start(blocking = False)
            while not downObj.isFinished():
                progress_bar = downObj.get_progress_bar().replace('#', '■').replace('-', '□')
                completed = downObj.get_dl_size(human=True)
                speed = downObj.get_speed(human=True)
                remaining = downObj.get_eta(human=True)
                percentage = int(downObj.get_progress()*100)
                msg = await bot.edit_message(msg, f"<b>Downloading... !! Keep patience...\n {progress_bar}\n📊Percentage: {percentage}\n✅Completed: {completed}\n🚀Speed: {speed}\n⌚️Remaining Time: {remaining}</b>", parse_mode = 'html')
                sleep(1)
            print('downloading done')
            try:
                filename = path.basename(downObj.get_dest())
                print(1)
            except Exception as e:
                print(line_number(), e)
            if downObj.isSuccessful():
                n_msg = await bot.edit_message(msg, uploading_msg, parse_mode = 'html')
                self.n_msg, self.filename = n_msg, filename
                return True
            else:
                task("No Task")
                try:
                    remove(f'{downloadFolder}{filename}')
                except Exception as e:
                    print(line_number(), e)
                await bot.delete_messages(None, msg)
                await bot.send_message(userid, unsuccessful_upload, parse_mode = 'html')
                for e in downObj.get_errors():
                    print(line_number(), str(e))

        elif len_file == 'Not Valid':
            await bot.edit_message(process_msg, unsuccessful_upload, parse_mode = 'html')
        else:
            await bot.edit_message(process_msg, f'This filesize is **{len_file}mb**. {file_limit}', parse_mode = 'html')
        self.filename = None
        task("No Task")
        return None


    #Downloading From Telegram File/Media
    async def file_downloader(self, event, process_msg, bot, message_info):
        task("Running")
        
        size_of_file = message_info.file.size/1024  #Getting Size of File
        if int(message_info.file.size) >= 419430400:    #File Size is more than Limit
            await bot.edit_message(process_msg, f'This filesize is {size_of_file}mb. {file_limit}', parse_mode = 'html')
        else:
            userid = event.sender_id
            try:
                files_before = listdir(downloadFolder)
                msg = await bot.edit_message(process_msg, starting_to_download, parse_mode = 'html')

                #Trying to Download File to Server
                await bot.download_media(message_info, file = downloadFolder)
            except Exception as e:  #Downlading Failed
                task("No Task")
                await bot.delete_messages(None, msg)
                await bot.send_message(userid, uploading_unsuccessful, parse_mode = 'html')
                print(line_number(), e)
                files_after = listdir(downloadFolder)
                try:
                    filename = str([i for i in files_after if i not in files_before][0])
                except IndexError:
                    pass
                except Exception as e:
                    print(line_number(), e)
                else:
                    remove(f'{downloadFolder}{filename}')
            else:
                files_after = listdir(downloadFolder)
                try:
                    filename = str([i for i in files_after if i not in files_before][0])
                except IndexError:  #Dowloading Failed
                    task("No Task")
                    await bot.delete_messages(None, msg)
                    await bot.send_message(userid, uploading_unsuccessful, parse_mode = 'html')
                except Exception as e:
                    task("No Task")
                    print(line_number(), e)
                else:   #File Downloaded Successfully
                    n_msg = await bot.edit_message(msg, uploading_msg, parse_mode = 'html')
                    self.n_msg, self.filename = n_msg, filename
                    return True
        self.filename = None
        task("No Task")
        return None