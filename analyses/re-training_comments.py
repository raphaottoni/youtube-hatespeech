from gensim import corpora, models, similarities
import json
import numpy
import random
import gensim, copy
from collections import defaultdict
import glob, os


# Load model the base wikipedia model
model = gensim.models.Word2Vec.load("../models/wiki-word2vec/wiki-en.word2vec.model")

# All available political views
#policital_spectrum = ["right"] 
policital_spectrum = ["left",  "leftcenter", "center", "right-center", "right"] 

for bias in policital_spectrum:
    print("Loading comments from bias:" + bias )

    # load all channels of that bias 
    for file in os.listdir("../data/processed/comments/"+ bias + "/" ):
        if file.endswith(".txt"):
            with open("../data/processed/comments/"+ bias+ "/"+ file, "r") as file_reader:
                data = []
                for line in file_reader:
                    data.append(line.strip().split(" "))
                print("Training the model: " + bias  + "(" + file + ")")
                # Train the model
                model_wiki = copy.deepcopy(model)
                model_wiki.train(data,total_examples=len(data),epochs=model.iter)
                print("Saving the model")
                if not os.path.exists("../models/biases/comments/" + bias):
                    os.makedirs("../models/biases/comments/"+bias)
                model_wiki.save("../models/biases/comments/"+ bias + "/" + file[:-4] + ".model")


#cosine_similarity_prostitute = numpy.dot(model['woman'],model['prostitute'])/(numpy.linalg.norm(model['woman'])*numpy.linalg.norm(model['prostitute']))
#cosine_similarity_seductress =  numpy.dot(model['woman'],model['seductress'])/(numpy.linalg.norm(model['woman'])*numpy.linalg.norm(model['seductress']))
#print(cosine_similarity_prostitute,cosine_similarity_seductress)
#print(model.most_similar("woman"))
#print(model.wv["woman"])
###print(model.most_similar(positive=['woman', 'bike'], negative=['boy']))
###print("-----------------2 ")
