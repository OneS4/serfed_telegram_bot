import logging
import os
import shutil

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputFile, BotCommand, \
    BotCommandScope, bot_command_scope
from aiogram.utils import executor
from aiogram.types import ParseMode

from bot_database import *
from bot_youtube import *
from bot_weather import *

logging.basicConfig(level=logging.INFO)

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())

path = ''
botname = ''
bot_id = ''


class States(StatesGroup):
    check_access_state = State()
    delete_access_start = State()
    video_state = State()
    playlist_state = State()
    create_dir = State()
    delete_dir = State()
    load_files = State()
    upload_files = State()
    send_files = State()
