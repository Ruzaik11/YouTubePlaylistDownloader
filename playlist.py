import googleapiclient.discovery
from urllib.parse import parse_qs, urlparse
import pytube
import os
from tqdm import tqdm
from time import sleep
from pprint import pprint
import sys


class playlist:

    play_list = []

    download_format='720p'

    default_path = 'C:\Downloads'

    def __init__(self, url, path, format) -> None:
        self.url = url
        self.path = path
        self.format = format

    def extract_play_list(self):

        
        if(self.format == '1'):
            self.download_format = '360p'
        elif(self.format == '2'):
            self.download_format = '720p'
        else:
            sys.exit("invalid video format please enter (1=360p,2=720p)")

        playlist_items=pytube.Playlist(self.url) 
      
        print(f"total: {len(playlist_items)}")

        for videos in tqdm(playlist_items):
            sleep(0.25)
            self.download_videos(videos)

        print("Playlist downloaded successfully....")

    def download_videos(self, video_url):

        if(self.path == ''):
            self.path = self.default_path

        if not os.path.exists(self.path):
            os.makedirs(self.path)

        yt = pytube.YouTube(video_url)

        streamvid = yt.streams.filter(res=self.download_format, progressive=True).first()
        
        if not os.path.exists(self.path + '\\' + streamvid.default_filename ):
            streamvid.download(self.path)
        # sys.exit()


pl = playlist(
    url=input('Play List URL :'), path=input('Download Folder Default: C:\Downloads :'), format=input('Video Format (1=360p,2=720p) :'))
pl.extract_play_list()
