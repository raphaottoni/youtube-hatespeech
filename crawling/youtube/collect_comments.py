import csv
from youtube_api import YoutubeApi
from tqdm import tqdm
import jsonlines

def main():

    print("loading YouTube video IDs ...")
    # Create the dictionary of medias
    video_info = {}
    with open('../../data/manually-filtered/youtube_videos.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)  # skip the headers
        for row in reader:
            video_info[row[0]] = {  "media": row[1].strip(), "bias": row[2].strip(), "channel": row[3].strip()}
 
    
    # collect all medias
    all_videos = video_info.keys()
    print("Done!")

    print("Checking how many aren't collected yet...") 

    already_collected = []

    try: 
        with open('../../data/video_already_collected_comments.csv', "r") as csv_collected: 
            reader = csv.reader(csv_collected)
            for video in reader:
                already_collected.append(video[0])
    except FileNotFoundError:
        print("video_already_collected_comments.csv wasnt found. Thus I am assuming that the datacrawling has not begun.")
 

    remaning_videos_to_collect = set(all_videos) - set(already_collected)

    print("Done!")
    api = YoutubeApi()

    # write json file with all data from the video, each line is a json
    with jsonlines.open("../../data/video_comments.jsonl", 'a') as writer:


        # Just an example of videos that comments were disable
        #comments = api.collect_comments_from_Video("LUxviiQDRYA")

        print("Collecting captions from YouTube videos...")
        for video in tqdm(remaning_videos_to_collect):

            comments = api.collect_comments_from_Video(video)

            if comments:
                for comment in comments :
                    video_comment = { "videoID": video, "media": video_info[video]["media"], "bias": video_info[video]["bias"],  "channel": video_info[video]["channel"], "comment": comment } 
                    writer.write(video_comment)

            # inform that the video was collected
            with open('../../data/video_already_collected_comments.csv', "a") as write_file:
               write_file.write(video +"\n")

        print("Done! Results written in ../../data/video_commentss.jsonl")



if __name__ == "__main__":
    main()
