import csv
from youtube_api import YoutubeApi
from tqdm import tqdm
import json

def main():

    print("loading YouTube video IDs ...")
    # Create the dictionary of medias
    video_info = {}
    with open('../../data/manually-filtered/youtube_videos.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)  # skip the headers
        for row in reader:
            video_info[row[0]] = {  "media": row[1], "bias": row[2], "channel": row[3]}
 
    
    # collect all medias
    all_videos = video_info.keys()
    print("Done!")
    
    api = YoutubeApi()

    # write json file with all data from the video, each line is a json
    with open("../../data/videos.jsonl", 'w') as json_file:

        print("Collecting captions from YouTube videos...")
        for video in tqdm(all_videos):
            captions = api.collect_caption(video, "en", "both")
            if captions:
                video = { "videoID": video, "media": video_info[video]["media"], "bias": video_info[video]["bias"],  "channel": video_info[video]["channel"], "captions": captions} 
                json.dump(video, json_file)
        print("Done! Results written in ../../data/videos.jsonl")


if __name__ == "__main__":
    main()
