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
AuAddata=open('/mnt/sdb/wos2018-wwh/Disambiguation/Authorship_Institution_2nd/Remake2nd_AD_AuthorShip_AddrDict_2008to2016.pickle','rb')
AuAd=pickle.load(AuAddata)
AuAddata.close()


STY=2008 #<<--------set the start year
EDY=2016 #<<--------set the end year

THRESHOLD=2 #<<<-------------set the threshold HERE!!
#Set the threshold for filtering in set D

ThrMtrix=defaultdict(list)
#ThrMtrix is a dataframe recording the appearance times of each pair of institution name
InD=defaultdict(set)
#InD is created to record the successfully matched institution names with the shortest one as the key which is also the unified name for all in the same list
FInD=defaultdict(set)
#FInD is created to record the final result of institution name disambiguation with the shortest name of each group as the representation 
AuAdPOOL=defaultdict(dict)
#AuAdPOOL is created to record the institution names pairs in group AA/C/D with their sequence number in the original list
NmGP=['AA','C','D']
'''
The three kinds of name similarity group according the Huang, Yang, Yan, and Rousseau (2014)
'AA' is set of addresses in AuAd (Author-Address)
'''


#-------------------------SimilarityJudgment-----------------------------
def PairJudge1(i_org,j_org): #input the name of the organization pair i&j
	Idf=0 #use the identifier to know whether this pair of addresses has passed the tests

	STPWD=['university','of','de','institute','univ','universidade','inst','ctr','for','la','universite','universidad','do','istituto','institut','di','universiti','universitat','universidade','ltd','co','universitario','universitaire','universita','corp','inc']
	#the common stop words that will disrupt the disambiguation process (optional for use or not)

	i_org=re.sub(r'[^\w\s]',' ',i_org) #Replace all punctuations with ' '
	j_org=re.sub(r'[^\w\s]',' ',j_org)

	a=set(i_org.split()) #split the words in the name of organization 'i'
	b=set(j_org.split()) #split the words in the name of organization 'j'

	if len(a)==len(b): #'i' or 'j' are substring of the other (rule 3)
		if i_org in j_org or j_org in i_org:
			Idf=1
			return Idf

	shared=len(a & b)

	if len(a)!=len(b) and shared>2: #not equal and shared >2 (rule 2 modified)
		Idf=1
		return Idf

	total=len(a | b)
	Jaccard_M=shared/total #the Jaccard measure

	if len(a)==len(b) and Jaccard_M>0.6: #Jaccard measure>0.6 (rule 1)
		Idf=1
		return Idf

	i_up="".join(list(filter(str.isupper, i_org))) #Abbreviation of capital initials in 'i'
	j_up="".join(list(filter(str.isupper, j_org))) #Abbreviation of capital initials in 'j'

	if i_up==j_up: #'i' and 'j' share the same abbreviation of capital initials (i.e. abbreviation of the other) (rule 3)
		Idf=1
		return Idf

	i_STP=i_org.lower() #Change all upper letters to lower
	j_STP=j_org.lower()
	i_STW=i_STP.split() #the 'list' of split institution name
	j_STW=j_STP.split()
	i_len=len(i_STW)
	j_len=len(j_STW)
	
	#1.Remove all stop words
	for stw in STPWD:
		for i0 in range(i_len):
			if stw in i_STW:
				i_STW.remove(stw)
		for j0 in range(j_len):
			if stw in j_STW:
				j_STW.remove(stw)
	
	#2.Remove the shared words in i&j
	i_len=len(i_STW)
	j_len=len(j_STW)
	i_set=set(i_STW) #find the sharing words in i&j
	j_set=set(j_STW)
	share_ij=i_set & j_set
	if share_ij:
		for smw in share_ij:
			for i0 in range(i_len):
				if smw in i_STW:
					i_STW.remove(smw)
			for j0 in range(j_len):
				if smw in j_STW:
					j_STW.remove(smw)
	i_Nspc="".join(i_STW) #Recombine the institution name without space
	j_Nspc="".join(j_STW)

	#since institution name without stop words, punctuations and spaces are used in rule 4
	if Levenshtein.jaro_winkler(i_Nspc,j_Nspc)>0.8: #the edit distance<0.2 (rule 4:'http://www.alias-i.com/lingpipe/docs/api/com/aliasi/spell/JaroWinklerDistance.html')
		Idf=1

	return Idf



