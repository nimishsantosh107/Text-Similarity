"""given 2 string compare how similar they are"""

#ORDER OF IMPORTANCE:
#     NOUN: noun
#     PROPN: proper noun
#     PRON: pronoun
#     VERB: verb
#     ADJ: adjective
#     ADV: adverb
#     NUM: numeral
#     SYM: symbol
#     X: other

#LIST OF FUNCTIONS:
#   tagSentence
#   reTagSentence
#   findSynonyms
#   compare
#   is_active
#   NCsplitOnVerb
#   checkOrderOfNoun
#   ACsplitOnVerb
#   checkOrderOfAdjective


##SPACY IMPORTS
import spacy
nlp = spacy.load("en_core_web_lg")
from spacy.matcher import Matcher
matcher = Matcher(nlp.vocab)
##NLTK IMPORTS
from nltk.corpus import wordnet
from num2words import num2words
##OTHER IMPORTS

#Gets sentence returns obj with POS tagged
def tagSentence(sentence):
    doc = nlp(sentence)
    obj = {}
    obj["NOUN"] = [token.lemma_.lower() for token in doc if token.pos_ == "NOUN"]
    obj["PROPN"] = [token.lemma_.lower() for token in doc if token.pos_ == "PROPN"]
    obj["PRON"] = [token.lemma_.lower() for token in doc if token.pos_ == "PRON"]
    obj["VERB"] = [token.lemma_.lower() for token in doc if token.pos_ == "VERB" and token.lemma_.lower() != "be"]
    obj["ADJ"] = [token.lemma_.lower() for token in doc if token.pos_ == "ADJ"]
    obj["ADV"] = [token.lemma_.lower() for token in doc if token.pos_ == "ADV"]
    obj["NUM"] = [token.lemma_.lower() for token in doc if token.pos_ == "NUM"]
    obj["SYM"] = [token.lemma_.lower() for token in doc if token.pos_ == "SYM"]
    obj["X"] = [token.lemma_.lower() for token in doc if token.pos_ == "X"]
    return obj

#Only for sent2
def reTagSentence(sentence2):
    obj = {}
    doc = nlp(sentence2)
    obj["NOUN"] = [token.lemma_.lower() for token in doc if token.pos_ == "NOUN"]
    obj["PROPN"] = [token.lemma_.lower() for token in doc if token.pos_ == "PROPN"]
    obj["PRON"] = [token.lemma_.lower() for token in doc if token.pos_ == "PRON"]
    obj["ADJ"] = [token.lemma_.lower() for token in doc if token.pos_ == "ADJ"]
    obj["VERB"] = [token.lemma_.lower() for token in doc if token.pos_ == "VERB" and token.lemma_.lower() != "be"]
    return obj

#Gets obj with POS tagged, returns obj with POS tagged + synonyms(only for obj2)
def findSynonyms(obj):
    #NOUN SYNONYMS FOUND IN COMPARE() ITSELF DUE TO NOUN ORDER CHECK
    #ADJ SYNONYMS FOUND IN COMPARE() ITSELF DUE TO ADJ ORDER CHECK
    #VERB
    if(len(obj["VERB"])>0):
        tempArr = []
        for word in obj["VERB"]:
            for syn in wordnet.synsets(word):
                for l in syn.lemmas():
                    tempArr.append(l.name())
        obj["VERB"] = list(set(obj["VERB"]+tempArr))
    
    #ADV   
    if(len(obj["ADV"])>0):
        tempArr = []
        for word in obj["ADV"]:
            for syn in wordnet.synsets(word):
                for l in syn.lemmas():
                    tempArr.append(l.name())
        obj["ADV"] = list(set(obj["ADV"]+tempArr))
    #X  
    if(len(obj["X"])>0):
        tempArr = []
        for word in obj["X"]:
            for syn in wordnet.synsets(word):
                for l in syn.lemmas():
                    tempArr.append(l.name())
        obj["X"] = list(set(obj["X"]+tempArr))
    return obj
     
