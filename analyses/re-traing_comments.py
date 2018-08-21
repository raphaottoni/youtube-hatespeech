from gensim import corpora, models, similarities
import json
import numpy
import random
import gensim, copy
from collections import defaultdict


channels_comments = defaultdict(list)
old_channel = ""
#
for line in open("../../data/comments-filtered.jsonl"):
  data = json.loads(line)

  current_channel = data["channel_id"]

  if data["comment_text"] != "":
    for sentence in data["comment_text"].split("\n"):
      channels_comments["all"].append(sentence.split(" "))
      channels_comments[current_channel].append(sentence.split(" "))

# Load model
model = gensim.models.Word2Vec.load("../../data/wikipedia_model/wiki.en.word2vec.model")

#cosine_similarity_prostitute = numpy.dot(model['woman'],model['prostitute'])/(numpy.linalg.norm(model['woman'])*numpy.linalg.norm(model['prostitute']))
#cosine_similarity_seductress =  numpy.dot(model['woman'],model['seductress'])/(numpy.linalg.norm(model['woman'])*numpy.linalg.norm(model['seductress']))
#print(cosine_similarity_prostitute,cosine_similarity_seductress)
#print(model.most_similar("woman"))


# for each channel print the change in the woman vector:
for channel_id in channels_comments:
    if channel_id != "all":
        print("trainando o modelo " + channel_id + "_comments")
        # Train the model
        model_wiki = copy.deepcopy(model)
        model_wiki.train(channels_comments[channel_id],total_examples=model.corpus_count,epochs=model.iter)
        model_wiki.save("./modelos/"+channel_id+"_comments")





#print(model.wv["woman"])
###print(model.most_similar(positive=['woman', 'bike'], negative=['boy']))
###print("-----------------2 ")
##
###for i in range(0,15):
#for i in range(0,1):
#    print(i+1)
#
#    #model.build_vocab(channels_transcripts["all"], update=True)
#    model.train(channels_transcripts["all"],total_examples=model.corpus_count,epochs=model.iter)
#    depois = model.wv["woman"]
#    print(model.most_similar("woman"))
#print(depois)
#print(antes)
#print( str(antes) == str(depois))
#print(str(depois - antes))
#
##model.train(channels_transcripts["all"], total_examples=len(channels_transcripts["all"]))
##model.train(channels_transcripts["all"],total_examples=model.corpus_count,epochs=model.iter)
###model.train(channels_transcripts["all"])
##
##print(model.most_similar("woman"))
##print(model.most_similar(positive=['woman', 'bike'], negative=['boy']))
##print("-----------------3 ")
##model.train(channels_transcripts["all"],total_examples=model.corpus_count,epochs=model.iter)
##print(model.most_similar("woman"))
##print(model.most_similar(positive=['woman', 'bike'], negative=['boy']))



#result = (depois - antes)/antes
#
#result_sorted = sorted( [ (i, result[i]) for i in range(len(result)) ],
#                        key=lambda a:a[1],
#                        reverse=True)
#
#for pos, (i, value) in enumerate(result_sorted,1):
#    if i in [121, 578,570,588,235]:
#        print(pos, i ,value)
#


