import pickle
import pandas as pd
from collections import defaultdict

def get_keys1(d, value1, value2):
	return [k for k,v in d.items() if value1 in v['Organization'] and value2 in v['Organization']]

def find_index(lst, x):
	result = []
	for k,v in enumerate(lst): #k和v分别表示list中的下标和该下标对应的元素
		if v == x:
			result.append(k)
	return result


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

'''
This part of the program aims to test second of module of classification
Why universitis from New York and Illonois are classified together
	
For example:
'State University of New York (SUNY) System' & 'University of Illinois System'
They have different length and 3 shared words (i.e., University & of & System) which can satisfy rule 2.
It's obvious that when the two university systems cooperate frequently, they can easily achieve the threshold you set.
Not only this pair can be misclassified, but different universities under the two systems can be misclassified.
For instance:
{'Univ Chicago', 'State University of New York (SUNY) Downstate Medical Center', 'Univ Illinois Urbana Cham', 
'State University of New York (SUNY) Upstate Medical Center', 'State University of New York (SUNY) System', 'University of Illinois System', 
'University of Illinois Urbana-Champaign', 'University of Illinois Chicago Hospital', 'State University of New York (SUNY) - Oswego', 
'University of Illinois Springfield', 'University of Illinois Chicago', 'New York University', 'State University of New York (SUNY) Albany', 
'University of Chicago'}
It's easy to find out that two university systems 'State University of New York' and 'University of Illinois System' are misclassified together
due to the rule.
'''


TGF='CS'
AuAddata=open('/mnt/sdb/wos2018-wwh/Disambiguation/Authorship_Institution_2nd/Remake2nd_AuthorShip_AddrDict_'+TGF+'_2008to2016.pickle','rb')
AuAd=pickle.load(AuAddata)
AuAddata.close()

Ins1='State University of New York (SUNY) System'
Ins2='University of Illinois System'
INS=[Ins1,Ins2]

#The author blockes with the two institution together
AuthorNM=get_keys1(AuAd,Ins1,Ins2)
print('Number of AuthorBlocks: ',len(AuthorNM))
ShareAddr=defaultdict(dict)
Address_set1=['SubOrganization','City','State','PostalCode']
for NM in AuthorNM:
	ShareAddr[NM]=defaultdict(dict)
	for InsNM in INS:
		ShareAddr[NM][InsNM]=defaultdict(set)
		seqlst=find_index(AuAd[NM]['Organization'],InsNM)
		for addr in Address_set1:
			for seq in seqlst:
				ShareAddr[NM][InsNM][addr].add(AuAd[NM][addr][seq])
print('ShareAddr created!')

for NM in ShareAddr.keys():
	print('AuthorBlock: ',NM)
	for addr in Address_set1:
		print('Address type: ',addr)
		commonaddr=ShareAddr[NM][Ins1][addr]&ShareAddr[NM][Ins2][addr]
		if not commonaddr or commonaddr=={''}:
			continue
		print('Shared address: \n',commonaddr)
		para=input()
		if para:
			break










