import re
import os
import time
import pickle
import numpy as np
import pandas as pd
from collections import defaultdict

'''
1.this step will aggregate the addresses with the same authorship together 
in the specified field and further clean the original data

2.this program will find all the institution names with the same authorship 
under the corresponding requirement (field/discipline)
'''

#get_keys() is a 'list' through which you can find the keys of certain value in a 'dict'
def get_keys(d, value):
	return [k for k,v in d.items() if value == v]
def get_keys1(d, value):
	return [k for k,v in d.items() if value in v]

#the 'dict' of papers' fields
#Notice that one paper can have more than one disciplines!!!
FieldData=open('/mnt/sdb/data_hu_2018/update_data/dict_data/paper_fields_after_1990_list.pickle','rb')
PF=pickle.load(FieldData)
FieldData.close()

#the 'dict' of papers publication year
PYdata=open('/mnt/sdb/wos2018-junming/data-paper_year.pickle','rb')
PY=pickle.load(PYdata)
PYdata.close()

#the comparison table for unified paperID to the WoS original articleID
ppIDdata=open("/mnt/sdb/wos2018-junming/data-paper2wos.pkl", "rb")
ppID=pickle.load(ppIDdata)
ppIDdata.close()

#the file of original WoS data with both authors' name and the corresponding address
filePath = '/mnt/sdb/wos2018-wwh/Disambiguation/Authorship_Address_2nd/'
all_files = os.listdir(filePath)
year_list=[]
for each_file in all_files:
	m = re.search("address_(\d\d\d\d)", each_file)
	if m is None:
		continue
	else:
		year_list.append(m.group(1))
year_list = sorted(list(set(year_list)))
print('The year to consider (year_list):\n',year_list)
#the year_list here indicates the year of the files with both authors' name and addresses
#which is exactly the year we need to consider

STY=year_list[0]
EDY=year_list[len(year_list)-1]

'''
There are total 14 fields:
{'Chemistry', 'Computer and information technology', 'Business and management', 'Law', 'Engineering', 'Medicine', 'Social sciences', 
'Environmental and earth sciences', 'Physical sciences', 'Mathematics', 'Humanities', 'Multidisciplinary Sciences', 'Agriculture', 'Biology'}
This method performs better in: CS, Math
'''
TGF='Mathematics' #<<---------------set the target field here!!
TFP=set(get_keys1(PF,TGF)) #the 'set' of unified paperID in target field
print('Number of ',TGF,' papers: ',len(TFP))
#The abbreviation of specific fields
abbrTGF={'Computer and information technology':'CS','Mathematics':'Math'}


print('Start Calculating--------------------------------------')
#create a 'set' TYP to record the all the papers of target years
TYP=set()
for CRY in year_list:
	CRY=int(CRY)
	TYP=TYP.union(set(get_keys(PY,CRY))) #the 'set' of papers published in CRY
	print('papers of ',CRY,' : ',len(TYP))
TGP=TYP.intersection(TFP) #the 'set' of all papers published in target years of mathematics
#notice that the TGP includes the unified paperID instead of the original articleID from WoS database
	
#find the articleID of target papers (not the paperID)
TGartID=[]
para0=0
for id0 in TGP:
	TGartID.append(ppID[id0])
print('Number of target papers from ',STY,' to ',EDY,' in ',TGF,': ', len(TGartID),'\n')
#now we have a list of target papers' ArticleID
TGID=pd.DataFrame({'ArticleID':TGartID})
#TGID is a dataframe with the column 'ArticleID' containing all the target articleID


print('Start aggregate Authorship_Address files')
data=pd.DataFrame() #Create empty DF to record Authorship_Address information
#Now find all Authorship-Address files within year_list and combine
for CRY in year_list:
	for each_file in all_files:
		m = re.search("address_" + str(CRY), each_file)
		if m is None:
			continue
		else:
			filename = filePath + each_file
			print('Current file: ',each_file)
		data =data.append(pd.read_hdf(filename),ignore_index=True)
		#data is the original WoS database containing both authorship and addresses of each paper in 'CRY'
print('Number of addresses before clean: ',data.shape[0])
data=data[~data['Country'].isin([''])] #clean the rows without country address
data=data[~data['abbrFullName'].isin([''])] #clean the rows without abbreviated names
data=data.reset_index(drop=True)
print('Number of addresses after invalid inf clean: ',data.shape[0])


data0=pd.merge(data,TGID,on=['ArticleID'])
#data0 is the dataframe with all the target papers (Target year&field) and their corresponding inf.
#now you have the dataframe of necessary papers!
print('Number of eligible targets (Field&Year):\n',data0.shape[0])

print('Columns before drop: ',data0.columns)
cldrop=['ArticleID','AuthorOrder','AddressOrder','reprint']
for clname in cldrop:
	data0.drop([clname],axis=1,inplace=True)
print('Columns after drop: ',data0.columns)

#Clean the repetitive addresses
data0.drop_duplicates(inplace=True)
data0=data0.reset_index(drop=True)
print('Number of addresses after duplicate clean: ',data0.shape[0])



Author_Addr=defaultdict(dict)
#the address subsets we need is listed below
Address_set=['Organization','SubOrganization','City','State','Country','PostalCode']
#create a 'defaultdict' to record the addresses with the same author name in the corresponding year and field
print('Classification and Counting:')
datalen=data0.shape[0]
for j in range(0,datalen):
	if j%10000==0:
		print(j,'/',datalen)
	mainaddr=(data0.loc[j])['Organization']
	name0=(data0.loc[j])['abbrFullName']
	if name0 not in Author_Addr:
		Author_Addr[name0]=defaultdict(list)
	for addr in Address_set:
		addr0=data0.loc[j,addr]
		Author_Addr[name0][addr].append(addr0)
#now 'Author_Addr' is a defaultdict containing the addresses of each subsets with the same author name under the corresponding condition
Author_Num=len(Author_Addr)
print('Number of Author_Block: ',Author_Num)


file1 =open('/mnt/sdb/wos2018-wwh/Disambiguation/Authorship_Institution_2nd/Remake2nd_AuthorShip_AddrDict_'+abbrTGF[TGF]+'_'+STY+'to'+EDY+'.pickle', 'wb')
pickle.dump(Author_Addr, file1)
file1.close()

















