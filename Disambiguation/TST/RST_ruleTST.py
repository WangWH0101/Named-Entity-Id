import Levenshtein
import pickle

DSRSTdata=open(r'D:\桌面\111\now research\CiData\whole_strict_fractionCounting\Disambiguation\AD_Univ_IND_Threshold_2_2008to2016.pickle','rb')
DSRST=pickle.load(DSRSTdata)
DSRSTdata.close()

STPWD=['University','university','of','de','Institute','Univ','univ','Universidade','universidade','Inst','inst','Ctr','ctr','for','la','Universite','universite','Universidad','universidad','do','Istituto','istituto','Institut','institut','di','Universiti','universiti','Universitat','universitat','Universidade','universidade','Ltd','Co','Universitario','universitario','Universitaire','universitaire','Universita','universita','Corp','Inc']
STPPC=['&','(',')','-']
#the common stop words that will disrupt the disambiguation process (optional for use or not)
UnivWD=['Univ','univ','U']

AuAdPOOL=[]

#for ky in DSRST.keys():

org=list(DSRST['USC'])
ins_num=len(org)
for i in range(ins_num-1):
	if UnivWD[0] not in org[i] and UnivWD[1] not in org[i]:
		if not org[i].isupper() or UnivWD[2] not in org[i]:
			continue

	i_org=org[i]
	for j in range(i+1,ins_num):

		if UnivWD[0] not in org[j] and UnivWD[1] not in org[j]:
			if not org[j].isupper() or UnivWD[2] not in org[j]:
				continue

		j_org=org[j]

		i_STP=i_org
		j_STP=j_org
		for stpc in STPPC:
			if stpc in i_org:
				i_STP=i_org.replace(stpc,' ') #replace the punctuations with space ' '
			if stpc in j_org:
				j_STP=j_org.replace(stpc,' ')
		i_STW=i_STP.split() #the 'list' of split institution name
		i_len=len(i_STW)
		j_STW=j_STP.split()
		j_len=len(j_STW)
		for stw in STPWD:
			for i0 in range(i_len):
				if stw in i_STW:
					i_STW.remove(stw)
			for j0 in range(j_len):
				if stw in j_STW:
					j_STW.remove(stw)
		i_Nspc="".join(i_STW) #Recombine the institution name without space
		j_Nspc="".join(j_STW)

		a=set(i_org.split()) #split the words in the name of organization 'i'
		b=set(j_org.split()) #split the words in the name of organization 'j'
		shared=len(a.intersection(b))
		total=len(a.union(b))
		Jaccard_M=shared/total #the Jaccard measure
		i_up="".join(list(filter(str.isupper, i_org))) #Abbreviation of capital initials in 'i'
		j_up="".join(list(filter(str.isupper, j_org))) #Abbreviation of capital initials in 'j'
		'''
		if len(a)==len(b) and Jaccard_M>0.6: #Jaccard measure>0.6 (rule 1)
			AuAdPOOL.append('_'.join(['r1',i_org,j_org]))
		elif len(a)!=len(b) and shared>2: #not equal and shared >2 (rule 2)
			AuAdPOOL.append('_'.join(['r2',i_org,j_org]))

		elif len(a)==len(b): #'i' or 'j' are substring of the other (rule 3)
			if i_org in j_org or j_org in i_org:
				AuAdPOOL.append('_'.join(['r31',i_org,j_org]))
		elif i_up==j_up: #'i' and 'j' share the same abbreviation of capital initials (i.e. abbreviation of the other) (rule 3)
			AuAdPOOL.append('_'.join(['r32',i_org,j_org]))
		'''
		if Levenshtein.jaro_winkler(i_Nspc,j_Nspc)>0.85:
			print(i_Nspc,'_',j_Nspc,'_',Levenshtein.jaro_winkler(i_Nspc,j_Nspc))
			AuAdPOOL.append('_'.join(['r4',i_org,j_org]))
			input()
		'''
		elif Levenshtein.jaro_winkler(i_Nspc,j_Nspc)==1.0: #the edit distance<0.2 (rule 4:'http://www.alias-i.com/lingpipe/docs/api/com/aliasi/spell/JaroWinklerDistance.html')
			AuAdPOOL.append('_'.join(['r4',i_org,j_org]))
		'''
print(AuAdPOOL)
'''
if len(AuAdPOOL)>0:
	print(ky)
	print(AuAdPOOL)
	input()
'''
