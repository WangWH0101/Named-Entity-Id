import pickle
import Levenshtein
import pandas as pd
from collections import defaultdict

'''
This is the all discipline version of step 3
No target field!!

1.this step aims to do the institution name disambiguation (IND) progress through the 3 modules and 6 rules
according to Huang(2014)
2.set the parameter below to get the proper result
'''


#Manually choose the original authorship_address file you want. mind: 1.the field 2.time period
AuAddata=open('/mnt/sdb/wos2018-wwh/Disambiguation/Authorship_Institution/AD_AuthorShip_AddrDict_2008to2016.pickle','rb')
AuAd=pickle.load(AuAddata)
AuAddata.close()

STY=2008 #<<--------set the start year
EDY=2016 #<<--------set the end year

STPWD=['University','university','of','&','(',')','de','Institute','-','Univ','univ','Universidade','universidade','Inst','inst','Ctr','ctr','for','la','Universite','universite','Universidad','universidad','do','Istituto','istituto','Institut','institut','di','Universiti','universiti','Universitat','universitat','Universidade','universidade','Ltd','Co','Universitario','universitario','Universitaire','universitaire','Universita','universita','Corp','Inc']
use_stwd=0 #<<-------------1 if you want to use the stop words/0 if you don't
#the common stop words that will disrupt the disambiguation process (optional for use or not)
THRESHOLD=3 #<<<-------------set the threshold HERE!!
#set the threshold for filtering

ThrMtrix=defaultdict(list)
#ThrMtrix is a dataframe recording the appearance times of each pair of institution name
InD=defaultdict(set)
#InD is created to record the successfully matched institution names with the shortest one as the key which is also the unified name for all in the same list
FInD=defaultdict(set)
#FInD is created to record the final result of institution name disambiguation with the shortest name of each group as the representation 
AuAdPOOL=defaultdict(dict)
#AuAdPOOL is created to record the institution names pairs in group AA/C/D with their sequence number in the original list
NmGP=['C','D']
#the three kinds of name similarity group according the Huang, Yang, Yan, and Rousseau (2014)
Address_set=['Organization','SubOrganization','City','PostalCode','State','Country']
#the names of the detailed addresses
Address_set1=['City','PostalCode','State']
#the addresses for rule 6


Author_Num=len(AuAd)
print('number of authors:', Author_Num,'\n')

