'''Some permanent Variables defined'''

dev = 1972357814

downloadFolder = '/app/download/'
# downloadFolder = 'D:\Projects\Public\MegaUploaderbot\download\\'

common_text = "\n\n<u>If you are facing any problem, so report at @AJPyroVerseGroup</u>"

to_login = "<i>If you are not logged in then, send login detail in this format email,password.</i>\n"

start_msg = f"<b>Hi, I am MegaUploaderBot Created by @AJPyroVerse and My Developer is @AJTimePyro.</b>\n\nI support:-\n<i>1.</i> <u>Direct Downloading Link</u>\n<i>2.</i> <u>Telegram File</u>\n<i>3.</i> <u>Youtube URL</u>\n\n\n{to_login}\nWe will store your login detail on our database.{common_text}"

help_msg = f"{to_login}\nAfter login send Direct Downloading Link, Youtube URL or any Telegram File.\n\nTo remove your account from Database use /revoke.{common_text}"

trying_to_login = "I am trying to login your account.\nSo Please Wait..."

logged_in = "<b>Congratulations</b>, <i>Your account is successfully logged in.</i>"

invalid_login = f"<b>Please provide a valid login detail.</b>{common_text}"

revoke_failed = f"<u>You are not even logged in. So how can I remove your account.</u>{common_text}"

logged_out = "Your account is now logged out.\nTo Login again send your login detail."

already_login = "<b>Your account is already login.</b>"

not_joined_community = f'<b>To use this bot, you need to Join our channel and Group.</b>{common_text}'

not_loggin = f"<i>Your account is not logged in so I am unable to upload file.</i>{common_text}"

login_detail_changed = f"Seems like your <b>login detail is changed.</b> /revoke this account, and add new login detail.{common_text}"

file_limit = f"Send only those whose size is less than 400mb.{common_text}"

starting_to_download = "<i>Starting to Upload the file.... Have Some Patience!!!</i>"

unsuccessful_upload = f"Uploading went <b>unsuccessful</b>, maybe url has problem.{common_text}"

uploading_msg = '<b>File successfully downloaded to server, Now uploading to Drive.</b>'

successful_uploaded = "<b>Your file is successfully uploaded.</b>"

uploading_unsuccessful = f'Uploading went <b>unsuccessful</b>, Something Went Wrong{common_text}'

broadcast_failed = '<b>Broadcasting Message can`t be empty</b>'

choose_quality = '<i>Choose Which Video Quality you want to Upload</i>'

all_above_limit = 'Sorry, No Quality Found Under Limit'

processing_url = '<i>Please wait while I am Processing Url</i>'

processing_file = '<i>Please wait while I am Processing File</i>'

task_ongoing = '<u>One Task is already going on, So Please Try Again Later.</u>'

ytVideoUnavailable = '<b>Youtube Video is unavailable.<b>'
