from collections import defaultdict
import pickle

file=open(r'D:\桌面\111\now research\CiData\whole_strict_fractionCounting\Disambiguation\FormalSteps\AD\MiddleFile\AD_Univ_OrgPair_2008to2016.pickle','rb')
ThrMtrix=pickle.load(file)
file.close()

THRESHOLD=10 #<<<-------------set the threshold HERE!!
InD=defaultdict(list)
FInD=defaultdict(set)

#now use InD to create the institution name disambiguation comparison table satisfying the threshold T
seq=0
for x in ThrMtrix.keys():
	thr=ThrMtrix[x][3] #the time this pair of ins. appears in D set
	Ctry=ThrMtrix[x][2] #the country of the institution pair
	if thr<THRESHOLD: #compare the threshold
		continue
	fd=0 #identifier whether this pair already exits
	i_org=ThrMtrix[x][0]
	j_org=ThrMtrix[x][1]
	if seq==0:
		InD[seq].append(set())
		InD[seq][0].update({i_org,j_org})
		InD[seq].append(Ctry)
		seq+=1
		continue
	for y in InD.keys():
		if Ctry==InD[y][1]: #from the same country
			if i_org in InD[y][0] or j_org in InD[y][0]:
				InD[y][0].update({i_org,j_org})
				fd=1
	if fd==0:
		InD[seq].append(set())
		InD[seq][0].update({i_org,j_org})
		InD[seq].append(Ctry)
		seq+=1
#now we have a dataframe 'InD' containing the result of the institution name disambiguation and corresponding threshold value

Group_Num=len(InD)
print('Number of Groups:',Group_Num)

#now we need to change the keys of 'InD' to the shortest institution name of each 'set'
for ky in InD.keys():
	ct0=0
	for insnm in InD[ky][0]:
		if ct0==0:
			rpnm=insnm
			ct0=1
		else:
			if len(insnm)<len(rpnm):
				rpnm=insnm
	FInD[rpnm]=InD[ky][0]


file1=open(r'D:\桌面\111\now research\CiData\whole_strict_fractionCounting\Disambiguation\FormalSteps\AD\MiddleFile\Result\AD_Univ_IND_Threshold_'+str(THRESHOLD)+'_2008to2016.pickle', 'wb')
pickle.dump(FInD, file1)
file1.close()

