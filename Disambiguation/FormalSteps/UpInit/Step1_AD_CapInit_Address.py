import os
import re
import pandas as pd

'''
This program will aggregate the candidate addresses according to their
capital letter combination (CLC). The number of CLC is adjustable (1~...)

Without the limitation of authors' name and corresponding address, any year can be taken into consideration theoretically

All disciplines are considered in this program

First of all, we still think about the address inforamtion during 2008~2012

if the levenshtein.jaro result of the instutition pair's CLC is greater than 0.8, then they are put into the same group
'''


#set the start and end year here (the start and end year themself will be included)
STY=2008 #<<-----------set start year #cann't be earlier than 2008 when the data has no author-address inf
EDY=2014 #<<-----------set end year


#the file of original WoS data containing address inf(no author name inf!)
filePath = '/mnt/sdb/wos2018-parsed-PAPER-ADDRESS/'
all_files = os.listdir(filePath)
'''
Columns and Datatype:
ArticleID          object
AddressOrder        int64
Organization       object
SubOrganization    object
City               object
State              object
Country            object
PostalCode         object
Reprint              bool
dtype: object
'''

CRY=STY
while CRY<=EDY:
	print('Current Year:', CRY)
	data=pd.DataFrame()
	for each_file in all_files:
		m = re.search("WR_" + str(CRY) + "_", each_file)
		if m is None:
			continue
		else:
			filename = filePath + each_file
			data = data.append(pd.read_hdf(filename),ignore_index=True)
	#data now is the dataframe containing all the inf of CRY's papers' addresses
	
	#Now we need to clean out the columns we don't need
	print('original columns:\n',data.columns,'\n')
	cleanCL=['ArticleID','AddressOrder','Reprint'] #<------------the columns we don't need
	for clname in data.columns:
		if clname in cleanCL:
			data.drop([clname],axis=1,inplace=True)
	#delete the unnecessary information in data
	print('the columns after delete:\n',data.columns,'\n')
	
	#unify the NaN data as '*'
	data=data.fillna('*') 
	
	print('Number of addresses before cleaning: ',data.shape[0])
	data=data[~data['Country'].isin(['*',''])]
	#delete the rows without country information
	data=data[~data['Organization'].isin(['*',''])]
	#delete the rows without specific organization name
	print('Number of addresses after country and organization cleaning: ',data.shape[0])
	
	#reset the index
	data=data.reset_index(drop=True) 
	
	#Remove the " in the addresses
	data=data.replace('"','',regex=True)
	
	#Restore the institution name!!!here<<-----------------!!!
	NewNMlist=[] #create an empty list 'NewNMlist' to record the Capital Letter Combination (CLC) of institutions
	print('Name Remake:')
	length1=data.shape[0]
	print('total rows of authorship:',length1)
	for i in range(length1):
		if i%100000==0:
			print(i,'/',length1)
		InsNM=data.loc[i,'Organization']
		if InsNM is None:
			NewNMlist.append('*')
			continue
		CpLetComb=''.join(list(filter(str.isupper,InsNM)))
		NewNMlist.append(CpLetComb)
	data['CLC']=NewNMlist
	
	print('Number of addresses before InsName cleaning: ',data.shape[0])
	data=data[~data['Organization'].isin(['*',''])]
	#delete the rows without specific organization name
	print('Number of addresses after InsName cleaning: ',data.shape[0])
	
	#reset the index
	data=data.reset_index(drop=True) 
	
	data.to_hdf('/mnt/sdb/wos2018-wwh/Disambiguation/CLC_Address/AD_CLC_address_'+str(CRY)+'.hdf5','s')
	CRY+=1