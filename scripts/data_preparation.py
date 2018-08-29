import csv
import random
import string
import re
import jsonlines
import os

LATIN_1_CHARS = (
    (b'\xe2\x80\x99', b"'"),
    (b'\xc3\xa9', b'e'),
    (b'\xe2\x80\x90', b'-'),
    (b'\xe2\x80\x91', b'-'),
    (b'\xe2\x80\x92', b'-'),
    (b'\xe2\x80\x93', b'-'),
    (b'\xe2\x80\x94', b'-'),
    (b'\xe2\x80\x94', b'-'),
    (b'\xe2\x80\x98', b"'"),
    (b'\xe2\x80\x9b', b"'"),
    (b'\xe2\x80\x9c', b'"'),
    (b'\xe2\x80\x9c', b'"'),
    (b'\xe2\x80\x9d', b'"'),
    (b'\xe2\x80\x9e', b'"'),
    (b'\xe2\x80\x9f', b'"'),
    (b'\xe2\x80\xa6', b'...'),
    (b'\xe2\x80\xb2', b"'"),
    (b'\xe2\x80\xb3', b"'"),
    (b'\xe2\x80\xb4', b"'"),
    (b'\xe2\x80\xb5', b"'"),
    (b'\xe2\x80\xb6', b"'"),
    (b'\xe2\x80\xb7', b"'"),
    (b'\xe2\x81\xba', b"+"),
    (b'\xe2\x81\xbb', b"-"),
    (b'\xe2\x81\xbc', b"="),
    (b'\xe2\x81\xbd', b"("),
    (b'\xe2\x99\xab', b""),
    (b'\xc2\xa1', b""),
    (b'\xc2\xa0', b" "),
    (b'\xc3\xa7', b"c"),
    (b'\xc3\xb1', b"n"),
    (b'\xc3\xa0', b"a"),
    (b'\xc3\xa1', b"a"),
    (b'\xc3\xa2', b"a"),
    (b'\xc3\xa3', b"a"),
    (b'\xc3\xa4', b"a"),
    (b'\xc3\xa5', b"a"),
    (b'\xc3\xb2', b"o"),
    (b'\xc3\xb3', b"o"),
    (b'\xc3\xb4', b"o"),
    (b'\xc3\xb5', b"o"),
    (b'\xc3\xb6', b"o"),
    (b'\xc3\xba', b"u"),
    (b'\xc3\xbb', b"u"),
    (b'\xc3\xbc', b"u"),
    (b'\xc3\xa8', b"e"),
    (b'\xc3\xaa', b"e"),
    (b'\xc3\xab', b"e"),
    (b'\xc3\xa9', b"e"),
    (b'\xc3\xac', b"i"),
    (b'\xc3\xad', b"i"),
    (b'\xc3\xae', b"i"),
    (b'\xc3\xae', b"i"),
    (b'\xc3\xaf', b"i"),
    (b'\xc2\xad', b""),
    (b'\xe2\x81\xbe', b")")
)

def unicodetoascii(text):

    data = text.encode("utf-8")
    for _hex, _char in LATIN_1_CHARS:
        data = data.replace(_hex, _char)
    return data    

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', str(raw_html))
    return cleantext

def remove_punctuation(text):
    puncutations =  set(string.punctuation)

    for punctuation in puncutations:
        text = text.replace(punctuation, " ")
    return text    

def prep_data(text):

    # Convert those nasty unicode characteres
    text = unicodetoascii(text)
    text = text.decode("utf-8")
    # Remove html tags
    text = cleanhtml(text)
    # Remove punctuation
    text = remove_punctuation(text)
    # turn to lower case
    text = text.lower()
    # Remove multiple spaces
    text = re.sub(' +',' ',text)

    return text


def main():
    
    # All available political views
    policital_spectrum = ["left",  "leftcenter", "center", "right-center",
    "right"]

    captions = {}
    comments = {}

    for bias in policital_spectrum:
        captions[bias] = {}
        comments[bias] = {}

    # Generate one file for channel captions into directory data 
    with jsonlines.open('../data/videos.jsonl') as reader:
        print("Collecting captions from videos")

        for obj in reader:      

            if obj["bias"] in policital_spectrum:
                # create the channel key if it dosnt exista
                if obj["channel"] not in captions[obj["bias"]]:
                    captions[obj["bias"]][obj["channel"]] = []

                if obj["captions"]["subtitle"]:
                    captions[obj["bias"]][obj["channel"]].append(prep_data(obj["captions"]["subtitle"]))
                elif obj["captions"]["transcript"]:
                    captions[obj["bias"]][obj["channel"]].append(prep_data(obj["captions"]["transcript"]))

        print("Writing captions from channels")
        for bias in policital_spectrum:
            for channel in captions[bias]:

                # create directory if it is the case
                if not os.path.exists("../data/processed/captions/" + bias + "/"):
                        os.makedirs("../data/processed/captions/" + bias + "/")
                # Saves olnly those channels with equal or more than 100 video's
                # captions collected
                if captions[bias][channel] and len(captions[bias][channel]) >= 100:
                    with open("../data/processed/captions/"+ bias+ "/" + channel + ".txt", "w") as file_writer:
                        # shuffle the captions using the same seed for reproducibility
                        # porpuses
                        random.seed(10)
                        random.shuffle(captions[bias][channel])
                        for caption in captions[bias][channel]:
                            try:
                                file_writer.write(caption + "\n")
                            except UnicodeEncodeError:
                                c = prep_data(caption)
                                try:
                                    file_writer.write(c + "\n")
                                except UnicodeEncodeError: 
                                    c = c.encode('ascii', 'ignore').decode("utf-8")
                                    file_writer.write(c + "\n")

    # Generate one file for channel captions into directory data 
    with jsonlines.open('../data/video_comments.jsonl') as reader:
        print("Collecting comments from videos")

        for obj in reader:      
            if obj["bias"] in policital_spectrum:
                # create the channel key if it dosnt exista
                if obj["channel"] not in comments[obj["bias"]]:
                    comments[obj["bias"]][obj["channel"]] = []

                comment  = prep_data(obj["comment"]["snippet"]["topLevelComment"]["snippet"]["textDisplay"])
                if comment: 
                    comments[obj["bias"]][obj["channel"]].append(comment)

        print("Writing comments from videos")
        for bias in policital_spectrum:
            for channel in comments[bias]:

                # create directory if it is the case
                if not os.path.exists("../data/processed/comments/" + bias + "/"):
                        os.makedirs("../data/processed/comments/" + bias + "/")
 
                # olnly save those comments that we have more than 100 video's
                # captions
                if comments[bias][channel] and captions[bias][channel] and len(captions[bias][channel]) >= 100:
                    with open("../data/processed/comments/"+ bias+ "/" + channel+ ".txt", "w") as file_writer:
                        # shuffle the captions using the same seed for reproducibility
                        # porpuses
                        random.seed(10)
                        random.shuffle(comments[bias][channel])
                        for comment in comments[bias][channel]:
                            try:
                                file_writer.write(comment + "\n")
                            except UnicodeEncodeError:
                                c = prep_data(comment)
                                try:
                                    file_writer.write(c + "\n")
                                except UnicodeEncodeError: 
                                    c = c.encode('ascii', 'ignore').decode("utf-8")
                                    file_writer.write(c + "\n")

       

    
if __name__ == "__main__":
    main()
