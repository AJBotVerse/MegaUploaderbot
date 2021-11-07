from plugins.helper import length_of_file, line_number
from time import sleep, time
from os import path, listdir
from shutil import rmtree
try:
    from testexp.config import Config
except ModuleNotFoundError:
    from config import Config

OwnerID = Config.OWNER_ID

