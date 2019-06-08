import spacy
nlp = spacy.load('en_core_web_lg')
import neuralcoref

###FUNCTIONS###
# resolve_co_reference
# chunk

def resolve_co_reference(text):
	'''
	The coref model calculates the probabilities of links between The main occurence and a reference of that
	main occurence and on the basis of that replaces every reference with the main occurence it is referring to
	'''
	coref = neuralcoref.NeuralCoref(nlp.vocab) # initialize the neuralcoref with spacy's vocabulary
	nlp.add_pipe(coref, name='neuralcoref') #add the coref model to pipe
	doc = nlp(text)
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
		#  	l[0]="be"
		# else:
		#  	l[0]=token.text
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
