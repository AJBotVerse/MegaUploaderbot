#!/usr/bin/env python3


### Importing
# Importing Common Files
from botModule.importCom import *

parse_mode=enums.ParseMode.HTML

### Log files Handler
@Client.on_message(filters.chat(Config.OWNER_ID) & filters.private & filters.command("log"))
async def logHandler(bot:Update, msg:Message):
    try:
        await msg.reply_document('megauploader.log')
    except Exception as e:
        await msg.reply_text(
            f"Something went wrong while sending log file.\n{e}",
            #parse_mode = 'html' 
             parse_mode
        )


### Broadcast Handler
@Client.on_message(filters.chat(Config.OWNER_ID) & filters.regex("^/broadcast"))
async def broadcast_handler(bot:Update, msg:Message):

    MSG = msg.reply_to_message
    if not MSG:
        return await msg.reply_text(
            "First send me the message that you want to send to the other users of this bot! <b>Then as a reply to it send <code>/broadcast</code></b>",
            #parse_mode = 'html' 
            parse_mode
        )
    m = await msg.reply_text(
        "<code>Broadcasting..</code>",
        #parse_mode = 'html' 
         parse_mode
    )
    SUCE = 0
    FAIL = 0
    for userid in [document['userid'] for document in collection_login.find()]:
        try:
            await MSG.copy(userid)
            SUCE += 1
        except Exception as e:
            FAIL += 1
    await msg.reply_text(
        f"Successfully Broadcasted to {SUCE} Chats\nFailed - {FAIL} Chats!"
    )
    await m.delete()
    return

    

