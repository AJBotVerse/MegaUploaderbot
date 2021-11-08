#!/usr/bin/env python3


"""Importing"""
# Importing External Packages
from pytube import YouTube
from pyrogram.types import CallbackQuery
from ffmpeg import input, concat

# Importing Inbuilt packages
from shutil import rmtree
from uuid import uuid4
from time import time
from os import makedirs, path

# Importing Common Files
from botModule.importCommon import *

# Importing Developer defined modules
from helper.uploader import *
from helper.login import *


"""Some Global Variable"""
listTask = ['']
global counter
counter = 0
fileName = 'callbackYTDL'


@Client.on_callback_query()
async def Youtube_Video_CallBack(bot:Update, callback_query:CallbackQuery):
    itag, url = eval(callback_query.data)

    global counter
    counter += 1
    listTask.append(YTDownloadCallback(callback_query, itag, url, bot))
    bot.loop.create_task(listTask[counter].start())
    return


class YTDownloadCallback:

    def __init__(self, callback_query, itag, url, bot):
        self.callback = callback_query
        self.user = self.callback.from_user
        self.userid = self.user.id
        self.itag = itag
        self.url = url
        self.bot = bot

        self.slash = '//' if '/'in Config.DOWNLOAD_LOCATION else '\\'
        self.Downloadfolder = Config.DOWNLOAD_LOCATION + self.slash + str(uuid4())
        self.videoFolder = f'{self.Downloadfolder}{self.slash}video'
        self.audioFolder = f'{self.Downloadfolder}{self.slash}audio'

        self.__creatingFolder()
        return

    def __creatingFolder(self):
        makedirs(self.Downloadfolder)
        makedirs(self.videoFolder)
        makedirs(self.audioFolder)

    async def start(self):

        self.log_obj = await self.getLogin()

        if self.log_obj:
            # async def edit_msg(progress_bar, percentage, completed, speed, remaining):
            #     try:
            #         self.msg = await self.msg.edit_text(f"<b>Downloading... !! Keep patience...\n [ {progress_bar}]\n📊Percentage: {percentage}%\n✅Completed: {completed} MB\n🚀Speed: {speed} MB/s\n⌚️Remaining Time: {remaining} seconds</b>", parse_mode = 'html')
            #     except exceptions.bad_request_400.MessageNotModified:
            #         pass
            #     except exceptions.bad_request_400.MessageIdInvalid:
            #         pass

            # # Progress bar function
            # def progressBar(stream, _chunk, bytes_remaining):
            #     filesize = stream.filesize
            #     completed = round(((filesize - bytes_remaining)/1024)/1024, 1)
            #     current = (stream.filesize - bytes_remaining)/stream.filesize
            #     percentage = int(current*100)
            #     progress = int(18*current)
            #     progress_bar = '■' * progress + '□' * (18 - progress)
            #     time_taken = int(time()) - t1
            #     speed = round(completed/time_taken, 2)
            #     if speed == 0:
            #         speed = 0.1
            #     remaining = int(((bytes_remaining/1024)/1024)/speed)
                
            #     self.bot.loop.create_task(edit_msg(progress_bar, percentage, completed, speed, remaining))

            self.msg = await self.callback.edit_message_text(BotMessage.starting_to_download, parse_mode = 'html')
            try:
                # self.yt = YouTube(self.url, on_progress_callback = progressBar)
                yt = YouTube(self.url)
                stream = self.yt.streams.get_by_itag(self.itag)
                t1 = time()
                self.videoFilepath = stream.download(output_path = self.videoFolder)
                self.filename = str(path.basename(self.videoFilepath))
                if not await self.__downloadingAudio():
                    return
            except Exception as e:
                await self.errorMsg(e)
                return
            else:
                pass
                if self.filename:
                    self.Uploader = Upload(self.filename, self.log_obj, self.bot, self.userid, self.Downloadfolder, self.msg, self.slash)
                    await self.Uploader.start()
                else:
                    await self.errorMsg()
            finally:
                return
        else:
            rmtree(self.Downloadfolder, ignore_errors = True)
            return
        
    async def errorMsg(self, e = ''):

        await self.bot.send_message(Config.OWNER_ID, f'{line_number(fileName, e)}\n\n{self.url}')
        await self.callback.edit_message_text(BotMessage.unsuccessful_upload, parse_mode = 'html')
        rmtree(self.Downloadfolder, ignore_errors = True)
        return

    async def getLogin(self):
        login_detail = getting_email_pass(self.userid)
        if login_detail:
            email, password = login_detail  #Getting Login Details
            login_instance = Login(email, password)
            if login_instance.result:
                return login_instance.log
            else:   #Login Detail is Changed
                await self.callback.edit_message_text(BotMessage.login_detail_changed, parse_mode = 'html')
        else:   #Not Logged in
            await self.callback.edit_message_text(BotMessage.not_loggin, parse_mode = 'html')
        return

    async def __downloadingAudio(self):
        try:
            qualities = self.yt.streams.filter(only_audio = True, adaptive = True)
            listAudio = {quality.abr[:-4] : quality.itag for quality in qualities}
            sizeA = (int(i) for i in listAudio)
            stream = self.yt.streams.get_by_itag(listAudio[f'{max(sizeA)}'])
            self.audioFilepath = stream.download(output_path = self.audioFolder)
        except Exception as e:
            await self.errorMsg(e)
        else:
            if self.audioFilepath:
                if await self.merge():
                    return True
            else:
                await self.errorMsg()
        return
    
    async def merge(self):
        try:
            inputVideo = input(self.videoFilepath)
            inputAudio = input(self.audioFilepath)
            concat(inputVideo, inputAudio, v = 1, a = 1).output(f'{self.Downloadfolder}{self.slash}{self.filename}').run()
        except Exception as e:
            await self.errorMsg(e)
            return
        else:
            return True
        finally:
            rmtree(self.videoFolder, ignore_errors = True)
            rmtree(self.audioFolder, ignore_errors = True)

