import os
import time

from youtube import *
from video import *
from image import *
from aiogram.filters import *
from aiogram.fsm.context import *
from aiogram.types import *
from params import *
from tiktok import *
import logging
import asyncio
import atexit
import shutil

# декораторы
@form_router.message(Command('start'))
async def menu(message: types.Message):
    await message.answer('чем тебе помочь?', reply_markup=keyboard_menu)

# декораторы
@form_router.message(Command('cancel'))
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer('Ну отмена так отмена', reply_markup=ReplyKeyboardRemove())

# декораторы
@form_router.message(F.text=='посмотри видео')
async def process_video(message: Message, state: FSMContext):
    await state.set_state(Form.vid)
    await message.answer('Давай присылай, готов слушать', reply_markup=ReplyKeyboardRemove())

# декораторы
@form_router.message(F.text=='посмотри картинку')
async def process_image(message: Message, state: FSMContext):
    await state.set_state(Form.img)
    await message.answer('Давай присылай, готов слушать', reply_markup=ReplyKeyboardRemove())

# декораторы
@form_router.message(F.text=='посмотри ютуб / рутуб')
async def process_yt(message: Message, state: FSMContext):
    await state.set_state(Form.yt)
    await message.answer('присылай ссылку, я посмотрю', reply_markup=ReplyKeyboardRemove())

# декораторы
@form_router.message(Form.yt)
async def process_yt_download(message: Message, state: FSMContext):
    # обработчик ошибок, связанных с моим любимым ркн
    try:
        await message.answer('сейчас обработаю подожди, терпение...\n'
                             'это не должно занимать много времени')
        # переменные названия файла, из user_id и message_id, и ссылки на видео
        filename, message_text = str(message.from_user.id) + str(message.message_id), message.text

        # скачивание файла с ютуб, подробнее в youtube.py
        files = download(message_text)
        if len(files) == 1: # ссылка на видео
            files = files[0]
            print('wv')
            print(files)
            file = FSInputFile(files)
            await message.answer_video(file, caption='на, держи!', reply_markup=keyboard_menu)
            os.remove(files)

        else: # ссылка плэйлист'
            print('wp')
            print(files)
            for i in range(0, len(files), 5):
                vids = [types.input_media_video.InputMediaVideo(media=FSInputFile(i)) for i in files[i:i + 5]]
                await message.answer_media_group(vids)
                await message.answer(f'[{min(i + 5, len(files))}/{len(files)}]')
            await message.answer('это все')
    except Exception as e:
        logging.exception(e)
        print('ERROR', e)
        if e != '':
            await message.answer('Ошибка\n' 
                                f'данные об ошибке: {e}')

        await state.clear()

# декораторы
@form_router.message(F.text=='посмотри тикток')
async def process_tiktok(message: Message, state: FSMContext):
    await state.set_state(Form.tt)
    await message.answer('скидывай ссылку, я скачаю', reply_markup=ReplyKeyboardRemove())

# декораторы
@form_router.message(Form.tt)
async def process_tiktok_download(message: Message, state: FSMContext):
    # тут почти все как в process_yt_download
    try:
        await message.answer('сейчас обработаю подожди...')
        # переменные названия файла, из user_id и message_id, и ссылки на видео
        filename, message_text = str(message.from_user.id) + str(message.message_id), message.text

        # скачивание файла с тектока, подробнее в tiktok.py
        files = download_tiktok(message_text, filename)

        # сслыка видео?
        if os.path.exists(f'cache/tiktok/{filename}.mp4'):
            file = FSInputFile(f'cache/tiktok/{filename}.mp4')
            await message.answer_video(file, caption='на, держи!', reply_markup=keyboard_menu)
        else: # ссылка фото'
            for i in range(0, len(files), 10):
                images = [types.input_media_photo.InputMediaPhoto(media=FSInputFile(i)) for i in files[i:i + 10]]
                await message.answer_media_group(images)
                await message.answer(f'[{min(i + 10, len(files))}/{len(files)}]')
            await message.answer('это все')
    except Exception as e:
        logging.exception(e)
        print('ERROR', e)
        if e != '':
            await message.answer('Ошибка\n'
                                f'данные об ошибке: {e}')

        await state.clear()

