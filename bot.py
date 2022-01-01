#!/usr/bin/env python3


### Importing
# Importing External Packages
from pyrogram import Client

# Importing Inbuilt Packages
import logging
import os

# Importing Credentials & Required Data
try:
    from testexp.config import Config
except ModuleNotFoundError:
    from config import Config


### For Displaying Errors&Warnings Better
logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers = [
        logging.FileHandler("megauploader.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
logging.getLogger(
    "pyrogram"
).setLevel(
    logging.WARNING
)

### Starting Bot
if __name__ == "__main__" :

    # Creating download directories, if they does not exists
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        print("Creating 'DOWNLOADS' Directory")
        os.makedirs(Config.DOWNLOAD_LOCATION)
    
    # Connecting to Bot
    print("Connecting to Bot")
    app = Client(
        "MegaUploader",
        bot_token = Config.TG_BOT_TOKEN,
        api_id = Config.APP_ID,
        api_hash = Config.API_HASH,
        plugins = dict(
            root="plugins"
        )
    )
    print("Connection Establised")

    # Running The Bot
    print("Running Bot Now!!!")
    app.run()

