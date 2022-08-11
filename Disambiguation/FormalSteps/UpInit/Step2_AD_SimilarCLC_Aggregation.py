import os
import re
import pandas as pd
from collections import defaultdict

'''
This program aims to aggregate the instutition names with 
1.same country
2.similar CLC (Levenshtein.Jaro>0.8)
'''

#The Jaccrad measure method
def Jaccrad(a,b):
	a_LST=list(a) #Notice that you can use 'set' to remove the same letters
	b_LST=list(b)
	temp=0
	for i in a_LST:
		if i in b_LST:
			temp=temp+1
	denominator=len(a_LST)+len(b_LST)-temp #并集
	jaccard_coefficient=float(temp/denominator)#交集
	return jaccard_coefficient

#set the start and end year here (the start and end year themself will be included)
STY=2008 #<<-----------set start year #cann't be earlier than 2008 when the data has no author-address inf
EDY=2014 #<<-----------set end year


#the file of original WoS data containing address inf(no author name inf!)
filePath = '/mnt/sdb/wos2018-wwh/Disambiguation/CLC_Address/'
all_files = os.listdir(filePath)
'''
Columns and Datatype:
CLC                object
Organization       object
SubOrganization    object
City               object
State              object
Country            object
PostalCode         object
dtype: object
'''

#create a defaultdict to record the IND candidate pairs under each country
IND_Cand=defaultdict(dict) 

CRY=STY
while CRY<=EDY:
	print('Current Year:', CRY)
	data=pd.DataFrame()
	for each_file in all_files:
		m = re.search("address_" + str(CRY), each_file)
		if m is None:
			continue
		else:
			filename = filePath + each_file
			data = data.append(pd.read_hdf(filename),ignore_index=True)
	#data now is the dataframe containing all the inf of CRY's papers' addresses
	CRY+=1
#now addresses of selected years are aggregated together
print('Number of institutions and adresses: ',data.shape[0])


#groupby using column 'Country'
AddrGrp=data.groupby(['Country'])
for Ctry, Addr in AddrGrp:
	print('Country: ',Ctry) #the country of the address groupby
	addrnum=Addr.shape[0] #the number of addresses
	print('Number of addresses: ',addrnum)
	
	
