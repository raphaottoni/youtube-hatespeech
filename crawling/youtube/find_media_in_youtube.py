import csv
from youtube_api import YoutubeApi
from tqdm import tqdm

def main():
    print("loading media names...")
    
    # Create the dictionary of medias
    medias_bias = {}
    with open('../../data/mediasbias.csv', 'r') as csvfile:
        media_reader = csv.reader(csvfile, delimiter=',')
        for row in media_reader:
            medias_bias[row[0]] = row[1]
    
    
    # collect all medias
    all_medias = medias_bias.keys()
    print("Done!")
    
    api = YoutubeApi()

    # write csv with all medias name and the associated bias
    with open("../../data/mediasbias_with_youtube_channel.csv", 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["media, bias, youtube_channel, viewCount, subscribersCount, videoCount"])

        print("Searching for media channels in YouTube...")
        for media in tqdm(all_medias):
            channels = api.youtube_search(media)
            if channels:
                most_proeminent_channel = channels[0][1]
                channel_statistic = api.get_channel_info(most_proeminent_channel)
                writer.writerow([media, medias_bias[media], most_proeminent_channel, channel_statistic["viewCount"], channel_statistic["subscriberCount"], channel_statistic["videoCount"]])
        print("Done! Results written in ../../data/mediasbias_with_youtube_channel.csv")




if __name__ == "__main__":
    main()
