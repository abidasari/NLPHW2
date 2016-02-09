#!/usr/bin/python
import fnmatch
import os
import re
import sys

droplist = ["a","am","are","at","and","as","be","but","by","do","for","had", "has","he","her","him","his","i","it","if","is","me","my","of","on","or","our","you","with","who","which","were","we","was","up","to","too","this","they","then","there","them","the","so","she"]

def droppuncs(tokenlist):
    output = []
    for token in tokenlist:
        token = re.sub('[^a-zA-Z0-9\n\-]', '', token)
        output.append(token)
    return output

def dropstops(tokenlist):
    output = []
    for token in tokenlist:
        if token in droplist:
            continue
        else:
            output.append(token)
    return output

def processfile(filename):
    fileobj = open(filename, "r")
    filecontent = fileobj.read()
    filecontent = filecontent.lower()
    tokens = filecontent.split()
    tokenss = droppuncs(tokens)
    tokensss = dropstops(tokenss)
    fileobj.close()
    return tokensss

def addtodict(dictionary, tokenlist):
    output = dictionary
    for token in tokenlist:
        if token != '':
            if token in output :
                output[token]  += 1
            else:
                output[token] = 1
    return output

def dict_size(vocab):
    output = 0
    for word in vocab:
        output += vocab[word]
    return output

#the classes in the corpus
classes = ["positive_polarity", "negative_polarity", "deceptive", "truthful"]

# basepath = "./op_spam_train/"

basepath = str(sys.argv[1])

print(str(sys.argv[0]) , "\n", str(sys.argv[1]), "\n", str(sys.argv[2]))
# #paths ot the training data
# pos_pol = r"."+basepath+"/positive_polarity/deceptive_from_MTurk/"
# pos_pol_truthful = r"."+basepath+"/positive_polarity/truthful_from_TripAdvisor/"
# neg_pol = r"."+basepath+"/negative_polarity/deceptive_from_MTurk/"
# neg_pol_truthful = r"."+basepath+"/negative_polarity/truthful_from_Web/"


pos_pol = r"."+basepath+"/positive_polarity/deceptive_from_MTurk/"
pos_pol_truthful = r"."+basepath+"/positive_polarity/truthful_from_TripAdvisor/"
neg_pol = r"."+basepath+"/negative_polarity/deceptive_from_MTurk/"
neg_pol_truthful = r"."+basepath+"/negative_polarity/truthful_from_Web/"


path_directory = { classes[0]: [pos_pol,pos_pol_truthful],
                   classes[1]: [neg_pol,neg_pol_truthful],
                   classes[2]: [pos_pol,neg_pol],
                   classes[3]: [pos_pol_truthful,neg_pol_truthful] }

class_doc_count = { classes[0]: 0,
                    classes[1]: 0,
                    classes[2]: 0,
                    classes[3]: 0 }


pos_pol_dic = {}
neg_pol_dic = {}
truthful_dic = {}
deceptive_dic = {}
vocabulary = {}

for key, value in path_directory.items():
    print("Building vocab for", key)
    for path in value:

        print("Building vocab for ", key ,"in path ", path)

        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, '*.txt'):
                filename = os.path.join(root, filename)
                # print("currently reading: ", filename)
                tokens_in_file = processfile(filename)
                if(key == classes[0]):
                    pos_pol_dic = addtodict(pos_pol_dic, tokens_in_file)
                    class_doc_count[classes[0]] += 1
                    vocabulary = addtodict(vocabulary, tokens_in_file)
                elif(key == classes[1]):
                    neg_pol_dic = addtodict(neg_pol_dic, tokens_in_file)
                    class_doc_count[classes[1]] += 1
                    vocabulary = addtodict(vocabulary, tokens_in_file)
                elif(key == classes[2]):
                    deceptive_dic = addtodict(deceptive_dic, tokens_in_file)
                    class_doc_count[classes[2]] += 1
                    vocabulary = addtodict(vocabulary, tokens_in_file)
                elif(key == classes[3]):
                    truthful_dic = addtodict(truthful_dic, tokens_in_file)
                    class_doc_count[classes[3]] += 1
                    vocabulary = addtodict(vocabulary, tokens_in_file)

                # print("about to read next file for ", key)
                # inp = input("press enter to continue...")

    # str = input("continue?")

classprior = {}
Tct_pos_pol = {}
Tct_neg_pol = {}
Tct_tru = {}
Tct_dec = {}
condprob = {}
vocab_size = dict_size(vocabulary)


condprob_pos_pol = {}
condprob_neg_pol = {}
condprob_tru = {}
condprob_dec = {}



sum_of_all_docs = 0
for clas in classes:
    sum_of_all_docs += class_doc_count[clas]
# print(sum_of_all_docs)

for each_class in classes:
    classprior[each_class] = class_doc_count[each_class] / sum_of_all_docs
    if each_class == "positive_polarity":
        for word in vocabulary:
            if word in pos_pol_dic:
                Tct_pos_pol[word] = pos_pol_dic[word]
            else:
                Tct_pos_pol[word] = 0
        sigma_term = dict_size(Tct_pos_pol)
        mod_V = len(vocabulary)
        for word in vocabulary:
            nmer = Tct_pos_pol[word] + 1
            denr = mod_V + sigma_term
            condprob_pos_pol[word] = nmer / denr
    elif each_class == "negative_polarity":
        for word in vocabulary:
            if word in neg_pol_dic:
                Tct_neg_pol[word] = neg_pol_dic[word]
            else:
                Tct_neg_pol[word] = 0
        sigma_term = dict_size(Tct_neg_pol)
        mod_V = len(vocabulary)
        for word in vocabulary:
            nmer = Tct_neg_pol[word] + 1
            denr = mod_V + sigma_term
            condprob_neg_pol[word] = nmer / denr
    elif each_class == "truthful":
        for word in vocabulary:
            if word in truthful_dic:
                Tct_tru[word] = truthful_dic[word]
            else:
                Tct_tru[word] = 0
        sigma_term = dict_size(Tct_tru)
        mod_V = len(vocabulary)
        for word in vocabulary:
            nmer = Tct_tru[word] + 1
            denr = mod_V + sigma_term
            condprob_tru[word] = nmer / denr
    elif each_class == "deceptive":
        for word in vocabulary:
            if word in deceptive_dic:
                Tct_dec[word] = deceptive_dic[word]
            else:
                Tct_dec[word] = 0
        sigma_term = dict_size(Tct_dec)
        mod_V = len(vocabulary)
        for word in vocabulary:
            nmer = Tct_dec[word] + 1
            denr = mod_V + sigma_term
            condprob_dec[word] = nmer / denr


fo = open('model.txt', 'w')

fo.write(str(vocabulary))
fo.write("\n")

fo.write(str(classprior))
fo.write("\n")

fo.write(str(condprob_dec))
fo.write("\n")

fo.write(str(condprob_tru))
fo.write("\n")

fo.write(str(condprob_neg_pol))
fo.write("\n")

fo.write(str(condprob_pos_pol))

fo.close()
