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
            "We are finding your login details from our database.",
            parse_mode = 'html'
        )
        loginDetail = getting_email_pass(msg.chat.id)
        if loginDetail:
            await pmsg.edit_text(
                "Login details Found, Now verifying it.",
                parse_mode = 'html'
            )
            email, password = loginDetail
            mlog = loginInstance(email, password, bot)

            if isinstance(mlog, int):
                await pmsg.edit_text(
                    "Seems like login details is changed.",
                    parse_mode = 'html'
                )
            elif not mlog:
                await pmsg.edit_text(
                    "Something went wrong while login to your account.",
                    parse_mode = 'html'
                )
            else:
                await pmsg.edit_text(
                    "Login details successfully verifed. Now checking url.",
                    parse_mode = 'html'
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
                        return await pmsg.edit_text(
                            f"Something went wrong while attempting to download file.\n{e}"
                        )
                    else:
                        if not filepath:
                            return await pmsg.edit_text(
                            f"Something went wrong while attempting to download file.\n"
                        )
                        print(os.path.basename(filepath))
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
                                "Multiple <code>|</code>",
                                parse_mode = 'html'
                            )
                    else:
                        url = urlText.strip()
                    downObj = SmartDL(url, dest = downLoc)
                    try:
                        downObj.start(blocking = False)
                    except Exception as e:
                        print(e)
                        downObj.stop()
                        return await pmsg.edit_text(
                            f"Something went wrong while attempting to download file.\n{e}"
                        )
                    else:
                        if downObj.get_final_filesize() <= 2147483648:
                            await pmsg.edit_text(
                                "Url also verifed, Now downloading the file",
                                parse_mode = 'html'
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
                                        parse_mode = 'html'
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
                                            "BotMessage.uploading_msg",
                                            parse_mode = 'html'
                                        )
                                    except exceptions.bad_request_400.MessageNotModified:
                                        pass
                                else:
                                    return await pmsg.edit_text(
                                        "Something went wrong while downloading File",
                                        parse_mode = 'html'
                                    )
                        else:
                            downObj.stop()
                            return await pmsg.edit_text(
                                "File size is more than limit."
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
                        "Something went wrong while Uploading File.",
                        parse_mode = 'html'
                    )
                else:
                    await pmsg.edit_text(
                        "File successfully Uploaded.",
                        parse_mode = 'html'
                    )
                finally:
                    shutil.rmtree(downLoc)
        else:
            await pmsg.edit_text(
                "You are not logged in.",
                parse_mode = 'html'
            )
    return