para0=0
for nm0 in AuAd.keys():
	if para0%10000==0:
		print(para0,'/',Author_Num)
	org=AuAd[nm0]['Organization']
	#print('institution list:\n',org)
	addrlen=len(AuAd[nm0]['Organization'])
	AuAdPOOL[nm0]=defaultdict(list)
	if addrlen<=1:
		para0+=1
		continue
	for i in range(addrlen):
		if org[i]=='*' or org[i]=='' or AuAd[nm0]['Country'][i]=='*' or AuAd[nm0]['Country'][i]=='':
			continue
		i_org=org[i]
		for j in range(i+1,addrlen):
			if org[j]=='*' or org[j]=='' or AuAd[nm0]['Country'][j]=='*' or AuAd[nm0]['Country'][j]=='':
				continue
			elif AuAd[nm0]['Country'][i]!=AuAd[nm0]['Country'][j]: #make sure they have valid country inf. and are from the same country (rule 5)
				continue
			j_org=org[j]
			if use_stwd==1:
				for stw in STPWD:
					if stw in i_org:
						i_org=i_org.replace(stw,'')
					if stw in j_org:
						j_org=j_org.replace(stw,'')
			#set 'use_stwd=0' if you don't want to use the stop words
			
			a=set(i_org.split()) #split the words in the name of organization 'i'
			b=set(j_org.split()) #split the words in the name of organization 'j'
			shared=len(a.intersection(b))
			total=len(a.union(b))
			Jaccard_M=shared/total #the Jaccard measure
			i_up="".join(list(filter(str.isupper, i_org))) #Abbreviation of capital initials in 'i'
			j_up="".join(list(filter(str.isupper, j_org))) #Abbreviation of capital initials in 'j'
			if len(a)==len(b) and Jaccard_M>0.6: #Jaccard measure>0.6 (rule 1)
				AuAdPOOL[nm0]['C'].append('_'.join([str(i),str(j)]))
			elif len(a)!=len(b) and shared>2: #not equal and shared >2 (rule 2)
				AuAdPOOL[nm0]['C'].append('_'.join([str(i),str(j)]))
			elif len(a)==len(b): #'i' or 'j' are substring of the other (rule 3)
				if i_org in j_org or j_org in i_org: 
					AuAdPOOL[nm0]['C'].append('_'.join([str(i),str(j)]))
			elif i_up==j_up: #'i' and 'j' share the same abbreviation of capital initials (i.e. abbreviation of the other) (rule 3)
				AuAdPOOL[nm0]['C'].append('_'.join([str(i),str(j)]))
			elif Levenshtein.jaro_winkler(i_org,j_org)>0.8: #the edit distance<0.2 (rule 4:'http://www.alias-i.com/lingpipe/docs/api/com/aliasi/spell/JaroWinklerDistance.html')
				AuAdPOOL[nm0]['C'].append('_'.join([str(i),str(j)]))
	#start the screening in group C of each author block and generate the group D
	for cp in AuAdPOOL[nm0]['C']: #notice that all the unknown information is now represented by '*'/''
		i=int(cp.split('_')[0]) #the sequence number of 'i' mentioned above
		j=int(cp.split('_')[1]) #the sequence number of 'j' mentioned above
		#number of segments in the addresses of 'i' and 'j'
		i_segnum=0 #count the number of valid segments of address 'i'
		j_segnum=0 #count the number of valid segments of address 'j'
		for addr in Address_set:
			if AuAd[nm0][addr][i]!='*' and AuAd[nm0][addr][i]!='':
				i_segnum+=1
			if AuAd[nm0][addr][j]!='*' and AuAd[nm0][addr][j]!='':
				j_segnum+=1
		if i_segnum!=j_segnum or i_segnum<=3: #rule 6
			if AuAd[nm0]['SubOrganization'][i]==AuAd[nm0]['SubOrganization'][j] and AuAd[nm0]['SubOrganization'][i]!='*' and AuAd[nm0]['SubOrganization'][i]!='':
				AuAdPOOL[nm0]['D'].append('_'.join([str(i),str(j)]))
		elif i_segnum>3:
			for addr1 in Address_set1:
				if AuAd[nm0][addr1][i]!='*' and AuAd[nm0][addr1][i]!='' and AuAd[nm0][addr1][i]==AuAd[nm0][addr1][j]:
					AuAdPOOL[nm0]['D'].append('_'.join([str(i),str(j)]))
					break
	para0+=1

#now 'AuAdPOOL' is a defaultdict containing all the authorships and corresponding addresses groups
print('pool built\n')

fp0 =open('/mnt/sdb/wos2018-wwh/Disambiguation/ScreenRst/AD_CandDset_'+str(STY)+'to'+str(EDY)+'.pickle', 'wb')
pickle.dump(AuAdPOOL, fp0)
fp0.close()


'''
用矩阵的形式实现对不同阈值下的机构名称对的筛选，1列放机构名称1，2列放机构名称2，3列放1+2无顺序组合出现的次数
然后筛选第3列>=T的，作为最终消歧结果，以此实现不同阈值下的消歧。
太慢了，针对dataframe的循环检索及添加数据的过程十分缓慢->需要找到新的方法记录机构名称对出现的次数，尽量尝试使用dict/set/list等原生数据结构，效率更高
通过defaultdict(list)的形式可以达到同样的效果，用序列号代表dict的键值，在list中的1/2/3分别代表机构名称1，名称2，出现次数，即可避免使用dataframe
'''
#now we start the institution disambiguation by aggregate the institution names in group D
#threshold T
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

if use_stwd==1:
	file1 =open('/mnt/sdb/wos2018-wwh/Disambiguation/Result/AD_IND_StopWd_Threshold_'+str(THRESHOLD)+'_'+str(STY)+'to'+str(EDY)+'.pickle', 'wb')
else:
	file1 =open('/mnt/sdb/wos2018-wwh/Disambiguation/Result/AD_IND_Threshold_'+str(THRESHOLD)+'_'+str(STY)+'to'+str(EDY)+'.pickle', 'wb')
pickle.dump(FInD, file1)
file1.close()