# декораторы
@form_router.message(Form.vid)
async def process_video_operations(message: Message, state: FSMContext):
    try:
        file = message.video
        if file is None:
            file = message.document
        print(file)
        file_id = file.file_id
        name = file.file_name
        if name is None:
            name = file_id + '.mp4'
        file_raw = await bot.get_file(file_id)

        await message.reply('сейчас обработаю подожди')
        await bot.download_file(file_raw.file_path, f'cache/videos/{name}')

        await state.set_state(Form.vid_processing)
        await state.update_data(vid=name)

        await message.answer(
            'обработал, во что конвертировать?', reply_markup=keyboard_vid)

    except Exception as e:
        logging.exception(e)
        await message.answer('Файл не видео, поврежден или слишком большой \n'
                             'P.S файл не может быть больше 20мб я ничего не могу с этим сделать, смирись')

# декораторы
@form_router.message(Form.img)
async def process_image_operations(message: Message, state: FSMContext):
    try:
        file = message.photo[-1]
        file_id = file.file_id
        await message.reply('сейчас обработаю подожди')
        await message.bot.download(file=message.photo[-1].file_id, destination=f'cache/images/{file_id}.png')

        await state.set_state(Form.img_processing)
        await state.update_data(img=file_id + '.png')

        await message.answer(
            'обработал, во что конвертировать?', reply_markup=keyboard_img)
    except Exception as e:
        logging.exception(e)
        await message.answer('Файл не картинка, поврежден или слишком большой \n'
                             'P.S файл не может быть больше 20мб я ничего не могу с этим сделать, смирись')

# декораторы
@form_router.message(Form.vid_processing)
async def convert_video(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        video = data['vid']

        to = message.text[7:]
        file_name, file_format = video[:video.rfind('.')], video[video.rfind('.') + 1:]

        file_path = convert_vid(file_name, file_format, to)
        file = FSInputFile(file_path)

        await message.answer_document(file, caption='на, держи!', reply_markup=keyboard_menu)
    except Exception as e:
        logging.exception(e)
        await message.answer('не вовремя')
    finally:
        os.remove(file_path)
        os.remove('cache/videos/' + file_name + '.' + file_format)
        await state.clear()

# декораторы
@form_router.message(Form.img_processing)
async def convert_image(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        image = data['img']

        to = message.text[7:]
        filename, file_format = image[:image.rfind('.')], image[image.rfind('.') + 1:]

        file_path = convert_img(filename, file_format, to)
        file = FSInputFile(file_path)

        await message.answer_document(file, caption='на, держи!', reply_markup=keyboard_menu)
    except Exception as e:
        logging.error(e)
        await message.answer('иди поплачь')
    finally:
        os.remove('cache/images/' + filename + '.' + file_format)
        await state.clear()

# создание папок если вдруг их нет и отчистка кэша
def check_cache_on_start():
    dirs = ['converted', 'images', 'videos', 'youtube', 'tiktok']
    if os.path.isdir('cache'):
        for directory in dirs:
            if os.path.isdir(f'cache/{directory}'):
                files = os.listdir(f'cache/{directory}')
                for i in files:
                    os.remove(f'cache/{directory}/{i}')
            else:
                os.mkdir(f'cache/{directory}')
    else:
        os.mkdir('cache')
        for directory in dirs:
            os.mkdir(f'cache/{directory}')


def exit_handler():
    shutil.rmtree('cache')

# запуск бота
async def main():
    logging.basicConfig(
        # filename="logs/" + '_'.join(str(time.ctime(time.time())).split()).replace(":", "") + ".log",
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG
    )

    logger = logging.getLogger(__name__)
    atexit.register(exit_handler)
    check_cache_on_start()
    dp.include_router(form_router)
    await dp.start_polling(bot)
