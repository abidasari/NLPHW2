#!/usr/bin/python
import os
import fnmatch
import re
import sys
import math


fileobject = open("model.txt", "r")


vocabulary = eval(fileobject.readline())
priors = eval(fileobject.readline())
condprob_dec = eval(fileobject.readline())
condprob_tru = eval(fileobject.readline())
condprob_neg_pol = eval(fileobject.readline())
condprob_pos_pol = eval(fileobject.readline())

fileobject.close()

classes = ["positive_polarity", "negative_polarity", "deceptive", "truthful"]

# basepath = "./op_spam_test/"

basepath = str(sys.argv[1])
# print(basepath)

droplist = ["a","am","are","at","and","as","be","but","by","do","for","had", "has","he","her","him","his","i","it","if","is","me","my","of","on","or","our","you","with","who","which","were","we","was","up","to","too","this","they","then","there","them","the","so","she"]

score = {}


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
    print("processing file: ", filename)
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

def dealwithnoword(condprobdict, wordtoken):
    if wordtoken in condprobdict:
        return condprobdict[wordtoken]
    else:
        return 0



def classify4way(filepath):
    tokens_in_file = processfile(filename)
    filedic = {}
    filedic = addtodict(filedic, tokens_in_file)
    for eachclass in classes:
        score[eachclass] = math.log(priors[eachclass], 10)
        for eachtoken in filedic:
            if eachclass == classes[0]:
                switch = dealwithnoword(condprob_pos_pol, eachtoken)
                if switch == 0:
                    continue
                else:
                    score[eachclass] += math.log(switch, 10)#math.log(condprob_pos_pol[eachtoken])
            elif eachclass == classes[1]:
                switch = dealwithnoword(condprob_neg_pol, eachtoken)
                if switch == 0:
                    continue
                else:
                    score[eachclass] += math.log(switch, 10)#math.log(condprob_neg_pol[eachtoken])
            elif eachclass == classes[2]:
                switch = dealwithnoword(condprob_dec, eachtoken)
                if switch == 0:
                    continue
                else:
                    score[eachclass] += math.log(switch, 10)#math.log(condprob_dec[eachtoken])
            elif eachclass == classes[3]:
                switch = dealwithnoword(condprob_tru, eachtoken)
                if switch == 0:
                    continue
                else:
                    score[eachclass] += math.log(switch, 10)#math.log(condprob_tru[eachtoken])
    return score


def classify2way(filepath):
    tokens_in_file = processfile(filename)
    filedic = {}
    filedic = addtodict(filedic, tokens_in_file)
    for eachclass in ["positive_polarity", "negative_polarity"]:
        score[eachclass] = math.log(priors[eachclass], 10)
        for eachtoken in filedic:
            if eachclass == classes[0]:
                switch = dealwithnoword(condprob_pos_pol, eachtoken)
                if switch == 0:
                    continue
                else:
                    score[eachclass] += math.log(switch, 10)#math.log(condprob_pos_pol[eachtoken])
            elif eachclass == classes[1]:
                switch = dealwithnoword(condprob_neg_pol, eachtoken)
                if switch == 0:
                    continue
                else:
                    score[eachclass] += math.log(switch, 10)#math.log(condprob_neg_pol[eachtoken])
            elif eachclass == classes[2]:
                switch = dealwithnoword(condprob_dec, eachtoken)
                if switch == 0:
                    continue
                else:
                    score[eachclass] += math.log(switch, 10)#math.log(condprob_dec[eachtoken])
            elif eachclass == classes[3]:
                switch = dealwithnoword(condprob_tru, eachtoken)
                if switch == 0:
                    continue
                else:
                    score[eachclass] += math.log(switch, 10)#math.log(condprob_tru[eachtoken])
    return score




outfile = open("nboutput.txt", "w")
output = ""
for root, dirnames, filenames in os.walk(r"."+basepath):
    for filename in fnmatch.filter(filenames, '*.txt'):
        filename = os.path.join(root, filename)
        _4way = classify4way(filename)
        # _2way = classify2way(filename)
        output = []
        if _4way["deceptive"] > _4way["truthful"]:
            class1 = "deceptive"
        else:
            class1 = "truthful"
        if _4way["positive_polarity"] > _4way["negative_polarity"]:
            class2 = "positive_polarity"
        else:
            class2 = "negative_polarity"
        output = class1 + " " + class2 + " " + filename + "\n"
        print(output)

        outfile.write(output)

        # print(_4way)
        # print (output)

outfile.close()
