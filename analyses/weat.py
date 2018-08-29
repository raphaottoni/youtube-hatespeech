from gensim import corpora, models, similarities
import json
import numpy
import random
import csv
import itertools
import gensim, copy
from collections import defaultdict
import glob, os

target_words = {}
attribute_words= {}
weats_name = []

# 1 WEAT Immigrants
target_words["1_a"] = ["immigrant", "migrant"]
target_words["1_b"] = ["citizen", "native"]
attribute_words["1_a"]  = ["bad", "burden", "pirate", "plague", "taker", "thief"]
attribute_words["1_b"]  = ["good", "honest", "maker", "rightful"]
weats_name.append("Immigrants")

# 2 WEAT Muslims
target_words["2_a"] = ["islamism", "muhammed", "muslim", "quran"]
target_words["2_b"] = ["bible", "christian", "christianity", "jesus"]
attribute_words["2_a"]  = ["assassin", "attack", "bomb", "death", "murder", "radical", "terrorist"]
attribute_words["2_b"]  = ["compassionate", "gentle", "humane", "kind", "tolerant"]
weats_name.append("Muslims")

# 3 WEAT LGBT people
target_words["3_a"] = ["bisexual", "gay", "homosexual", "lesbian"]
target_words["3_b"] = ["het", "hetero", "heterosexual", "straight"]
attribute_words["3_a"]  = ["immoral", "outrageous", "promiscuous", "revolting", "sinner"]
attribute_words["3_b"]  = ["moral", "natural", "normal"]
weats_name.append("LGBT People")

# 4 WEAT math arts male_female
target_words["4_a"]  = ["math","algebra","geometry","calculus","equations","computation","numbers" ]
target_words["4_b"]  = ["poetry","art","dance","literature","novel","symphony","drama","sculpture" ]
attribute_words["4_a"]  = ["male","man","boy","brother","he","him","his", "son"]
attribute_words["4_b"]  = ["female","woman","girl","sister","she","her","hers", "daughter"]
weats_name.append("Math Arts")

# 5 WEAT  Judaism and Christianity
# Religious  Judaism Christianity
target_words["5_a"]  = ["church","bible","christian","christianity"]
target_words["5_b"]  = ["synagogue","torah","jew","judaism"]
attribute_words["5_a"]  = ["terrific","delight","celebrate","glad","beautiful","appealing", "pleasure", "enjoy" ]
attribute_words["5_b"]  = ["hate","angry","detest","despise","dirty","humiliate","pain", "horrible"]
weats_name.append("Jewish")

# 6 WEAT  African American 1
target_words["6_a"]  = ["brad", "brendan", "geoffrey", "greg", "brett", "jay",
                        "matthew", "neil", "todd", "allison", "anne", "carrie",
                        "emily", "jill", "laurie", "kristen", "meredith", "sarah"]

target_words["6_b"]  = ["darnell", "hakim", "jermaine", "kareem", "jamal",
                        "leroy", "rasheed", "tremayne", "tyrone", "aisha", 
                        "ebony", "keisha", "kenya", "latonya", "lakisha", 
                        "latoya", "tamika", "tanisha"]
attribute_words["6_a"]  = [ "joy", "love", "peace", "wonderful", "pleasure", "friend", "laughter", "happy"]
attribute_words["6_b"]  = ["agony", "terrible", "horrible", "nasty", "evil", "war", "awful","failure"]
weats_name.append("African - 1")

# 7 WEAT  African American 2
target_words["7_a"]  = ["brad", "brendan", "geoffrey", "greg", "brett", "jay",
                        "matthew", "neil", "todd", "allison", "anne", "carrie",
                        "emily", "jill", "laurie", "kristen", "meredith", "sarah"]

target_words["7_b"]  = ["darnell", "hakim", "jermaine", "kareem", "jamal",
                        "leroy", "rasheed", "tremayne", "tyrone", "aisha", 
                        "ebony", "keisha", "kenya", "latonya", "lakisha", 
                        "latoya", "tamika", "tanisha"]
attribute_words["7_a"]  = ["caress", "freedom", "health", "love", "peace",
                            "cheer", "friend", "heaven", "loyal", "pleasure", 
                            "diamond", "gentle", "honest", "lucky", "rainbow",
                            "diploma", "gift", "honor", "miracle", "sunrise",
                            "family", "happy","laughter","paradise", "vacation"] 

attribute_words["7_b"]  = ["abuse", "crash", "filth", "murder", "sickness",
                            "accident", "death", "grief", "poison", "stink", 
                            "assault", "disaster", "hatred","pollute", "tragedy", 
                            "bomb", "divorce", "jail", "poverty", "ugly", "cancer",
                            "evil", "kill", "rotten","vomit"]
weats_name.append("African - 2")






def statistic_test(X,Y,A,B,M):
    result = 0.0
    sum_X = 0.0
    sum_Y = 0.0

    for word_X in X:
        sum_X += sub_statistic_test(word_X, A,B,M)
    for word_Y in Y:
        sum_Y += sub_statistic_test(word_Y, A,B,M)

    return (sum_X - sum_Y)

def sub_statistic_test(w,A,B,M):
    result = 0.0
    sum_cos_A = 0.0
    sum_cos_B = 0.0

    for word_A in A:
        sum_cos_A += numpy.dot(M[w],M[word_A])/(numpy.linalg.norm(M[w])*numpy.linalg.norm(M[word_A]))
    for word_B in B:
        sum_cos_B += numpy.dot(M[w],M[word_B])/(numpy.linalg.norm(M[w])*numpy.linalg.norm(M[word_B]))

    return (sum_cos_A/len(A) - sum_cos_B/len(B))

