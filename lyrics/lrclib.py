import requests
import urllib3
from lrclib import LrcLibAPI
from .parsing import lrc_to_dictionary


class LRCLibLyrics:
    def __init__(self):
        self.lyrics_api = LrcLibAPI(user_agent="VRC-Lyrics")

    def get_lyrics(self, playback):
        duration = playback.duration_ms / 1000
        words = playback.name.split()

        for wc in range(len(words), 0, -1):
            title = ' '.join(words[:wc])
            for artist in playback.artists:
                try:
                    results = self.lyrics_api.search_lyrics(track_name=title, artist_name=artist['name'])
                except (requests.exceptions.SSLError, urllib3.exceptions.ProtocolError) as e:
                    # Prevents fatal error when LRC servers hit rate limit
                    print(f'LRC Server Error: {e}')
                    results = []
                filtered = [r for r in results if r.synced_lyrics and abs(r.duration - duration) <= 3]
                if filtered:
                    return lrc_to_dictionary(filtered[0].synced_lyrics)

        return None
