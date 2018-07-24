import csv
from youtube_api import YoutubeApi

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
    
    print("Searching medias in YouTube...")
    api = YoutubeApi()

    for media in all_medias:
        api.youtube_search(media)



if __name__ == "__main__":
    main()
