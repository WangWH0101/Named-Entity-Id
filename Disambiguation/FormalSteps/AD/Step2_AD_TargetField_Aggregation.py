import re
import os
import time
import pickle
import numpy as np
import pandas as pd
from collections import defaultdict

'''
This is the all discipline version of step 2
1.extend to all disciplines
so there is no need for target field

1.this step will aggregate the addresses with the same authorship(surname) together 
in target years and further clean the original data

2.this program will find all the institution names with the same authorship 
under the corresponding requirement (year)
'''

#get_keys() is a 'list' through which you can find the keys of certain value in a 'dict'
def get_keys(d, value):
    return [k for k,v in d.items() if value == v]
def get_keys1(d, value):
    return [k for k,v in d.items() if value in v]


#the 'dict' of papers publication year
PYdata=open('/mnt/sdb/wos2018-junming/data-paper_year.pickle','rb')
PY=pickle.load(PYdata)
PYdata.close()

#the comparison table for unified paperID to the WoS original articleID
ppIDdata=open("/mnt/sdb/wos2018-junming/data-paper2wos.pkl", "rb")
ppID=pickle.load(ppIDdata)
ppIDdata.close()

#the file of original WoS data with both authors' name and the corresponding address
filePath = '/mnt/sdb/wos2018-wwh/Disambiguation/Authorship_Address/'
all_files = os.listdir(filePath)
year_list=[]
for each_file in all_files:
	m = re.search("address_(\d\d\d\d)", each_file)
	if m is None:
		continue
	else:
		year_list.append(m.group(1))
year_list = sorted(list(set(year_list)))
print('the year to consider:\n',year_list)
#the year_list here indicates the year of the files with both authors' name and addresses
#which is exactly the year we need to consider

STY=year_list[0] #cann't be earlier than 2008 when authorship doesn't match the address
EDY=year_list[len(year_list)-1]


print('Start Calculating--------------------------------------')
#create a 'set' TYP to record the all the papers of target years
TYP=set()
for CRY in year_list:
	CRY=int(CRY)
	TYP=TYP.union(set(get_keys(PY,CRY))) #the 'set' of papers published in CRY
	print('papers of ',CRY,' : ',len(TYP))
TGP=TYP
#notice that the TGP includes the unified paperID instead of the original articleID from WoS database
	
#find the articleID of target papers (not the paperID)
TGartID=[]
para0=0
for id0 in TGP:
	TGartID.append(ppID[id0])
print('Number of target papers from ',STY,' to ',EDY,': ', len(TGartID))
#now we have a list of target papers' articleID
TGID=pd.DataFrame({'ArticleID':TGartID})
#TGID is a dataframe with the column 'ArticleID' containing all the target articleID

for each_file in all_files:
	m = re.search("address_" + str(CRY), each_file)
	if m is None:
		continue
	else:
		filename = filePath + each_file
	data = pd.read_hdf(filename)
	#data is the original WoS database containing both authorship and addresses of each paper in 'CRY'
print('Number of existential targets:\n',data.shape[0])

data0=pd.merge(data,TGID,on=['ArticleID'])
#data0 is the dataframe with all the target papers and their corresponding inf.
#now you have the dataframe of necessary papers!
print('number of eligible targets:\n',data0.shape[0])

Author_Addr=defaultdict(dict)
#the address subsets we need is listed below
Address_set=['Organization','SubOrganization','City','State','Country','PostalCode']
#create a 'defaultdict' to record the addresses with the same author name in the corresponding year and field



datalen=data0.shape[0]
N_org=[] #create a new list to record the unified institution name
#unify the format in organization column
print('Unify the format of organization:')
for i in range(0,datalen):
	if i%50000==0:
		print(i,'/',datalen)
	mainaddr=data0.loc[i,'Organization']
	if '"' in mainaddr:
		mainaddr=mainaddr.replace('"','')
		N_org.append(mainaddr)
	else:
		N_org.append(mainaddr)
data0['Organization']=N_org

#create the 'abbreviated name'-'address' dict
print('Classification and Counting:')
for j in range(0,datalen):
	if j%10000==0:
		print(j,'/',datalen)
	mainaddr=(data0.loc[j])['Organization']
	if mainaddr=='*' or mainaddr is None:
		continue
	name0=(data0.loc[j])['abbrFullName']
	if name0 not in Author_Addr:
		Author_Addr[name0]=defaultdict(list)
		for addr in Address_set:
			addr0=(data0.loc[j])[addr]
			Author_Addr[name0][addr].append(addr0)
	elif mainaddr not in Author_Addr[name0]['Organization']:
		for addr in Address_set:
			addr0=(data0.loc[j])[addr]
			Author_Addr[name0][addr].append(addr0)
#now 'Author_Addr' is a defaultdict containing the addresses of each subsets with the same author name under the corresponding condition
Author_Num=len(Author_Addr)
print('number of authors: ',Author_Num)
#Remove double quotes
para1=0
for nm in Author_Addr:
	if para1%10000==0:
		print(para1,'/',Author_Num)
	for addr in Address_set:
		for i in range(len(Author_Addr[nm][addr])):
			if Author_Addr[nm][addr][i] is None or '"' not in Author_Addr[nm][addr][i]:
				continue
			Author_Addr[nm][addr][i]=Author_Addr[nm][addr][i].replace('"','')
	para1+=1


file1 =open('/mnt/sdb/wos2018-wwh/Disambiguation/Authorship_Institution/AD_AuthorShip_AddrDict_'+STY+'to'+EDY+'.pickle', 'wb')
pickle.dump(Author_Addr, file1)
file1.close()

