def effect_size(x_words,y_words,a_attributes,b_attributes,M):
    # Effect size
    test_x = 0.0
    test_y = 0.0
    samples = []

    for word_x in target_words[x_words]:
        test_x += sub_statistic_test(word_x,attribute_words[a_attributes],attribute_words[b_attributes],M)
        samples.append(sub_statistic_test(word_x,attribute_words[a_attributes],attribute_words[b_attributes],M))

    for word_y in target_words[y_words]:
        test_y += sub_statistic_test(word_y,attribute_words[a_attributes],attribute_words[b_attributes],M)
        samples.append(sub_statistic_test(word_y,attribute_words[a_attributes],attribute_words[b_attributes],M))

    mean_x =  test_x/len(target_words[x_words])
    mean_y =  test_y/len(target_words[y_words])

    std_dev = numpy.std(samples)
    effect_size =  (mean_x - mean_y)/std_dev
    return effect_size


# P-Value
def p_value(X,Y,A,B,model):
    null_hipotese_evidance = 0.0
    number_permitations = 0.0

    # Finds the biggest possible set of the same size for the two classes
    X_size =  len(target_words[X])
    Y_size =  len(target_words[Y])
    size = max(X_size, Y_size)
    union = set(target_words[X] + target_words[Y])
    random_test_statistic_values = []
    test_statistic_value = statistic_test(target_words[X],target_words[Y],attribute_words[A],attribute_words[B],model)

    if (Y_size + X_size) < 14:
        # there will be less than 5000 combinations
        permutations = itertools.combinations(union,size)

        for i,permutation in enumerate(permutations):
            x_i = permutation
            y_i = union - set(permutation)
            test_value = statistic_test(x_i,y_i,attribute_words[A],attribute_words[B],model)

            random_test_statistic_values.append(test_value)
            if( test_value > test_statistic_value):
                null_hipotese_evidance += 1
            number_permitations += 1

        #print("null hipotese_evidance: " + str(null_hipotese_evidance))
        #print("num_permutations: " + str(number_permitations))
        #print("P-Value():")
        #print(null_hipotese_evidance/number_permitations)
        p_value_result =  null_hipotese_evidance/number_permitations
        #print("enviando " + str(p_value_result))
        return(p_value_result)

    else:
        # There will be more than 5000, thus we should randomize
        print("Generating 5k random")
        classes = target_words[X] + target_words[Y]

        for i in range(5000):
          random.shuffle(classes)
          x_i = classes[:size]
          y_i = classes[size+1:]
          test_value = statistic_test(x_i,y_i,attribute_words[A],attribute_words[B],model)
          # save the valus to be used for each channel
          random_test_statistic_values.append(test_value)
          if( test_value > test_statistic_value):
            null_hipotese_evidance += 1
          number_permitations += 1
          #if number_permitations % 100 == 0:
          #    print(number_permitations)

        #print("null hipotese_evidance: " + str(null_hipotese_evidance))
        #print("num_permutations: " + str(number_permitations))
        #print("P-Value(english):")
        #print(null_hipotese_evidance/number_permitations)
        p_value_result =  null_hipotese_evidance/number_permitations
        return(p_value_result)



def main():

    # Which models to load
    political_biases_model = ["left", "leftcenter", "center", "right-center", "right"]
    model_types = [ "captions", "comments"]

    
    # list of WEATs to execute
    weats = [1,2,3]
    
    with open("../data/weat/weat_results.csv", "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(["channel","WEAT","political_bias", "source", "effect_size", "p_value"])
    
        #for political_bias in political_biases_model:
        #    for model_type in model_types: 

        #        for file in os.listdir("../models/biases/" + model_type + "/" + political_bias):
        #            if file.endswith(".model"):
        #                print("Loading " + political_bias + " word2vec " +  model_type +  " model " + "(" + file + ")") 
        #                model = gensim.models.Word2Vec.load("../models/biases/" + model_type + "/" + political_bias+ "/" + file)
        #                #model = gensim.models.Word2Vec.load("../models/wiki-word2vec/wiki-en.word2vec.model")
        #                print("Executing WEATs on current model" )
        #                for weat_number in weats:
        #                    X =  str(weat_number) + "_a"
        #                    Y =  str(weat_number) + "_b"
        #                    A =  str(weat_number) + "_a"
        #                    B =  str(weat_number) + "_b"
        #                    ##  Effect size of the base model
        #                    effect_size_result =  effect_size(X,Y,A,B,model)
        #                    print("Effect-Size("+str(weat_number)+ "):" + str(effect_size_result))
        #                    p_value_result  =  p_value(X,Y,A,B,model)
        #                    print("P-value("+str(weat_number)+ "):" + str(p_value_result))
        #                    writer.writerow([file[:-6],weats_name[weat_number -1],political_bias , model_type, effect_size_result, p_value_result])

        # Add the baseline weat results the wikipedia model
        print("Loading the wiki base model")
        model = gensim.models.Word2Vec.load("../models/wiki-word2vec/wiki-en.word2vec.model")
        print("Executing WEATs on current model" )
        for weat_number in weats:
            X =  str(weat_number) + "_a"
            Y =  str(weat_number) + "_b"
            A =  str(weat_number) + "_a"
            B =  str(weat_number) + "_b"
            ##  Effect size of the base model
            effect_size_result =  effect_size(X,Y,A,B,model)
            print("Effect-Size("+str(weat_number)+ "):" + str(effect_size_result))
            p_value_result  =  p_value(X,Y,A,B,model)
            print("P-value("+str(weat_number)+ "):" + str(p_value_result))
            writer.writerow(["wikipedia",weats_name[weat_number -1], "wiki", "wiki", effect_size_result, p_value_result])

 


if __name__ == "__main__":
    main()
