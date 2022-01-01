#!/usr/bin/env python3


### Importing
# Importing Common Files
from botModule.importCom import *


### Start & Help Handler
@Client.on_message(filters.private & filters.command(["start", "help"]))
async def start_help_handler(
    bot : Update,
    msg : Message
    ):
    if await search_user_in_community(bot, msg):
        if msg.text == "/start":
            textMsg = f"<b>Hi, I am MegaUploaderBot🤖 Created by @AJPyroVerse and My Developer🧑‍💻 is @AJTimePyro.</b>\n\nAnd I support:-\n1. <u>Direct Downloading Link</u>\n2.<u>Telegram File</u>\n3. <u>Youtube URL</u>\n\n\n{to_login}\n😊We will store your login detail on our database.{common_text}"
        else:
            textMsg = f"{to_login}\n<b>After login😊 send Direct Downloading Link, Youtube URL or any Telegram File.\n\nTo remove your account from Database use /revoke.</b>{common_text}"
        await msg.reply_text(
            textMsg,
            parse_mode = "html"
        )
    return