#Create a function PairJudge2 to compare the rest segments of the address pair
#The 'AddrGrp' is the corresponding Author_Block
def PairJudge2(i,j,AddrGrp):
	Idf=0

	Address_set=['Organization','SubOrganization','City','PostalCode','State','Country']
	#the names of the detailed addresses
	Address_set1=['City','State','PostalCode']
	#the addresses for rule 6
	InvPsCd=[' ','0'] #invalid elements in postalcode
	#The invalid PostalCode element ' ' and '0'


	i_segnum=0 #count the number of valid segments of address 'i'
	j_segnum=0 #count the number of valid segments of address 'j'
	for addr in Address_set:
		if AddrGrp[addr][i]!='':
			i_segnum+=1
		if AddrGrp[addr][j]!='':
			j_segnum+=1
	
	if i_segnum!=j_segnum or i_segnum<=3: #rule 6
		if AddrGrp['SubOrganization'][i]!='' and AddrGrp['SubOrganization'][i]==AddrGrp['SubOrganization'][j]:
			Idf=1
			return Idf
	else:
		for addr1 in Address_set1:
			if addr1=='PostalCode' and AddrGrp[addr1][i]!='' and AddrGrp[addr1][i]==AddrGrp[addr1][j]:
				i_PsCd=AddrGrp[addr1][i]
				j_PsCd=AddrGrp[addr1][j]
				i_PC=i_PsCd
				j_PC=j_PsCd
				for PsNum in InvPsCd:
					i_PC=re.sub(PsNum,'',i_PC) #Remove all ' '(space) and '0' in the postalcode
					j_PC=re.sub(PsNum,'',j_PC)
				if not i_PC or not j_PC: #Continue if the PostalCode has only ' '(space) or/and '0'
					continue
				elif i_PsCd==j_PsCd:
					Idf=1
					return Idf
			else:
				if AddrGrp[addr1][i]!='' and AddrGrp[addr1][i]==AddrGrp[addr1][j]:
					Idf=1
					return Idf
	return Idf
#-------------------------SimilarityJudgment-----------------------------




Author_Num=len(AuAd) #Number of Author_Blocks
print('Number of Author_Blocks: ', Author_Num,'\n')
para0=0
for nm0 in AuAd.keys():
	if para0%50000==0:
		print(para0,'/',Author_Num)
	AuthorBlock=AuAd[nm0]
	Org=AuthorBlock['Organization']
	AddrLen=len(Org)
	if AddrLen<2:
		continue
		para0+=1
	Ctry=AuthorBlock['Country']
	AuAdPOOL[nm0]=defaultdict(list)

	#1.Find pairs for set 'C'
	for i in range(AddrLen-1):
		i_org=Org[i]
		for j in range(i+1,AddrLen):
			j_org=Org[j]
			if Ctry[i]!=Ctry[j] or i_org==j_org: #Continue if i&j are from different Country or have exactly the same name
				continue
			if PairJudge1(i_org,j_org):
				AuAdPOOL[nm0]['C'].append('_'.join([str(i),str(j)]))
	if 'C' not in AuAdPOOL[nm0]:
		AuAdPOOL.pop(nm0)
		para0+=1
		continue

	#2.Find pairs for set 'D'
	for cp in AuAdPOOL[nm0]['C']: #notice that all the unknown information is now represented by '*'
		i=int(cp.split('_')[0]) #the sequence number of 'i' mentioned above
		j=int(cp.split('_')[1]) #the sequence number of 'j' mentioned above
		if PairJudge2(i,j,AuthorBlock):
			AuAdPOOL[nm0]['D'].append('_'.join([str(i),str(j)]))
	if 'D' not in AuAdPOOL[nm0]:
		AuAdPOOL.pop(nm0)

	para0+=1