#Comparison
def compare(obj1,obj2,sentence2):
    #original object 2
    obj2a = reTagSentence(sentence2)
    result = {}
    #NOUN, PROPN, PRON, VERB, ADJ, ADV, NUM, SYM, X - CRITICAL
    #NOUN
    if(len(obj1["NOUN"])>0):
        result["NOUN"] = 0
        status = 0
        for i in range(len(obj1["NOUN"])): 
            word1 = obj1["NOUN"][i]
            for j in range(len(obj2["NOUN"])): 
                word2 = obj2["NOUN"][j]
                tempArr = []
                for syn in wordnet.synsets(word2):
                    for l in syn.lemmas():
                        tempArr.append(l.name())
                for tempWord in tempArr:
                    if(word1 == tempWord):
                        status = 1
                        sentence2 = sentence2.replace(word2,word1)
                        result["NOUN"] += 1
                        break
            if(status == 1):
                status = 0
            else:
                break
    
    #PROPN      
    if(len(obj1["PROPN"])>0):
        result["PROPN"] = 0
        for i in range(len(obj1["PROPN"])): 
            word1 = obj1["PROPN"][i]
            for word2 in obj2["PROPN"]:
                if(word1 == word2):
                    result["PROPN"] += 1
    #PRON               
    if(len(obj1["PRON"])>0):
        result["PRON"] = 0
        for word1 in obj1["PRON"]:
            for word2 in obj2["PRON"]:
                if(word1 == word2):
                    result["PRON"] += 1
    #VERB
    if(len(obj1["VERB"])>0):
        result["VERB"] = 0
        for word1 in obj1["VERB"]:
            for word2 in obj2["VERB"]:
                if(word1 == word2):
                    result["VERB"] += 1 
    #ADJ 
    if(len(obj1["ADJ"])>0):
        result["ADJ"] = 0
        status = 0
        for i in range(len(obj1["ADJ"])): 
            word1 = obj1["ADJ"][i]
            for j in range(len(obj2["ADJ"])): 
                word2 = obj2["ADJ"][j]
                tempArr = []
                for syn in wordnet.synsets(word2):
                    for l in syn.lemmas():
                        tempArr.append(l.name())
                for tempWord in tempArr:
                    if(word1 == tempWord):
                        status = 1
                        sentence2 = sentence2.replace(word2,word1)
                        result["ADJ"] += 1
                        break

    #ADV
    if(len(obj1["ADV"])>0):
        result["ADV"] = 0
        for word1 in obj1["ADV"]:
            for word2 in obj2["ADV"]:
                if(word1 == word2):
                    result["ADV"] += 1 
    #NUM     
    if(len(obj1["NUM"])>0):
        #NUM2WORD
        for i in range(len(obj1["NUM"])):
            if(obj1["NUM"][i].isdigit()):
                obj1["NUM"][i] = num2words(obj1["NUM"][i])
        for i in range(len(obj2["NUM"])):
            if(obj2["NUM"][i].isdigit()):
                obj2["NUM"][i] = num2words(obj2["NUM"][i])
        #NORMAL
        result["NUM"] = 0
        for word1 in obj1["NUM"]:
            for word2 in obj2["NUM"]:
                if(word1 == word2):
                    result["NUM"] += 1
    #SYM
    if(len(obj1["SYM"])>0):
        result["SYM"] = 0
        for word1 in obj1["SYM"]:
            for word2 in obj2["SYM"]:
                if(word1 == word2):
                    result["SYM"] += 1
    #X-OTHERS
    if(len(obj1["X"])>0):
        result["X"] = 0
        for word1 in obj1["X"]:
            for word2 in obj2["X"]:
                if(word1 == word2):
                    result["X"] += 1
    tempObj = {
        'NOUN':len(obj1['NOUN']),
        'PROPN':len(obj1['PROPN']),
        'PRON':len(obj1['PRON']),
        'VERB':len(obj1['VERB']),
        'ADJ':len(obj1['ADJ']),
        'ADV':len(obj1['ADV']),
        'SYM':len(obj1['SYM']),
        'NUM':len(obj1['NUM']),
        'X':len(obj1['X'])
    }
    res = {
        'teachArr':tempObj,
        'studArr':result
    }
    #TUPLE UNPACK AND GET BOTH VALUES
    return res,sentence2

