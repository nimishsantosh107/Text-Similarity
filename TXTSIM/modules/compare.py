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
#   resolve_co_reference
#   chunk ----
#   simCheck
#   tagSentence
#   reTagSentence
#   findSynonyms
#   compare - 
#   is_active
#   NCsplitOnVerb
#   checkOrderOfNoun - 
#   ACsplitOnVerb
#   checkOrderOfAdjective - 
#   compareMain


##SPACY IMPORTS
import spacy
nlp = spacy.load("en_core_web_lg")
from spacy.matcher import Matcher
matcher = Matcher(nlp.vocab)
##NLTK IMPORTS
from nltk.corpus import wordnet
from num2words import num2words
##OTHER IMPORTS
import json


###chunker.py
def resolve_co_reference(text):
    import neuralcoref
    nlpa = spacy.load("en_core_web_sm")
    '''
    The coref model calculates the probabilities of links between The main occurence and a reference of that
    main occurence and on the basis of that replaces every reference with the main occurence it is referring to
    '''
    coref = neuralcoref.NeuralCoref(nlpa.vocab) # initialize the neuralcoref with spacy's vocabulary
    nlpa.add_pipe(coref, name='neuralcoref') #add the coref model to pipe
    doc = nlpa(text)
    if doc._.has_coref: ## if coreference is possible
        return doc._.coref_resolved ##return the sentence with all references replaced
    else:
        return text ##else return text as it is 

