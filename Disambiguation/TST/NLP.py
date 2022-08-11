import spacy
import pickle
import Levenshtein
import difflib
from tabulate import tabulate
#import time
nlp=spacy.load('en_core_web_lg')

'''
DSRSTdata=open(r'D:\桌面\111\now research\CiData\whole_strict_fractionCounting\Disambiguation\AD_Univ_IND_Threshold_2_2008to2016.pickle','rb')
DSRST=pickle.load(DSRSTdata)
DSRSTdata.close()
'''

STPWD=['University','university','of','de','Institute','Univ','univ','Universidade','universidade','Inst','inst','Ctr','ctr','for','la','Universite','universite','Universidad','universidad','do','Istituto','istituto','Institut','institut','di','Universiti','universiti','Universitat','universitat','Universidade','universidade','Ltd','Co','Universitario','universitario','Universitaire','universitaire','Universita','universita','Universiteit','universiteit','Corp','Inc']
STPPC=['&','(',')','-']
#the common stop words that will disrupt the disambiguation process (optional for use or not)
UnivWD=['Univ','univ','U']

a='University of California Irvine'
b='California State University Long Beach'
c='University of California Berkeley'
d='University of Minnesota Duluth'

a1='Univ California Irvine'
a2='UCI'
a3='UC Irvine'
a4='Univ Calif Irvine'

b1='Calif State Univ LB'
b2='CSULB'
b3='CSU LB'
b4='CSU Long Beach'

c1='CUI'
c2='UI'

ins=[c1,c2]

#Utilization of stop-words
def STPW(a):
	i_STP=a
	for stpc in STPPC:
		if stpc in a:
			i_STP=a.replace(stpc,' ') #replace the punctuations with space ' '
	i_STW=i_STP.split() #the 'list' of split institution name
	i_len=len(i_STW)
	for stw in STPWD:
		for i0 in range(i_len):
			if stw in i_STW:
				i_STW.remove(stw)
	i_Nspc="".join(i_STW) #Recombine the institution name without space
	return i_Nspc

#stop words with spaces
def STPW_SPC(a):
	i_STP=a
	for stpc in STPPC:
		if stpc in a:
			i_STP=a.replace(stpc,' ') #replace the punctuations with space ' '
	i_STW=i_STP.split() #the 'list' of split institution name
	i_len=len(i_STW)
	for stw in STPWD:
		for i0 in range(i_len):
			if stw in i_STW:
				i_STW.remove(stw)
	i_spc=" ".join(i_STW) #Recombine the institution name without space
	return i_spc


#Spacy similarity (cosine similarity+word embedding)
def SpSim(a,b):
	SIM=nlp(a).similarity(nlp(b))
	return SIM

#SequenceMatcher based on difflib
def SqM(a,b):
	SIM=difflib.SequenceMatcher(None,a,b).ratio()
	return SIM

#Levenshtein ratio
def LvR(a,b):
	SIM=Levenshtein.ratio(a,b)
	return SIM

#Levenshtein.jaro
def LvJ(a,b):
	SIM=Levenshtein.jaro(a,b)
	return SIM

#Levenshtein jaro-winkler
def LvJW(a,b):
	SIM=Levenshtein.jaro_winkler(a, b)
	return SIM







TableHeader=['Method','Score']
for i in range(len(ins)):
	for j in range(i+1,len(ins)):

		print(ins[i],'_',ins[j])
		print(STPW_SPC(ins[i]),'_',STPW_SPC(ins[j]))
		print(STPW(ins[i]),'_',STPW(ins[j]),':')

		SqMtch=SqM(ins[i],ins[j])
		STP_SqMtch=SqM(STPW(ins[i]),STPW(ins[j]))

		LVR=LvR(ins[i],ins[j])
		STP_LVR=LvR(STPW(ins[i]),STPW(ins[j]))

		LVJ=LvJ(ins[i],ins[j])
		STP_LVJ=LvJ(STPW(ins[i]),STPW(ins[j]))


		OrJW=LvJW(ins[i],ins[j])
		STP_OrJW=LvJW(STPW(ins[i]),STPW(ins[j]))

		CosSim=SpSim(ins[i],ins[j])
		STP_CosSim=SpSim(STPW_SPC(ins[i]),STPW_SPC(ins[j]))

		Ave=(SqMtch+LVR+LVJ+OrJW)/4
		STP_Ave=(STP_OrJW+STP_LVJ+STP_LVR+STP_SqMtch)/4

		RST=[['CosSim',CosSim],['STW_CosSim',STP_CosSim],['SqcMch',SqMtch],['STW_SqcMch',STP_SqMtch],['LvRatio',LVR],['STW_LvRatio',STP_LVR],['J',LVJ],['STW_J',STP_LVJ],['JW',OrJW],['STW_JW',STP_OrJW],['Average',Ave],['STW_Ave',STP_Ave]]
		print(tabulate(RST,headers=TableHeader,tablefmt='grid'))







'''
TableHeader=['JW','STW_JW','Sim']
for nm in DSRST.keys():
	ins=list(DSRST[nm])
	print(ins)
	for i in range(len(ins)):
		for j in range(i+1,len(ins)):
			print(ins[i],'_',ins[j],':')

			#t0=time.time()
			OrJW=Levenshtein.jaro_winkler(ins[i],ins[j])
			#t1=time.time()
			#print('Original_LvJW:',OrJW)

			#t2=time.time()
			i0=nlp(ins[i])
			j0=nlp(ins[j])
			SIM=i0.similarity(j0) #the time cost is about 0.013s
			#t3=time.time()
			#print('Sim:',SIM)

			i_org=ins[i]
			j_org=ins[j]

			#t4=time.time()
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
			J_W=Levenshtein.jaro_winkler(i_Nspc,j_Nspc)
			#t5=time.time()
			#print('STPW_LvJW:',J_W)
			RST=[(str(OrJW),str(J_W),str(SIM))]
			print(tabulate(RST,headers=TableHeader,tablefmt='grid'))
	input()
'''


'''
DSRSTdata=open(r'D:\桌面\111\now research\CiData\whole_strict_fractionCounting\Disambiguation\AD_IND_Threshold_2_2008to2016.pickle','rb')
DSRST=pickle.load(DSRSTdata)
DSRSTdata.close()

for i in DSRST.keys():
	print(i,':',DSRST[i])
	for insNM in DSRST[i]:
		print(insNM)
		doc=nlp(insNM)
		spacy.displacy.render(doc,style='dep',options={'distance':140},jupyter=True)
		token_dependencies=((token.text,token.dep_,token.head.text) for token in doc)
		print(tabulate(token_dependencies, headers=['Token','Dependency Relation','Parent Token']))
		entity_types=((ent.text,ent.label_) for ent in doc.ents)
		print(tabulate(entity_types,headers=['Entity','Entity Type']))
		input()
'''
