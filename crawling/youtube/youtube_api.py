from config import Config
from apiclient.discovery import build
from apiclient.errors import HttpError
import urllib.request
import re
import json
import codecs
import html

# Class that handles youtube api v3
class YoutubeApi():

    def __init__(self):
        # loads the configs
        config = Config()
        DEVELOPER_KEY = config.youtube_key
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"
        self.youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

        
    #Search the youtube for the query
    def youtube_search(self, query,  maxResults = 50, kind = "channels"):
 
        search_response = self.youtube.search().list(
            q = query,
            part = "id,snippet",
            maxResults = maxResults
        ).execute()
    
        videos = []
        channels = []
        playlists = []
        results =  []
        
        # Add each result to the appropriate list, and then display the lists of
        # matching videos, channels, and playlists.
        for search_result in search_response.get("items", []):
          if search_result["id"]["kind"] == "youtube#video":
            videos.append([search_result["snippet"]["title"], search_result["id"]["videoId"]])
          elif search_result["id"]["kind"] == "youtube#channel":
            channels.append([search_result["snippet"]["title"], search_result["id"]["channelId"]])
          elif search_result["id"]["kind"] == "youtube#playlist":
            playlists.append([search_result["snippet"]["title"], search_result["id"]["playlistId"]])

        results = channels  if kind == "channels" else videos if kind == "videos" else playlists

        return results

    # get channel info
    def get_channel_info(self, channel, part="statistics"):
        
        response = self.youtube.channels().list(
            part = part,
            id = channel
        ).execute()
 
        return response["items"][0][part] if response["items"] else [] 


    # Collect videos from channel
    def youtube_get_videos_from_channel(self, channel_id):
        search_response = self.youtube.search().list(
                                channelId= channel_id,
                                part = "id",
                                type = "video",
                                maxResults=50
                            ).execute()
        videos = []
        continue_searching = True

        while(continue_searching):
            new_videos = [ video["id"]["videoId"] for video in search_response["items"] if video["id"]["kind"] == "youtube#video" ]
            if "nextPageToken" in search_response: 
                search_response = self.youtube.search().list(
                                        channelId= channel_id,
                                        part = "id",
                                        type = "video",
                                        pageToken= search_response["nextPageToken"],
                                        maxResults=50
                                    ).execute()
                videos.extend(new_videos)
            else:
                continue_searching = False

        return videos



    # Collect video caption
    def collect_closed_captions(self, video_id, lang="pt"):
    
        url_video = "https://www.youtube.com/watch?v={}".format(video_id)
        html = urllib.request.urlopen(url_video, timeout=30).read().decode("utf-8")
        search_url = re.search("\'TTS_URL\': (.*),", html)
    
        if search_url:
            url_partial = json.loads(search_url.group(1))
            if len(url_partial) > 0:
                url_caption = "{}&kind=asr&lang={}&fmt=srv3".format(url_partial, lang)
                data_caption = urllib.request.urlopen(url_caption, timeout=30).read().decode("utf-8")
            else:
                data_caption = None
        else:
            data_caption = None
    
        return data_caption

    # Clean html tags
    @staticmethod
    def cleanhtml(raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return html.unescape(re.sub(" +", " ", cleantext.strip().replace('\n',' ')))


    # Collect caption
    # params
    # ------
    #   video_id: str
    #       Youtube's video identification 
    #   lang: str
    #       What language you want to get
    #   kind: str
    #       Which kind of text do you want: "transcript" (Google's algorithm speech to text) 
    #                                       "subtitle" (Use's uploaded subtitles
    #                                       "both" (return both transcript and subtitle) 
    # returns
    # -------
    #   captions: dict
    #       dict containing the specified kind of caption regarding the video. The key is the kind specified.

    def collect_caption(self, video_id, lang="en", kind="both"):
    
        url_video = "https://www.youtube.com/watch?v={}".format(video_id)
        html = urllib.request.urlopen(url_video, timeout=30).read().decode("utf-8")
    
        search_url = re.search("\'TTS_URL\': (.*),", html)
    
        data_caption = {} 

        if search_url:
            url_partial = json.loads(search_url.group(1))
            if kind == "subtitle":
                if (not ("kind=asr" in url_partial)) and len(url_partial) > 0:
                    try:
                        url_caption = "{}&lang={}&fmt=srv3".format(url_partial, lang)
                        data_caption["subtitle"] = YoutubeApi.cleanhtml(urllib.request.urlopen(url_caption, timeout=30).read().decode("utf-8"))
                    except urllib.error.HTTPError:
                        data_caption["subtitle"] = None
                else:
                    data_caption["subtitle"] = {}
            elif kind == "transcript":
                if len(url_partial) > 0:
                    try:
                        url_caption = "{}&kind=asr&lang={}&fmt=srv3".format(url_partial, lang)
                        data_caption["transcript"]  = YoutubeApi.cleanhtml(urllib.request.urlopen(url_caption, timeout=30).read().decode("utf-8"))
                    except urllib.error.HTTPError:
                        data_caption["transcript"] = None
                else:
                    data_caption["transcript"] = None
            elif kind == "both":
                if (not ("kind=asr" in url_partial)) and len(url_partial) > 0:
                    try:
                        url_caption = "{}&lang={}&fmt=srv3".format(url_partial, lang)
                        data_caption["subtitle"] = YoutubeApi.cleanhtml(urllib.request.urlopen(url_caption, timeout=30).read().decode("utf-8"))
                    except urllib.error.HTTPError:
                        data_caption["subtitle"] = None
                else:
                    data_caption["subtitle"] = None

                if len(url_partial) > 0:
                    try:
                        url_caption = "{}&kind=asr&lang={}&fmt=srv3".format(url_partial, lang)
                        data_caption["transcript"]  = YoutubeApi.cleanhtml(urllib.request.urlopen(url_caption, timeout=30).read().decode("utf-8"))
                    except urllib.error.HTTPError:
                        data_caption["transcript"] = None
                else:
                    data_caption["transcript"] = None
        else:
            data_caption= {}
        
        return data_caption