def chunk(sent):
    sent=resolve_co_reference(sent)
    conj = set(('and', 'or' ,'but','while','so','because','where','however','whereas'))
    beverbs=set(('is','was','are','were'))
    wdt=set(('which','that'))
    l=[1,2,3]
    tagged_list=[[]]
    i=0
    doc=nlp(sent)
    for token in doc:
        # if (token.lemma_=="be"):
        #   l[0]="be"
        # else:
        #   l[0]=token.text
        l[0]=token.text
        l[1]=token.tag_
        if(token.dep_=='nsubj' and token.tag_.startswith("W")==False):
            l[2]=1
        else:
            l[2]=0
        tagged_list.insert(i,l)
        l=[1,2,3]
        i=i+1

    noun=-1
    i=0
    while(i<len(tagged_list)-1):
        if(tagged_list[i][1].find("NN")!=-1):
            noun=i
        if(tagged_list[i][0]in beverbs):
            if(i<len(tagged_list)-2 and tagged_list[i+1][1].startswith("V") and not tagged_list[i+1][1].startswith("VBG")):
                tagged_list[noun][2]=3
        i=i+1
    #print(tagged_list)

    n=[[]]
    ind=0
    ind2=-1
    i=0
    subj=""
    lis=[]
    flag=-1
    find=-1
    subj_type=-1
    while(i<len(tagged_list)-1):
        if(tagged_list[i][0] in wdt and i+1<len(tagged_list)-1 and tagged_list[i+1][1].find("VB")!=-1):
            if(i-2>=0 and tagged_list[i-1][0]==","):
                tagged_list[i][0]=tagged_list[i-2][0]
                tagged_list[i][2]=1
                tagged_list[i][1]=tagged_list[i-2][1]
            else:
                tagged_list[i-1][2]=1
            subj=tagged_list[i-1][0]
        i=i+1
    i=0
    while(i<len(tagged_list)-1):
        if(tagged_list[i][2]==1 or tagged_list[i][2]==3):
            subj=tagged_list[i][0]
            subj_type=tagged_list[i][2]
        if(tagged_list[i][1]=="CC"  or tagged_list[i][0] in conj or tagged_list[i][0]=="," or tagged_list[i][0]==";" or tagged_list[i][0]=="." or(tagged_list[i][0]in wdt and i+1<len(tagged_list)-1 and tagged_list[i+1][1].find("VB")==-1)):
            j=i+1
            while(j<len(tagged_list)-1 and tagged_list[j][1].find("NN")==-1 and tagged_list[j][1].find("VB")==-1):
                j=j+1
            if(j<len(tagged_list)-1and tagged_list[j][1].find("NN")!=-1):
                
                if((tagged_list[j][2]==1 or tagged_list[j][2]==3)):
                    if(ind2!=-1 and ind2!=ind):
                        find=find+1                 
                        while(find<len(tagged_list)-1 and (tagged_list[find][1]!="CC"  and tagged_list[find][0] not in conj and tagged_list[find][0]!="," and tagged_list[find][0]!=";" and tagged_list[find][0]!="." and(tagged_list[i][0]not in wdt or (i+1<len(tagged_list)-1 and tagged_list[i+1][1].find("VB")!=-1)))):
                            find=find+1
                        n.append([tagged_list[x][0] for x in range(ind2,i) if(x not in range(ct,find+1))])
                        ind2=-1
                    else:
                        for x in range(ind,i):
                            if(tagged_list[x][1]=="CC"  or tagged_list[x][0] in conj or tagged_list[x][0]=="," or tagged_list[x][0]==";" or tagged_list[x][0]=="." or (tagged_list[x][0]in wdt and x+1<len(tagged_list)-1 and tagged_list[x+1][1].find("VB")==-1) ):
                                if(x>ind and x<i-1):
                                    if((tagged_list[x-1][2]== 1 or tagged_list[x-1][2]==2)):
                                        y=x+1
                                        while(y<len(tagged_list)-1 and tagged_list[y][1].find("NN")==-1 and tagged_list[y][1].find("VB")==-1):
                                            y=y+1
                                        if(tagged_list[y][2]==1 or tagged_list[y][2]==2 or tagged_list[y][2]==3):
                                            if(len(lis)==0):
                                                lis.append(x-1)
                                            lis.append(y)
                        for l in range(len(lis)):
                            n.append([tagged_list[x][0] for x in range(ind,i) if(x == lis[l] or x>lis[len(lis)-1]) or (l==0 and x<lis[0]) or (l>0 and x>lis[l-1]) and x<=lis[l]])
                        if(len(lis)==0):
                            n.append([tagged_list[x][0] for x in range(ind,i)])
                    lis=[]
                    ind =i+1
                elif(i-1>=0 and (tagged_list[i-1][2]==1 or tagged_list[i-1][2]==2 or tagged_list[i-1][2]==3)):
                    tagged_list[j][2]=2
                    subj=subj+" "+tagged_list[i][0]+" "+tagged_list[j][0]

                else:
                    if(ind2==-1):
                        ind2=ind
                    ct=ind2
                    while(ct<i-1 and ((tagged_list[ct][1].find("NN")==-1 or tagged_list[ct][1].find("VB")==-1) or (tagged_list[ct][2]==1 or tagged_list[ct][2]==2 or tagged_list[ct][2]==3 ))):
                        ct=ct+1
                    if(flag!=ind2):
                        n.append([tagged_list[x][0] for x in range(ind2,i)])
                        flag=ind2
                        find=ct
                    else:
                        find=find+1                 
                        while(find<len(tagged_list)-1 and (tagged_list[find][1]!="CC"  and tagged_list[find][0] not in conj and tagged_list[find][0]!="," and tagged_list[find][0]!=";" and tagged_list[find][0]!="." and(tagged_list[i][0]not in wdt or (i+1<len(tagged_list)-1 and tagged_list[i+1][1].find("VB")!=-1)))):
                            find=find+1
                        n.append([tagged_list[x][0] for x in range(ind2,i) if(x not in range(ct,find+1))])
                    ind=i+1 #ADDED NOW



            elif(j<len(tagged_list)-1 and tagged_list[j][1].find("VB")!=-1):
                if(ind2!=-1 and ind2!=ind):
                    find=find+1                 
                    while(find<len(tagged_list)-1 and (tagged_list[find][1]!="CC"  and tagged_list[find][0] not in conj and tagged_list[find][0]!="," and tagged_list[find][0]!=";" and tagged_list[find][0]!="." and(tagged_list[i][0]not in wdt or (i+1<len(tagged_list)-1 and tagged_list[i+1][1].find("VB")!=-1)))):
                        find=find+1
                    n.append([tagged_list[x][0] for x in range(ind2,i) if(x not in range(ct,find+1))])
                    ind2=-1
                else:
                    for x in range(ind,i): #TO SEPARATE SUBJECTS
                        if(tagged_list[x][1]=="CC"  or tagged_list[x][0] in conj or tagged_list[x][0]=="," or tagged_list[x][0]==";" or tagged_list[x][0]=="." or (tagged_list[x][0]in wdt and x+1<len(tagged_list)-1 and tagged_list[x+1][1].find("VB")==-1) ):
                            if(x>ind and x<i-1):
                                if((tagged_list[x-1][2]== 1 or tagged_list[x-1][2]==2)):
                                    y=x+1
                                    while(y<len(tagged_list)-1 and tagged_list[y][1].find("NN")==-1 and tagged_list[y][1].find("VB")==-1):
                                        y=y+1
                                    if(tagged_list[y][2]==1 or tagged_list[y][2]==2 or tagged_list[y][2]==3):
                                        if(len(lis)==0):
                                            lis.append(x-1)
                                        lis.append(y)
                    for l in range(len(lis)):
                        n.append([tagged_list[x][0] for x in range(ind,i) if(x == lis[l] or x>lis[len(lis)-1]) or (l==0 and x<lis[0]) or (l>0 and x>lis[l-1]) and x<=lis[l]])
                    if(len(lis)==0):
                        n.append([tagged_list[x][0] for x in range(ind,i)])
                if(i+1<len(tagged_list)-1 and tagged_list[i+1][1]!="PRP"):
                    if(subj_type==3):
                        tagged_list[i][0]=subj+" was "
                    else:
                        tagged_list[i][0]=subj
                    ind=i
                else:
                    ind=i+1
                lis=[]

        
        i=i+1
    if(ind2!=-1 and ind2!=ind):
        find=find+1                 
        while(find<len(tagged_list)-1 and (tagged_list[find][1]!="CC"  and tagged_list[find][0] not in conj and tagged_list[find][0]!="," and tagged_list[find][0]!=";" and tagged_list[find][0]!="." and(tagged_list[find][0]not in wdt or (find+1<len(tagged_list)-1 and tagged_list[find+1][1].find("VB")!=-1)))):
            find=find+1
        n.append([tagged_list[x][0] for x in range(ind2,i) if(x not in range(ct,find+1))])
        ind2=-1;
    else:   
        for x in range(ind,i):
            if(tagged_list[x][1]=="CC"  or tagged_list[x][0] in conj or tagged_list[x][0]=="," or tagged_list[x][0]==";" or tagged_list[x][0]=="." or (tagged_list[x][0]in wdt and x+1<len(tagged_list)-1 and tagged_list[x+1][1].find("VB")==-1) ):
                if(x>ind and x<i-1):
                    if((tagged_list[x-1][2]== 1 or tagged_list[x-1][2]==2)):
                        y=x+1
                        while(y<len(tagged_list)-1 and tagged_list[y][1].find("NN")==-1 and tagged_list[y][1].find("VB")==-1):
                            y=y+1
                        if(tagged_list[y][2]==1 or tagged_list[y][2]==2):
                            if(len(lis)==0):
                                lis.append(x-1)
                            lis.append(y)
        for l in range(len(lis)):
            n.append([tagged_list[x][0] for x in range(ind,i) if(x == lis[l] or x>lis[len(lis)-1]) or (l==0 and x<lis[0]) or (l>0 and x>lis[l-1]) and x<=lis[l]])
        if(len(lis)==0):
            n.append([tagged_list[x][0] for x in range(ind,i)])
    stringArr = []
    for arr in n:
        if(len(arr)>0):
            stringArr.append(' '.join(arr))
    return stringArr

