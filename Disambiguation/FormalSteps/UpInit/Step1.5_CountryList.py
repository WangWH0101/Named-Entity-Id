import os
import re
import pickle
import pandas as pd
from collections import defaultdict

'''
This program aims to find all the countries and corresponding address number
'''

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


data=pd.DataFrame()
CRY=STY
while CRY<=EDY:
	print('Current Year:', CRY)
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
addrNum=data.shape[0]
print('Number of institutions and adresses: ',addrNum)

CtryNum=defaultdict(int)

for i in range(addrNum):
	if i%100000==0:
			print(i,'/',addrNum)
	ctry=data.loc[i,'Country'] #the country of the corresponding address
	CtryNum[ctry]+=1


Rk_CtryNum=sorted(CtryNum.items(),key=lambda x:x[1],reverse=True)

fp=open('/mnt/sdb/wos2018-wwh/Disambiguation/CLC_Address/AD_CLC_CtryNMandAddrNumRank_'+str(STY)+'_'+str(EDY)+'.pickle','wb')
pickle.dump(Rk_CtryNum,fp)
fp.close()