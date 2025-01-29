import random
from pytubefix import *
from params import *

def download(url):
     playlist = Playlist(url, 'WEB', use_oauth=True, allow_oauth_cache=True)
     paths = []
     for video in playlist.videos:
          print(video.title)
          path = re.sub('[^A-Za-z0-9 ]','', video.title)
          paths.append(path)
          video.streams.get_highest_resolution().download(output_path=f'cache/youtube/',
                                                          timeout=120,
                                                          filename=f'{path}.mp4')
     return paths

if __name__ == '__main__':
     print(download('https://www.youtube.com/watch?v=OGygxiR9s1U&list=PL0oGAkZp3KOJXuqaM-gLNhMCZvzOeGWP8'))