####### ADJUST FACTORS
def simCheck(obj, studSum=0 ,teachSum=0): 
    FACT = {'NOUN': 1, 'PROPN': 1, 'PRON':1, 'VERB': 1, 'ADJ': 0.3, 'ADV': 0.3, 'SYM':1 ,'NUM': 1}
    teachMark = obj['teachMark']
    studMark = obj['studMark']
    print(teachMark)
    print('\n------')
    print(studMark)
    for key in teachMark:
        if(teachMark[key]!=0):
            try:
                studMark[key]
                totalval = teachMark[key]
                val = ((teachMark[key]-studMark[key])*FACT[key])+studMark[key]
                studSum+=val
                teachSum+=totalval
            except:
                continue
    return studSum/teachSum

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
    
#______________MAIN______________     
#Comparison between two sentences
def compare(sentence1,sentence2):
    obj1 = tagSentence(sentence1)
    obj2 = tagSentence(sentence2)
    obj2 = findSynonyms(obj2)
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
        'teachMark':tempObj,
        'studMark':result
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

def NCsplitOnVerb(sentence):
    sent = {}
    flag=0
    doc = nlp(sentence)
    print(sentence)
    for tokenn in doc:
        # if (token.lemma_=="be"):
        #   l[0]="be"
        # else:
        #   l[0]=token.text
        print(tokenn.text,tokenn.pos_)
    sent["TYPE"] = is_active(sentence)
    for token in doc:
        if(token.pos_=="VERB"and token.lemma_.lower()!="be"):
            flag=1
    if(flag==1): #there are verbs other than be
        sent["NPV"] = [token.lemma_.lower() for token in doc if token.pos_=="NOUN" 
         or token.pos_=="PRON"  
         or token.pos_=="PROPN"
         or token.pos_=="VERB" and token.lemma_.lower()!="be"]
        sent["V"] = [token.lemma_.lower() for token in doc if token.pos_=="VERB" and token.lemma_.lower()!="be"]
    else:
        sent["NPV"] = [token.lemma_.lower() for token in doc if token.pos_=="NOUN" 
         or token.pos_=="PRON"  
         or token.pos_=="PROPN"
         or token.pos_=="VERB"]
        sent["V"] = [token.lemma_.lower() for token in doc if token.pos_=="VERB"]

      

    sent["NPV"] = ' '.join(sent["NPV"])
    try:
        sent["NP"]= sent["NPV"].split(sent["V"][0])
    except:
        sent["NP"]= sent["NPV"]
    
    
    sent["NP"] = [word.replace(' ','') for word in sent["NP"]]
    sent["NP"] = [''.join(sorted(word)) for word in sent["NP"]]
    print("finished")
    return sent

