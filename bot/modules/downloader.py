
from telethon import Button, events
from pytube import YouTube
from os import listdir, remove
from subprocess import Popen
from re import match
from bot.modules.funcs import *
from bot.modules.upload import *
from bot.perma_var import *

class Downloader:

    def __init__(self, event, message_info, bot):
        self.event = event
        self.message_info = message_info
        self.bot = bot
    
    @classmethod
    async def start(cls, event, message_info, bot, log_object):
        self = cls(event, message_info, bot)
        url = message_info.text
        if url: #For Url
            process_msg = await event.respond(processing_url, parse_mode = 'html')
            if match('^https://(www.)?youtu(.)?be(.com)?/(.*)', url):   #For Youtube Video
                filename = await self.youtube_downloader(self.event, process_msg, self.bot, url, log_object)
            else:   #Normal Url
                filename = await self.url_downloader(self.event, process_msg, self.bot, url)
        else:   #Telegram File
            process_msg = await event.respond(processing_file, parse_mode = 'html')
            filename = await self.file_downloader(self.event, process_msg, self.bot, message_info)
        return self

    #Downloading Youtube Video
    async def youtube_downloader(self, event, process_msg, bot, url, log_obj):
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
                            # global n_msg
                            n_msg = await bot.edit_message(msg, uploading_msg, parse_mode = 'html')
                            self.n_msg, self.filename = n_msg, filename
                            await Upload.start(filename, log_obj, bot, msg, event.sender_id)
                            return True
            else:
                task = False
                await bot.edit_message(process_msg, all_above_limit, parse_mode = 'html')
        self.filename = None
        return None


    #Downloading From url
    async def url_downloader(self, event, process_msg, bot, url):
        len_file = await length_of_file(url)
        if len_file == 'Valid':
            msg = await bot.edit_message(process_msg, starting_to_download, parse_mode = 'html')
            userid = event.sender_id
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
                        # global n_msg
                        n_msg = await bot.edit_message(msg, uploading_msg, parse_mode = 'html')
                        self.n_msg, self.filename = n_msg, filename
                        return True
        elif len_file == 'Not Valid':
            await bot.edit_message(process_msg, unsuccessful_upload, parse_mode = 'html')
        else:
            await bot.edit_message(process_msg, f'This filesize is **{len_file}mb**. {file_limit}', parse_mode = 'html')
        self.filename = None
        task = False
        return None


    #Downloading From Telegram File/Media
    async def file_downloader(self, event, process_msg, bot, message_info):
        #Getting Size of File
        size_of_file = message_info.file.size/1024
        if int(message_info.file.size) >= 419430400: #File Size is more than Limit
            await bot.edit_message(process_msg, f'This filesize is {size_of_file}mb. {file_limit}', parse_mode = 'html')
        else:
            userid = event.sender_id
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
                    n_msg = await bot.edit_message(msg, uploading_msg, parse_mode = 'html')
                    self.n_msg, self.filename = n_msg, filename
                    return True
        self.filename = None
        task = False
        return None