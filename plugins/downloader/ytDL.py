# !/usr/bin/env python3


"""Importing"""
# Importing External Packages
from pytube import YouTube, exceptions
from telethon import events, Button

# Importing Required developer defined data
from plugins.upload import *
from plugins.downloader.downloadingData import *
from bot.botMessages import ytVideoUnavailable, choose_quality, all_above_limit


class YTDown:

    def __init__(self, event, process_msg, bot, url, log_object):
        self.bot = bot
        self.process_msg = process_msg
        self.event = event
        self.url = url
        self.log_obj = log_object

    async def start(self):
        try:
            yt = YouTube(self.url)
            qualities = yt.streams.filter(progressive = True)   #Filtering Streams Having Audio & Video
        except exceptions.VideoUnavailable:
            task("No Task")
            await self.bot.edit_message(self.process_msg, ytVideoUnavailable, parse_mode = 'html')
        except Exception as e:
            task("No Task")
            await self.bot.send_message(dev, f'In downloader.py {line_number()} {e}')
            await self.bot.edit_message(self.process_msg, unsuccessful_upload, parse_mode = 'html')
        else:
            #Creating Buttons for Selecting Quality
            quality_button = [Button.inline(f'{quality.resolution}, {int(quality.filesize/1048576)}mb', quality.itag) for quality in qualities if quality.filesize <= 419430400]
            task("No Task")
            if quality_button:
                msg = await self.bot.edit_message(self.process_msg, choose_quality, parse_mode = 'html', buttons = quality_button)
                
                #CallBackQuery For Youtube Video Uploader
                @self.bot.on(events.CallbackQuery)
                async def Youtube_Video_CallBack(event):
                    if task() == "No Task":
                        task("Running")

                        #Getting String Value From event.data
                        itag = event.data.decode('utf-8')
                        files_before = listdir(downloadFolder)
                        stream = yt.streams.get_by_itag(itag)

                        #Trying To Download Video To Server
                        await self.bot.edit_message(msg, starting_to_download, parse_mode = 'html')
                        try:
                            stream.download(output_path = downloadFolder)
                        except Exception as e:
                            task("No Task")
                            files_after = listdir(downloadFolder)
                            await self.bot.send_message(dev, f'In downloader.py {line_number()} {e}')
                            await self.bot.edit_message(msg, unsuccessful_upload, parse_mode = 'html')
                            try:
                                filename = str([i for i in files_after if i not in files_before][0])
                            except IndexError:
                                pass
                            else:
                                #Deleting Incomplete File
                                remove(f'{downloadFolder}{filename}')
                        else:
                            files_after = listdir(downloadFolder)
                            try:
                                filename = str([i for i in files_after if i not in files_before][0])
                            except IndexError:
                                #File Not Downloaded
                                task("No Task")
                                await self.bot.edit_message(msg, unsuccessful_upload, parse_mode = 'html')
                            else:
                                #File Downloaded Successfully to Server
                                n_msg = await self.bot.edit_message(msg, uploading_msg, parse_mode = 'html')
                                self.n_msg, self.filename = n_msg, filename
                                await Upload.start(filename, self.log_obj, self.bot, msg, event.sender_id)
                                return True
                    else:
                        await self.bot.edit_message(msg, task_ongoing, parse_mode = 'html')
            else:
                await self.bot.edit_message(self.process_msg, all_above_limit, parse_mode = 'html')