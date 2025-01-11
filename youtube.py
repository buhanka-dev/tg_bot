# функция скачивания видев с ютуба и рутуба
from pytubefix import *
from rutube import Rutube
# from proxy import find_first
from video import convert_vid
from params import *

def download(url: str, filename: str):
    if url.find('youtube') != -1 or url.find('youtu.be') != -1: # ссылка на ютуб?
        # СТАРОЕ !!!!
        # прокси полученные в программе proxy.py
        # p = find_first(url)
        # proxy = {
        #   'http': f'http://{p}',
        # }

        # P.S теперь проски ненужны потому что я скачал zapret

        yt = YouTube(url,) #proxies=proxy)
        ys = yt.streams.get_highest_resolution()
        print(yt.streams)

        # ys.download(output_path=f'cache/youtube/', timeout=120, filename=f'{filename}_raw.mp4')
        # # сжатие видео
        # convert_vid(filename, compress=True)

        # запись файла в папку
        ys.download(output_path=f'cache/youtube/', timeout=120, filename=f'{filename}.mp4')
    elif url.find('rutube') != -1:  # ссылка на рутуб?
        rt = Rutube(url)
        with open(f'cache/youtube/{filename}.mp4', 'wb') as f:
            rt.get_best().download(stream=f)
    else:  # ссылка неправильная
        logging.error('Неправильная ссылка')

# тесты
if __name__ == '__main__':
    download('https://www.youtube.com/watch?v=oA_KFouhgdI', '1111')