#Is active
def is_active(sentence):
    doc = nlp(sentence)
    passive_rule = [{'DEP': 'nsubjpass'}, {'DEP': 'aux', 'OP': '*'}, {'DEP': 'auxpass'}, {'TAG': 'VBN'}]
    matcher.add('Passive', None, passive_rule)
    matches = matcher(doc)
    if matches:
        return False
    else:
        return True

#These sentences will be with replaced words for sent2 alone
#For NOUN check
def NCsplitOnVerb(sentence):
    sent = {}
    doc = nlp(sentence)
    sent["TYPE"] = is_active(sentence)
    sent["NPV"] = [token.lemma_.lower() for token in doc if token.pos_=="NOUN" 
     or token.pos_=="PRON" 
     or token.pos_=="PROPN"
     or token.pos_=="VERB" and token.lemma_.lower()!="be"]
    sent["NPV"] = ' '.join(sent["NPV"])
    sent["V"] = [token.lemma_.lower() for token in doc if token.pos_=="VERB" and token.lemma_.lower()!="be"]
    sent["NP"]= sent["NPV"].split(sent["V"][0])
    sent["NP"] = [word.replace(' ','') for word in sent["NP"]]
    sent["NP"] = [''.join(sorted(word)) for word in sent["NP"]]
    return sent

#Check order of appearance of a noun
def checkOrderOfNoun(sent1,sent2):
    sent1obj = NCsplitOnVerb(sent1)
    sent2obj = NCsplitOnVerb(sent2)
    index1 = []
    index2 = []
    for i in range(len(sent1obj["NP"])):
        index1.append(i)
        try:
            index2.append(sent2obj["NP"].index(sent1obj["NP"][i]))
        except:
            return False
    if(sent1obj["TYPE"]==sent2obj["TYPE"]):
        #len(index1) = len(index2)
        for i in range(len(index1)):
            if(index1[i]!=index2[i]):
                return False
        return True
    elif(sent1obj["TYPE"]!=sent2obj["TYPE"]):
        for i in range(len(index1)):
            if(index1[i]==index2[i]):
                return False
        return True

#For ADJ check
def ACsplitOnVerb(sentence):
    sent = {}
    doc = nlp(sentence)
    sent["TYPE"] = is_active(sentence)
    sent["NPVA"] = [token.lemma_.lower() for token in doc if token.pos_=="NOUN" 
     or token.pos_=="PRON" 
     or token.pos_=="PROPN"
     or token.pos_=="ADJ"
     or token.pos_=="VERB" and token.lemma_.lower()!="be"]
    sent["NPVA"] = ' '.join(sent["NPVA"])
    sent["V"] = [token.lemma_.lower() for token in doc if token.pos_=="VERB" and token.lemma_.lower()!="be"]
    sent["NPA"]= sent["NPVA"].split(sent["V"][0])
    sent["NPA"] = [word.replace(' ','') for word in sent["NPA"]]
    sent["NPA"] = [''.join(sorted(word)) for word in sent["NPA"]]
    return sent

#Check order of appearance of an adjective
def checkOrderOfAdjective(sent1,sent2):
    sent1obj = ACsplitOnVerb(sent1)
    sent2obj = ACsplitOnVerb(sent2)
    index1 = []
    index2 = []
    for i in range(len(sent1obj["NPA"])):
        index1.append(i)
        try:
            index2.append(sent2obj["NPA"].index(sent1obj["NPA"][i]))
        except:
            return False
    if(sent1obj["TYPE"]==sent2obj["TYPE"]):
        #len(index1) = len(index2)
        for i in range(len(index1)):
            if(index1[i]!=index2[i]):
                return False
        return True
    elif(sent1obj["TYPE"]!=sent2obj["TYPE"]):
        for i in range(len(index1)):
            if(index1[i]==index2[i]):
                return False
        return True