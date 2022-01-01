#!/usr/bin/env python3


### Importing
from os import environ

class Config(object):
    TG_BOT_TOKEN = environ.get("BOT_TOKEN", "") # Make a bot from https://t.me/BotFather and enter the token here
    
    APP_ID = int(environ.get("API_ID", 12345)) # Get this value from https://my.telegram.org/apps
    
    API_HASH = environ.get("API_HASH", "") # Get this value from https://my.telegram.org/apps
    
    OWNER_ID = int(environ.get("OWNER_ID", None)) # Your(owner's) telegram id
    
    MONGO_STR = environ.get("MONGO_STR", "") # Get from MongoDB Atlas

    DOWNLOAD_LOCATION = "app//DOWNLOADS//" # The download location for users. (Don't change anything in this field!)

    