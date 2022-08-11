import pickle
from collections import defaultdict

STY=2008 #<<--------set the start year
EDY=2016 #<<--------set the end year

THRESHOLD=2
InD=defaultdict(set)
FInD=defaultdict(set)

ThrMtrixdata=open('/mnt/sdb/wos2018-wwh/Disambiguation/ScreenRst/AD_OrgPair_2008to2016.pickle','rb')
ThrMtrix=pickle.load(ThrMtrixdata)
ThrMtrixdata.close()

seq=0
para2=0
for x in ThrMtrix.keys():
	if para2%1000==0:
		print(para2,'/',len(ThrMtrix))
	thr=ThrMtrix[x][2] #the time this pair of ins. appears in D set
	if thr<THRESHOLD: #compare the threshold
		para2+=1
		continue
	fd=0
	i_org=ThrMtrix[x][0]
	j_org=ThrMtrix[x][1]
	if seq==0:
		InD[seq].update({i_org,j_org})
		seq+=1
		continue
	for y in InD.keys():
		if i_org in InD[y] or j_org in InD[y]:
			InD[y].update({i_org,j_org})
			fd=1
	if fd==0:
		InD[seq].update({i_org,j_org})
		seq+=1
	para2+=1
#now we have a dataframe 'InD' containing the result of the institution name disambiguation and corresponding threshold value

Group_Num=len(InD)
print('Number of Groups:',Group_Num)

#now we need to change the keys of 'InD' to the shortest institution name of each 'set'
para3=0
for ky in InD.keys():
	if para3%1000==0:
		print(para3,'/',Group_Num)
	ct0=0
	for insnm in InD[ky]:
		if ct0==0:
			rpnm=insnm
			ct0=1
		else:
			if len(insnm)<len(rpnm):
				rpnm=insnm
	FInD[rpnm]=InD[ky]
	para3+=1


file1=open('/mnt/sdb/wos2018-wwh/Disambiguation/Result/AD_IND_Threshold_'+str(THRESHOLD)+'_'+str(STY)+'to'+str(EDY)+'.pickle', 'wb')
pickle.dump(FInD, file1)
file1.close()