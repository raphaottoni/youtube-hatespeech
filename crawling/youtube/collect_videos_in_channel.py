import csv
from youtube_api import YoutubeApi
from tqdm import tqdm

def main():

    print("loading YouTube Channels...")  
    
    # Create the dictionary of channels
    channel_info= {}
    with open('../../data/manually-filtered/youtube_channels.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)  # skip the headers
        for row in reader:
            channel_info[row[2]] = [row[0], row[1], row[2], row[3], row[4], row[5]]
    
    all_channels = channel_info.keys()
    print("Done! Found " + str(len(all_channels)) +  " channels.")
    
    api = YoutubeApi()

    # write csv with all videos also containing the channel info
    with open("../../data/manually-filtered/youtube_videos.csv", 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["videoId, media, bias, youtube_channel, viewCount, subscribersCount, videoCount"])

        print("Collect videoIDs from Youtube Channels...")
        for channel in tqdm(all_channels):
            videos = api.youtube_get_videos_from_channel(channel)

            for video in videos:
                writer.writerow([video, channel_info[channel][0], channel_info[channel][1], channel_info[channel][2], channel_info[channel][3], channel_info[channel][4], channel_info[channel][5]])

        print("Done! Results written in ../../data/manually-filtered/youtube_videos.csv")

if __name__ == "__main__":
    main()
