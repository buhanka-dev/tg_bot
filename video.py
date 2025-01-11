# функция перевода видео из одного формата в другой
import logging

from moviepy import *

def c(input_file, output_file):
    try:
        with VideoFileClip(input_file) as video:
            if output_file.endswith('.gif'):
                video.write_gif(output_file)
            else:
                codec = 'libxvid' if c else None
                video.write_videofile(output_file, codec=codec)

    except Exception as e:
        logging.error(f'Ошибка при конвертации: {e}')


def convert_vid(filename, fr='mp4', to='mp4', compress=False):
    if compress:
        inp = f'cache/youtube/{filename}_raw.{fr}'
        out = f'cache/youtube/{filename}.{to}'
    else:
        inp = f'cache/videos/{filename}.{fr}'
        out = f'cache/converted/{filename}.{to}'
    c(inp, out)
    return out

