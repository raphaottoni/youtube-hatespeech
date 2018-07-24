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
    def youtube_search(self, query,  maxResults = 50):
 
        search_response = self.youtube.search().list(
            q = query,
            part = "id,snippet",
            maxResults = maxResults
        ).execute()
    
        videos = []
        channels = []
        playlists = []
        
        # Add each result to the appropriate list, and then display the lists of
        # matching videos, channels, and playlists.
        for search_result in search_response.get("items", []):
          if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                       search_result["id"]["videoId"]))
          elif search_result["id"]["kind"] == "youtube#channel":
            channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                         search_result["id"]["channelId"]))
          elif search_result["id"]["kind"] == "youtube#playlist":
            playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                          search_result["id"]["playlistId"]))
 
        print("################################# "  + query + " ############################")     
        print("Videos:\n"+ "\n".join(videos)+ "\n")
        print("Channels:\n"+ "\n".join(channels)+ "\n")
        print("Playlists:\n" + "\n".join(playlists)+ "\n")
