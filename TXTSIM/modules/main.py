#teach and student are array of sentences
#AFTER CHUNKING

######## ADJUST SIM SCORE MULTIPLICATION
def compareMain(teach,student):
    arr=[]
    for i in range(len(teach)):
        obj={}
        obj['s']=teach[i]
        obj['c']=0
        arr.append(obj)
    teach = arr
    for teachObj in teach:
        for sent in student:
            res , sent2 = compare(teachObj['s'],sent)
            simScore = simCheck(res)
            if(res['teachMark']['VERB']>0):
                if(checkOrderOfNoun(teachObj['s'],sent2)==False):
                    simScore*=0
                if(checkOrderOfAdjective(teachObj['s'],sent2)==False):
                    simScore*=0.95              #################
                    if(simScore>0.4):           #################
                teachObj['SIM'] = simScore
                teachObj['c']=1
    #teach is an object with attribute 's' , 'c' and 'SIM' if matched(result)
    return teach