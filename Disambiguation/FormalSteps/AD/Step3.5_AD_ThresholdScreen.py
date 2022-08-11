from collections import defaultdict
import pickle

'''
This program aims to test the problem of memory error during the disambiguation
'''

#The original authorship_address file you want. mind the time period
AuAddata=open('/mnt/sdb/wos2018-wwh/Disambiguation/Authorship_Institution/AD_AuthorShip_AddrDict_2008to2016.pickle','rb')
AuAd=pickle.load(AuAddata)
AuAddata.close()

#The file with C and D sets constructed under each author block
AuAdPOOLdata=open('/mnt/sdb/wos2018-wwh/Disambiguation/ScreenRst/AD_CandDset_2008to2016.pickle','rb')
AuAdPOOL=pickle.load(AuAdPOOLdata)
AuAdPOOLdata.close()

STY=2008 #<<--------set the start year
EDY=2016 #<<--------set the end year

THRESHOLD=2 #<<<-------------set the threshold HERE!!
ThrMtrix=defaultdict(list)
#ThrMtrix is a dataframe recording the appearance times of each pair of institution name
InD=defaultdict(set)
#InD is created to record the successfully matched institution names with the shortest one as the key which is also the unified name for all in the same list
FInD=defaultdict(set)
#FInD is created to record the final result of institution name disambiguation with the shortest name of each group as the representation 


Author_Num=len(AuAd)
print('counting threshold number')
seq=0
para1=0
for nm1 in AuAdPOOL:
	if para1%10000==0:
		print(para1,'/',Author_Num)
	#print('--------------------Author surname:',nm1,'\n')
	if 'D' not in AuAdPOOL[nm1].keys():
		para1+=1
		continue
	org=AuAd[nm1]['Organization']
	#print('Org_AuthorBlock:',org,'\n')
	#!!!NOTICE: a pair of institution from a 'D' set of the same author block should only contribute 1 credit!!!
	#Create a subPair to achieve this target, the result of appearance of institution pair will be recorded in the subPair 'list' under an author block first
	subPair=defaultdict(list) #every author block has an independent subPair
	subseq=0 #subseq for sequence of subPair
	for cp in AuAdPOOL[nm1]['D']: #the institution couple in group 'D' within an author block 'nm1'
		i=int(cp.split('_')[0]) #the sequence number of 'i' mentioned above
		j=int(cp.split('_')[1]) #the sequence number of 'j' mentioned above
		fd=0 #Identifier:whether this pair of organization already exists
		#print('Org_couple ',cp,' :',i,',',j,'\n')
		if subseq==0:
			subPair[subseq]=[org[i],org[j]]
			subseq+=1
		else:
			for x in subPair.keys():
				if org[i]==subPair[x][0] and org[j]==subPair[x][1]: #continue if this pair already exits
					fd=1
					continue
				elif org[i]==subPair[x][1] and org[j]==subPair[x][0]: #continue if this pair already exits
					fd=1
					continue
			if fd==0:
				subPair[subseq]=[org[i],org[j]]
				subseq+=1
	#print('SubPair:',subPair,'\n')
	
	#The subPair for author block 'nm1' is now created
	#the format of 'ThrMtrix':[ins(i),ins(j),number of appearance in group 'D']
	for x in subPair.keys():
		org_i=subPair[x][0]
		org_j=subPair[x][1]
		fd=0 #Identifier: whether this pair of organization already exists
		#print('SubOrg_i: ',org_i,' // SubOrg_j: ',org_j,'\n')
		if seq==0:
			ThrMtrix[seq]=[org_i,org_j,1]
			seq+=1
		else:
			for y in ThrMtrix.keys():
				if org_i==ThrMtrix[y][0] and org_j==ThrMtrix[y][1]:
					#print('i=i,j=j:')
					#print(ThrMtrix[y],'\n')
					ThrMtrix[y][2]+=1
					fd=1
				elif org_i==ThrMtrix[y][1] and org_j==ThrMtrix[y][0]:
					#print('i=j,j=i:')
					#print(ThrMtrix[y],'\n')
					ThrMtrix[y][2]+=1
					fd=1
			#print('already exits? ',fd)
			if fd==0:
				ThrMtrix[seq]=[org_i,org_j,1]
				seq+=1
		#print('Middle-ThrMtrix: ',ThrMtrix,'\n')
	#print('Final-----Apearance of org pair:',ThrMtrix,'\n')
	para1+=1
#now we have the dataframe recording the institution name pairs and the time of appearance
print('institution pair number:',len(ThrMtrix),'\n')

fp0=open('/mnt/sdb/wos2018-wwh/Disambiguation/ScreenRst/AD_OrgPair_2008to2016.pickle','wb')
pickle.dump(ThrMtrix, fp0)
fp0.close()


#now use InD to create the institution name disambiguation comparison table satisfying the threshold T
print('aggregating the institution names')
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

file1 =open('/mnt/sdb/wos2018-wwh/Disambiguation/Result/AD_IND_Threshold_'+str(THRESHOLD)+'_'+str(STY)+'to'+str(EDY)+'.pickle', 'wb')
pickle.dump(FInD, file1)
file1.close()