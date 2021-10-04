#!/usr/bin/env python3


"""Importing environ from os Library"""
from os import environ


'''Credentials'''


api_id = environ["API_ID"] #Your API ID

api_hash = environ["API_HASH"]   #Your API Hash

bot_token = environ["BOT_TOKEN"]  #Your Bot Token

mongo_connection_string = environ["MONGO_CON_STRING"]    #Your MongoDB Connection String
