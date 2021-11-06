# !/usr/bin/env python3


"""Common functions, data required for downloading"""
from bot.botMessages import starting_to_download, uploading_msg, unsuccessful_upload, file_limit, downloadFolder, dev, uploading_unsuccessful
from plugins.helper import length_of_file, line_number
from time import sleep, time
from os import path, listdir
from shutil import rmtree

