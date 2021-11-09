#!/usr/bin/env python3


# Bot defined Messages
class BotMessage(object):

    '''Some permanent Variables defined'''

    common_text = "\n\n<b><u>If you are facing any problem😫, so report📝 at @AJPyroVerseGroup</u></b>"

    to_login = "<b>If you are not logged in then, send login detail in this format email,password.</b>\n"

    start_msg = f"<b>Hi, I am MegaUploaderBot🤖 Created by @AJPyroVerse and My Developer🧑‍💻 is @AJTimePyro.</b>\n\nAnd I support:-\n1. <u>Direct Downloading Link</u>\n2.<u>Telegram File</u>\n3. <u>Youtube URL</u>\n\n\n{to_login}\n😊We will store your login detail on our database.{common_text}"

    help_msg = f"{to_login}\n<b>After login😊 send Direct Downloading Link, Youtube URL or any Telegram File.\n\nTo remove your account from Database use /revoke.</b>{common_text}"

    userBanned = f"<b>You are Banned🚫 from AJPyroVerse Community.</b>"

    trying_to_login = "<code>I am trying to login your account.\nSo Please Wait...</code>"

    logged_in = "<b>Congratulations🥳🥳</b>, <i>Your account is successfully logged in😊.</i>"

    invalid_login = f"<b>Please provide a 😒valid login detail.</b>{common_text}"

    revoke_failed = f"<b><u>You are not even logged in😒. So how can I remove your account.</u></b>{common_text}"

    logged_out = "Your account is now logged out🥺.\nTo Login again send your login detail."

    already_login = "<b>Your account is already login🤪.</b>"

    not_joined_community = f'<b>To use this bot, you need to Join our channel and Group😁🤪.</b>{common_text}'

    not_loggin = f"<i>Your account is not logged in😒, so I am unable to upload file.</i>{common_text}"

    login_detail_changed = f"Seems like your <b>login detail is changed.</b> /revoke this account, and add new login detail.{common_text}"

    file_limit = f"I can't Upload file that are larger than 2000MB.{common_text}"

    starting_to_download = "<code>Starting to Download🚀 the file on server.... Have Some Patience!!!</code>"

    downloadingAudio = "<b>Now Downloading Audio🔉 File.</b>"

    merging = "<b>Merging Audio🔉 and Video🎥, This can take a while...</b>"

    unsuccessful_upload = f"Uploading went <b>unsuccessful</b>🥺, maybe url has problem.{common_text}"

    uploading_msg = '<b>File successfully downloaded to server, 😊Now uploading to Drive.</b>'

    successful_uploaded = "<b>Your file is successfully uploaded🥳🥳🥳.</b>"

    uploading_unsuccessful = f'Uploading went <b>unsuccessful</b>🥺, Something Went Wrong{common_text}'

    broadcast_failed = "<b>Broadcasting Message can't be empty😒</b>"

    choose_quality = '<b>Choose Which 🎥Video Quality you want to Upload.\n\nIt will automatically Deleted after 1 minute⏲️; If not selected any.</b>'

    all_above_limit = 'Sorry🥲, No Quality Found Under Limit'

    processing_url = '<code>Please wait⏳ while I am Processing Url</code>'

    processing_file = '<cpde>Please wait⏳ while I am Processing File</code>'

    ytVideoUnavailable = '<b>Youtube Video is unavailable😒.<b>'

