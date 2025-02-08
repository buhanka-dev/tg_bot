# функция скачивания видев с ютуба и рутуба
from faker.generator import random
from pytubefix import *
from rutube import Rutube
# from proxy import find_first
from params import *

def download(url):
    if url.find('youtube') != -1 or url.find('youtu.be') != -1: # ссылка на ютуб?
        if url.find('&list=') != -1 and url.find('index=') == -1: # это плейлист?
            print('p')
            playlist = Playlist(url, 'WEB', use_oauth=True, allow_oauth_cache=True)
            paths = []
            for video in playlist.videos:
                path = re.sub("[^А-Яа-яA-Za-z0-9 ]", "", video.title)
                paths.append([f'cache/youtube/{path}.mp4', video.title])
                print([f'cache/youtube/{path}.mp4', video.title])
                video.streams.get_highest_resolution().download(output_path=f'cache/youtube/',
                                                                timeout=120,
                                                                filename=f'{path}.mp4')
            return paths
        else:
            print('v')
            video = YouTube(url)
            print(video.title)
            path = re.sub("[^A-Za-z0-9 ]", "", video.title)
            ys = video.streams.get_highest_resolution()

            # запись файла в папку
            ys.download(output_path=f'cache/youtube/',
                        timeout=120,
                        filename=f'{path}.mp4')

            print([f'cache/youtube/{path}.mp4', video.title])
            return [[f'cache/youtube/{path}.mp4', video.title]]


    elif url.find('rutube') != -1:  # ссылка на рутуб?
        rt = Rutube(url)
        with open(f'cache/youtube/{random.random()}_{random.random()}.mp4', 'wb') as f:
            rt.get_best().download(stream=f)
    else:  # ссылка неправильная
        logging.error('Неправильная ссылка')

# тесты
if __name__ == '__main__':
    download('https://www.youtube.com/watch?v=YtUvMXvln4w')