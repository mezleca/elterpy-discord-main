from contextlib import redirect_stdout
import io
import json
import asyncio
import yt_dlp
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

def is_url(url):
    return url.startswith('http://') or url.startswith('https://')

class Downloader():

    def __init__(self, url):
        self.url = url
        self.ydl_opts = {
            'format': 'bestaudio[abr<=128]/best[abr<=128]/worst',
            'extractaudio': True,
            'audioformat': 'mp3',
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'noplaylist': True,
            'limit_rate': '500K',
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0'
        }
        self.yt_dlp = yt_dlp.YoutubeDL(self.ydl_opts)

    async def search(self):
        try:
            info = None
            if is_url(self.url):
                info = await asyncio.get_event_loop().run_in_executor(
                    None, 
                    lambda: self.yt_dlp.extract_info(self.url, download=False)
                )
            else: 
                info = await asyncio.get_event_loop().run_in_executor(
                    None, 
                    lambda: self.yt_dlp.extract_info(f"ytsearch:{self.url}", download=False)['entries'][0]
                )
            return {
                'url': info['url'],
                'title': info['title'],
                'duration': info['duration']
            }
        except Exception as e:  
            print(f"failed to extract info: {e}")
            return None
        except DownloadError as e:
            print(e)
            return None
        
    def get_playlist(self):
        try:
            playlist_info = self.yt_dlp.extract_info(self.url, download=False)
            
            # Check if it's actually a playlist
            if 'entries' not in playlist_info:
                print("no entries in playerlist info")
                return None
            
            # Extract video details
            playlist_videos = []
            for video in playlist_info['entries']:
                if video is not None:
                    playlist_videos.append({
                        'title': video.get('title', 'Unknown Title'),
                        'url': video.get('webpage_url', ''),
                        'duration': video.get('duration', 0),
                        'playlist_index': video.get('playlist_index', 0)
                    })
            
            return playlist_videos
        except Exception as e:
            print(f"error getting playlist: {e}")
            return None

    def download(self):
        buffer = io.BytesIO()
        with redirect_stdout(buffer), YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([self.url])
        return buffer
