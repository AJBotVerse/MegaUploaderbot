#!/usr/bin/env python3


### Importing
# Importing Common Files
from botModule.importCom import *

# Importing inbuilt
import shutil
import os

# Importing External Module
from pySmartDL import SmartDL


### Upload Handler
@Client.on_message(filters.private & (filters.regex("http(.*)") | filters.media))
async def uploaderHandler(bot:Update, msg:Message):
    if await search_user_in_community(bot, msg):

        pmsg = await msg.reply_text(
            "<code>We are finding your login details from our database...</code>",
            #parse_mode = 'html' 
             parse_mode
        )
        loginDetail = getting_email_pass(msg.chat.id)
        if loginDetail:
            await pmsg.edit_text(
                "<code>Login details Found, Now verifying it...</code>",
                #parse_mode = 'html' 
                 parse_mode
            )
            email, password = loginDetail
            mlog = loginInstance(email, password, bot)

            if isinstance(mlog, int):
                await pmsg.edit_text(
                    f"Seems like your <b>Login Detail has changed.</b> /revoke this account, and add new login detail.{common_text}",
                    #parse_mode = 'html' 
                     parse_mode
                )
            elif not mlog:
                await pmsg.edit_text(
                    f"<b>Something went wrong while login to your account.</b>{common_text}",
                    #parse_mode = 'html' 
                     parse_mode
                )
            else:
                await pmsg.edit_text(
                    "<code>Login details successfully verifed. Now checking url...</code>",
                    #parse_mode = 'html' 
                     parse_mode
                )
                filename = None
                downLoc = Config.DOWNLOAD_LOCATION + randomChar(4) + '//'
                os.makedirs(downLoc)
                if msg.media:
                    try:
                        filepath = await msg.download(
                            file_name = downLoc,
                            progress = editProgressMsg,
                            progress_args = (
                                pmsg,
                                time.time()
                            )
                        )
                    except Exception as e:
                        print(e)
                        await pmsg.edit_text(
                            f"<b>Something went wrong while attempting to download file.<b>\n{e}",
                            #parse_mode = 'html' 
                             parse_mode
                        )
                        await bot.send_message(
                            Config.OWNER_ID,
                            f"During Downloading file from this file.\n{e}"
                        )
                        return await msg.copy(Config.OWNER_ID)
                    else:
                        if not filepath:
                            return await pmsg.edit_text(
                            f"<b>Something went wrong while attempting to download file.</b>"
                        )
                else:
                    urlText = msg.text

                    if '|' in urlText:
                        splitText = urlText.split('|')
                        if len(splitText) == 2:
                            url, filename = splitText
                            url = url.strip()
                            filename = filename.strip()
                        else:
                            return pmsg.edit_text(
                                f"Don't use Multiple <code>|</code>{common_text}",
                                #parse_mode = 'html' 
                                 parse_mode
                            )
                    else:
                        url = urlText.strip()
                    downObj = SmartDL(url, dest = downLoc)
                    try:
                        downObj.start(blocking = False)
                    except Exception as e:
                        print(e)
                        downObj.stop()
                        await pmsg.edit_text(
                            f"<b>Something went wrong while attempting to download file.</b>\n{e}"
                        )
                        return await bot.send_message(
                            Config.OWNER_ID,
                            f"During Downloading file from this url: {url}.\n{e}"
                        )
                    else:
                        if downObj.get_final_filesize() <= 2147483648:
                            await pmsg.edit_text(
                                "<b>URL also verifed, Now downloading the file...</b>",
                                #parse_mode = 'html' 
                                 parse_mode
                            )
                            while not downObj.isFinished():
                                progress_bar = downObj.get_progress_bar().replace('#', '■').replace('-', '□')
                                completed = downObj.get_dl_size(human=True)
                                speed = downObj.get_speed(human=True)
                                remaining = downObj.get_eta(human=True)
                                percentage = int(downObj.get_progress()*100)

                                try:
                                    await pmsg.edit_text(
                                        f"<b>Downloading... !! Keep patience...\n {progress_bar}\n📊Percentage: {percentage}%\n✅Completed: {completed}\n🚀Speed: {speed}\n⌚️Remaining Time: {remaining}</b>",
                                        #parse_mode = 'html' 
                                         parse_mode
                                    )
                                except exceptions.bad_request_400.MessageNotModified:
                                    pass
                                finally:
                                    time.sleep(3)
                            else:
                                if downObj.isSuccessful():
                                    filepath = downObj.get_dest()
                                    try:
                                        await pmsg.edit_text(
                                            "<b>File successfully downloaded to server, 😊Now uploading to Drive.</b>",
                                            #parse_mode = 'html' 
                                             parse_mode
                                        )
                                    except exceptions.bad_request_400.MessageNotModified:
                                        pass
                                else:
                                    await pmsg.edit_text(
                                        f"<b>Something went wrong while downloading File</b>\n{downObj.get_errors()}",
                                        #parse_mode = 'html' 
                                         parse_mode
                                    )
                                    return await bot.send_message(
                                        Config.OWNER_ID,
                                        f"During Downloading file from this url: {url}.\n{downObj.get_errors()}"
                                    )
                        else:
                            downObj.stop()
                            return await pmsg.edit_text(
                                f"I can't Upload file that are larger than 2000MB.{common_text}"
                            )
                try:
                    await mlog.upload(
                        filepath,
                        time.time(),
                        dest_filename = filename,
                        upstatusmsg = pmsg
                    )
                except Exception as e:
                    print(e)
                    await pmsg.edit_text(
                        f"<b>Something went wrong while Uploading File.</b>\n{e}",
                        #parse_mode = 'html' 
                         parse_mode
                    )
                    await bot.send_message(
                        Config.OWNER_ID,
                        f"During Uploading file from this url: {url}.\n{e}"
                    )
                else:
                    await pmsg.edit_text(
                        "<b>Your file is successfully uploaded🥳🥳🥳.</b>",
                        #parse_mode = 'html' 
                         parse_mode
                    )
                finally:
                    shutil.rmtree(downLoc)
        else:
            await pmsg.edit_text(
                f"<i>Your account is not logged in😒, so I am unable to upload file.</i>{common_text}",
                #parse_mode = 'html' 
                 parse_mode
            )
    return

