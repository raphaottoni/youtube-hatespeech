from config import Config
from apiclient.discovery import build
from apiclient.errors import HttpError

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
