#teachMark
#studMark

####### ADJUST FACTORS
def simCheck(obj, studSum=0 ,teachSum=0): 
    FACT = {'NOUN': 1, 'PROPN': 1, 'PRON':1, 'VERB': 1, 'ADJ': 0.3, 'ADV': 0.3, 'SYM':1 ,'NUM': 1}
    teachMark = obj['teachMark']
    studMark = obj['studMark']
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