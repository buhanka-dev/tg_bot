from youtube import download
from pytubefix import *
p = Playlist('https://www.youtube.com/watch?v=pJc5SZTcFrw&list=OLAK5uy_mojBy7gXjbb-DCXjYCTWz1lp30IcEeZMQ&')
for video in p.videos:
     video.streams.get_highest_resolution().download()