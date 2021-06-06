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

    default_path = 'C:\Downloads'

    def __init__(self, url, path, format) -> None:
        self.url = url
        self.path = path
        self.format = format

    def extract_play_list(self):
        query = parse_qs(urlparse(self.url).query, keep_blank_values=True)

        playlist_id = query["list"][0]

        youtube = googleapiclient.discovery.build(
            "youtube", "v3", developerKey="")

        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50
        )

        response = request.execute()

        playlist_items = []

        while request is not None:
            response = request.execute()
            playlist_items += response["items"]
            request = youtube.playlistItems().list_next(request, response)

        print(f"total: {len(playlist_items)}")

        for videos in tqdm(playlist_items):
            sleep(0.25)
            video_url = f'https://www.youtube.com/watch?v={videos["snippet"]["resourceId"]["videoId"]}&list={playlist_id}&t=0s'
            self.download_videos(video_url)

    def download_videos(self, video_url):

        if(self.path == ''):
            self.path = self.default_path

        if not os.path.exists(self.path):
            os.makedirs(self.path)

        if(self.format == '1'):
            self.format = '360p'
        elif(self.format == '2'):
            self.format = '720p'
        else:
            sys.exit("invalid video format please enter (1=360p,2=720p)")

        yt = pytube.YouTube(video_url)

        streamvid = yt.streams.filter(
            res=self.format, progressive=True).first()
        streamvid.download(self.path)

        # sys.exit()


pl = playlist(
    url=input('Play List URL :'), path=input('Download Folder Default: C:\Downloads :'), format=input('Video Format (1=360p,2=720p) :'))
pl.extract_play_list()