#now 'AuAdPOOL' is a defaultdict containing all the authorships and corresponding addresses groups
print('Pool built\n')


'''
用矩阵的形式实现对不同阈值下的机构名称对的筛选，1列放机构名称1，2列放机构名称2，3列放1+2无顺序组合出现的次数
然后筛选第3列>=T的，作为最终消歧结果，以此实现不同阈值下的消歧。
太慢了，针对dataframe的循环检索及添加数据的过程十分缓慢->需要找到新的方法记录机构名称对出现的次数，尽量尝试使用dict/set/list等原生数据结构，效率更高
通过defaultdict(list)的形式可以达到同样的效果，用序列号代表dict的键值，在list中的1/2/3分别代表机构名称1，名称2，出现次数，即可避免使用dataframe
'''
#now we start the institution disambiguation by aggregate the institution names in group D
#threshold T
QA_AuBlNum=len(AuAdPOOL) #The number of AuthorBlocks with set 'D'
print('Number of Author_Blocks with set D: ',QA_AuBlNum)

print('Counting appearance time in set D')
seq=0
para1=0
for nm1 in AuAdPOOL:
	if para1%10000==0:
		print(para1,'/',QA_AuBlNum)
	#print('--------------------Author surname:',nm1,'\n')
	if 'D' not in AuAdPOOL[nm1].keys():
		para1+=1
		continue
	Org=AuAd[nm1]['Organization']
	#print('Org_AuthorBlock:',org,'\n')
	#!!!NOTICE: a pair of institution from a 'D' set of the same author block should only contribute 1 credit!!!
	#Create a subPair to achieve this target, the result of appearance of institution pair will be recorded in the subPair 'list' under an author block first
	subPair=defaultdict(list) #every author block has an independent subPair
	subseq=0 #subseq for sequence of subPair
	for cp in AuAdPOOL[nm1]['D']: #the institution couple in group 'D' within an author block 'nm1'
		i=int(cp.split('_')[0]) #the sequence number of 'i' mentioned above
		j=int(cp.split('_')[1]) #the sequence number of 'j' mentioned above
		i_org=Org[i]
		j_org=Org[j]
		fd=0 #Identifier:whether this pair of organization already exists
		#print('Org_couple ',cp,' :',i,',',j,'\n')
		if subseq==0:
			subPair[subseq]=[i_org,j_org]
			subseq+=1
		else:
			for x in subPair.keys():
				if i_org in subPair[x] and j_org in subPair[x][1]: #continue if this pair already exits
					fd=1
					continue
			if fd==0:
				subPair[subseq]=[i_org,j_org]
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
				if org_i in ThrMtrix[y] and org_j in ThrMtrix[y]:
					ThrMtrix[y][2]+=1
					fd=1
			if fd==0:
				ThrMtrix[seq]=[org_i,org_j,1]
				seq+=1
		#print('Middle-ThrMtrix: ',ThrMtrix,'\n')
	#print('Final-----Apearance of org pair:',ThrMtrix,'\n')
	para1+=1
#now we have the dataframe recording the institution name pairs and the time of appearance
print('Institution pair number:',len(ThrMtrix),'\n')

fp0=open('/mnt/sdb/wos2018-wwh/Disambiguation/ScreenRst/Remake2nd_AD_OrgPair_2008to2016.pickle','wb')
pickle.dump(ThrMtrix, fp0)
fp0.close()


#now use InD to create the institution name disambiguation comparison table satisfying the threshold T
print('Aggregating the institution names')
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


file1=open('/mnt/sdb/wos2018-wwh/Disambiguation/Result_2nd/Remake2nd_AD_IND_Threshold_'+str(THRESHOLD)+'_'+str(STY)+'to'+str(EDY)+'.pickle', 'wb')
pickle.dump(FInD, file1)
file1.close()

