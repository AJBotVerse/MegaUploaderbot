# !/usr/bin/env python3


"""Importing"""
# Importing External Packages
from pytube import YouTube, exceptions
from telethon import events, Button

# Importing Inbuilt packages
import asyncio

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

        #Editing Progress Bar
        async def edit_msg(progress_bar, percentage, completed, speed, remaining):
            self.msg = await self.bot.edit_message(self.msg, f"<b>Downloading... !! Keep patience...\n [ {progress_bar}]\n📊Percentage: {percentage}%\n✅Completed: {completed} MB\n🚀Speed: {speed} MB/s\n⌚️Remaining Time: {remaining} seconds</b>", parse_mode = 'html')

        #Progress bar function
        def progress_function(stream, _chunk, bytes_remaining):
            filesize = stream.filesize
            completed = round(((filesize - bytes_remaining)/1024)/1024, 1)
            current = (stream.filesize - bytes_remaining)/stream.filesize
            percentage = int(current*100)
            progress = int(18*current)
            progress_bar = '■' * progress + '□' * (18 - progress)
            time_taken = int(time()) - t1
            speed = round(completed/time_taken, 2)
            if speed == 0:
                speed = 0.1
            remaining = int(((bytes_remaining/1024)/1024)/speed)
            self.bot.loop.create_task(edit_msg(progress_bar, percentage, completed, speed, remaining))
        try:
            self.yt = YouTube(self.url, on_progress_callback = progress_function)
            self.qualities = self.yt.streams.filter(progressive = True)   #Filtering Streams Having Audio & Video
        except exceptions.VideoUnavailable: #Video not found
            task("No Task")
            await self.bot.edit_message(self.process_msg, ytVideoUnavailable, parse_mode = 'html')
        except Exception as e:
            task("No Task")
            await self.bot.send_message(dev, f'In ytDL.py {line_number()} {e}')
            await self.bot.edit_message(self.process_msg, unsuccessful_upload, parse_mode = 'html')
        else:
            #Creating Buttons for Selecting Quality
            quality_button = []
            for quality in self.qualities:
                if quality.type == "video":
                    if quality.filesize <= 419430400:
                        value = quality.resolution
                        if not value:
                            continue
                        if quality.fps == 60:
                            value += "60fps"
                        value += ',' + str(int(quality.filesize/1048576)) + 'mb'
                        quality_button.append(Button.inline(value, quality.itag))
            if quality_button:
                self.bmsg = await self.bot.edit_message(self.process_msg, choose_quality, parse_mode = 'html', buttons = quality_button)
                
                #CallBackQuery For Youtube Video Uploader
                @self.bot.on(events.CallbackQuery)
                async def Youtube_Video_CallBack(event):

                    #Getting String Value From event.data
                    itag = event.data.decode('utf-8')
                    files_before = listdir(downloadFolder)
                    stream = self.yt.streams.get_by_itag(itag)

                    #Trying To Download Video To Server
                    try:
                        self.msg = await self.bot.edit_message(self.bmsg, starting_to_download, parse_mode = 'html')
                        global t1
                        t1 = time()
                        stream.download(output_path = downloadFolder)
                    except Exception as e:
                        task("No Task")
                        files_after = listdir(downloadFolder)
                        await self.bot.send_message(dev, f'In ytDL.py {line_number()} {e}')
                        await self.bot.edit_message(self.msg, unsuccessful_upload, parse_mode = 'html')
                        try:
                            videoFile = str([i for i in files_after if i not in files_before][0])
                        except IndexError:
                            pass
                        else:
                            #Deleting Incomplete File
                            remove(f'{downloadFolder}{videoFile}')
                    else:
                        files_after = listdir(downloadFolder)
                        try:
                            videoFile = str([i for i in files_after if i not in files_before][0])
                        except IndexError:
                            #File Not Downloaded
                            task("No Task")
                            await self.bot.edit_message(self.msg, unsuccessful_upload, parse_mode = 'html')
                        else:
                            #File Downloaded Successfully to Server
                            self.videoFile = videoFile
                            n_msg = await self.bot.edit_message(self.msg, uploading_msg, parse_mode = 'html')
                            await Upload.start(self.videoFile, self.log_obj, self.bot, n_msg, event.sender_id)
                            return True
                return
            else:
                await self.bot.edit_message(self.process_msg, all_above_limit, parse_mode = 'html')