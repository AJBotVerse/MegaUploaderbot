from botModule.botHelper import line_number, length_of_file
from botModule.botMSG import BotMessage
from time import sleep, time
from os import path, listdir
from shutil import rmtree
try:
    from testexp.config import Config
except ModuleNotFoundError:
    from config import Config

OwnerID = Config.OWNER_ID

