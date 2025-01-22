# функция скачивания видев с ютуба и рутуба
from pytubefix import *
from rutube import Rutube
# from proxy import find_first
from params import *

def download(url, filename):
    if url.find('youtube') != -1 or url.find('youtu.be') != -1: # ссылка на ютуб?
        logging.info(url)

        yt = YouTube(url, use_po_token=True)
        ys = yt.streams.get_highest_resolution()

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