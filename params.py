from aiogram import *
from aiogram.client.default import *
from aiogram.enums import *
from aiogram.fsm.state import *
from aiogram.utils.keyboard import *
import logging


class Form(StatesGroup):
    vid = State()
    vid_processing = State()
    img = State()
    img_processing = State()
    yt = State()
    tt = State()

# базовые переменные, чтобы все работало
form_router = Router()
TOKEN = '7858275211:AAGpfmKD2n66Gzas3ljiYPHUnbRt6siPjpM'
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


kb_menu_builder = ReplyKeyboardBuilder()
kb_menu_builder.button(text='посмотри видео')
kb_menu_builder.button(text='посмотри картинку')
kb_menu_builder.button(text='посмотри ютуб / рутуб')
kb_menu_builder.button(text='посмотри тикток')
kb_menu_builder.adjust(2, 2)
keyboard_menu = kb_menu_builder.as_markup(resize_keyboard=True)


kb_vid_builder = ReplyKeyboardBuilder()
kb_vid_builder.button(text='сделай mp3')
kb_vid_builder.button(text='сделай mp4')
kb_vid_builder.button(text='сделай gif')
kb_vid_builder.button(text='сделай avi')
kb_vid_builder.button(text='сделай webm')
kb_vid_builder.adjust(3, 2)
keyboard_vid = kb_vid_builder.as_markup(resize_keyboard=True)


kb_img_builder = ReplyKeyboardBuilder()
kb_img_builder.button(text='сделай jpg')
kb_img_builder.button(text='сделай png')
kb_img_builder.button(text='сделай webp')
kb_img_builder.button(text='сделай tiff')
kb_img_builder.adjust(2, 2)
keyboard_img = kb_img_builder.as_markup(resize_keyboard=True)