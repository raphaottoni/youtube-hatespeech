import csv
import jsonlines

def main():

    print("loading YouTube Channel Ids...")
    # Create the dictionary of medias
    channel_info = {}
    with open('../data/manually-filtered/youtube_channels.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)  # skip the headers
        for row in reader:
            channel_info[row[2]] = {  "mediaName": row[0].strip(), "bias": row[1].strip(), "nVideos": 0, "nComments": 0}
    print("done")
     
    print(channel_info)

    print("Couting number of videos from channels that we have transcript...")
    with jsonlines.open('../data/videos.jsonl') as reader:
        for obj in reader:
            channel_info[obj["channel"]]["nVideos"] += 1
    print("done")

    print("Couting number of comments from channels that we have transcript...")
    with jsonlines.open('../data/video_comments.jsonl') as reader:
        for obj in reader:
            channel_info[obj["channel"]]["nComments"] += 1
    print("done")

       
    print("Saving statistics into ../data/dataset_stats.jsonl")
    # Save statisctics
    with jsonlines.open("../data/dataset_stats.jsonl", 'a') as writer:
        for channel in channel_info:
            writer.write(channel_info[channel])
    print("Done")


    
if __name__ == "__main__":
    main()
