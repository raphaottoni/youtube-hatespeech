from gensim import corpora, models, similarities
import json
import numpy
import random
import gensim, copy
from collections import defaultdict


# Load model the base wikipedia model
model = gensim.models.Word2Vec.load("../models/wiki-word2vec/wiki-en.word2vec.model")

# All available political views
#policital_spectrum = ["left",  "leftcenter", "center", "right-center", "right", "conspiracy"] 
policital_spectrum = ["left", "right"] 

for bias in policital_spectrum:
    print("Loading captions from bias:" + bias )
    with open("../data/processed/captions/"+ bias+ ".txt", "r") as file_reader:
        data = []
        for line in file_reader:
            data.append(line.strip().split(" "))
        #data = file_reader.read().split(" ")
        print("Training the model: " + bias )

        # Train the model
        model_wiki = copy.deepcopy(model)
        model_wiki.train(data,total_examples=len(data),epochs=model.iter)
        print("Saving the model: " + bias)
        model_wiki.save("../models/biases/captions/"+ bias+ ".model")


#cosine_similarity_prostitute = numpy.dot(model['woman'],model['prostitute'])/(numpy.linalg.norm(model['woman'])*numpy.linalg.norm(model['prostitute']))
#cosine_similarity_seductress =  numpy.dot(model['woman'],model['seductress'])/(numpy.linalg.norm(model['woman'])*numpy.linalg.norm(model['seductress']))
#print(cosine_similarity_prostitute,cosine_similarity_seductress)
#print(model.most_similar("woman"))
#print(model.wv["woman"])
###print(model.most_similar(positive=['woman', 'bike'], negative=['boy']))
###print("-----------------2 ")