#______________MAIN______________
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
    try:
        sent["NPA"]= sent["NPVA"].split(sent["V"][0])
    except:
        sent["NPA"]= sent["NPVA"]
    sent["NPA"] = [word.replace(' ','') for word in sent["NPA"]]
    sent["NPA"] = [''.join(sorted(word)) for word in sent["NPA"]]
    return sent
#______________MAIN______________     
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
            return (False,),sent1obj['NPA'][index1[i]]
    if(sent1obj["TYPE"]==sent2obj["TYPE"]):
        #len(index1) = len(index2)
        for i in range(len(index1)):
            if(index1[i]!=index2[i]):
                return (False,),sent1obj['NPA'][index1[i]]
        return (True,),"dummy"
    elif(sent1obj["TYPE"]!=sent2obj["TYPE"]):
        for i in range(len(index1)):
            if(index1[i]==index2[i]):
                return (False,),sent1obj['NPA'][index1[i]]
        return (True,),"dummy"


#teach and student are array of sentences
#AFTER CHUNKING
######## ADJUST SIM SCORE MULTIPLICATION

def compareMain(teach,student):
    f = open('feedback.txt','w+')
    arr=[]
    dicti = {}
    feedback = {}
    missing = {}

    for i in range(len(student)):
        dicti[i] = 0
        feedback[i]="Sentence subject not relevant to answer\n" 

    for i in range(len(teach)):
        obj={}
        obj['s']=teach[i]
        obj['c']=0
        arr.append(obj)
    teach = arr
    for teachObj in teach:
        counter = 0
        f = open('feedback.txt','w+')
        for sent in student:
            res , sent2 = compare(teachObj['s'],sent)
            simScore = simCheck(res)
            if(res['teachMark']['VERB']>0):
                if(checkOrderOfNoun(teachObj['s'],sent2)==False):
                    simScore*=0
                val1,val2=checkOrderOfAdjective(teachObj['s'],sent2)
                if(val1==False):
                    simScore*=0.95          #################
                if(simScore>0.4):           #################
                    teachObj['SIM'] = simScore
                    teachObj['c']=1
                    if(simScore>dicti[counter]):
                        dicti[counter] = simScore
                        if(simScore!=1):
                            feedback[counter] = "Missing adjective or modifier"
                            missing[counter] = val2
                        else:
                            feedback[counter] = "sentence fully relevant to subject"

    #teach is an object with attribute 's' , 'c' and 'SIM' if matched(result)
            counter+=1
    for i in range(len(student)):
        if(feedback[i]=="Sentence subject not relevant to answer"):
            f.write(feedback[i]+': '+student[i]+'\n--')
        elif(feedback[i] == "Missing adjective or modifier"):
            f.write(feedback[i]+" in "+student[i]+"Required: "+missing[i]+ '\n--')
        else:
            f.write(feedback[i]+' '+student[i]+'\n--')
    for i in range (len(teach)):
        f.write('\n')
        f.write(json.dumps(teach[i]));

    f.close()
