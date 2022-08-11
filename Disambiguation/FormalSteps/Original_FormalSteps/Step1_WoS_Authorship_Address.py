import os
import re
import time
import pandas as pd

'''
this step aims to create a new dataframe file including the articleID, Authors' Fullname and 
address information during the years you set

!!!
The authors' full names must be changed to the formation of "full FirstName+abbreviated LastName/surname"
e.g., 'Li, Y' , 'Jin, BH' or 'Glanzel W' as shown in the original paper:
"In this table the author name is abbreviated as surname and initials as provided in the WoS"
'''


#set the start and end year here (the start and end year themself will be included)
STY=2008 #<<-----------set start year
EDY=2016 #<<-----------set end year


#the file of original WoS data (no author name inf!)
filePath = '/mnt/sdb/wos2018-parsed-AUTHOR-ADDRESS/'
all_files = os.listdir(filePath)

#the file of original WoS data containing authors' name
filePath1='/mnt/sdb/wos2018-parsed-Authorship/'
all_files1=os.listdir(filePath1)

CRY=STY
while CRY<=EDY:
	print('Current Year:', CRY)
	ndata=pd.DataFrame()
	data=pd.DataFrame()
	data1=pd.DataFrame()
	for each_file in all_files:
		m = re.search("WR_" + str(CRY) + "_", each_file)
		if m is None:
			continue
		else:
			filename = filePath + each_file
			data = data.append(pd.read_hdf(filename),ignore_index=True)
	#data now is the dataframe containing all the inf of CRY's papers' addresses
	for each_file in all_files1:
		m = re.search("WR_" + str(CRY) + "_", each_file)
		if m is None:
			continue
		else:
			filename = filePath1 + each_file
			data1 = data1.append(pd.read_hdf(filename),ignore_index=True)
	#data1 now is the dataframe containing the authorship inf of papers in CRY
	#There are some NoneType data in the orginal data1!!
	data1=data1.fillna('*') #unify the NoneType data as '*'
	
	#Restore the authors' name!!!here<<-----------------!!!
	NewNMlist=[] #create an empty list 'NewNMlist' to record the remade names by sequence
	print('Name Remake:')
	length1=data1.shape[0]
	print('total rows of authorship:',length1)
	for i in range(length1):
		if i%100000==0:
			print(i,'/',length1)
		fullNM=data1.loc[i,'FullName']
		firstNM=data1.loc[i,'FirstName'] #the first name of the author
		if firstNM=='*' or firstNM is None:
			NewNMlist.append('*')
			continue
		lastNM=data1.loc[i,'LastName']
		if lastNM=='*' or lastNM is None:
			NewNMlist.append('*')
			continue
		lastNM_up=''.join(list(filter(str.isupper, lastNM))) #The last name will be changed to a combination of initial capital letters
		NewNM=','.join([firstNM,lastNM_up])
		NewNMlist.append(NewNM)
	data1['abbrFullName']=NewNMlist
	#for example both Bob Williams and Bob Wilson will be restored as Bob,W after this process
	#Too slow!!	


	#Now we need to filter out the columns we need and splice them according to the articleID
	#print('original columns:\n',data1.columns,'\n')
	clkeep1=['ArticleID','AuthorOrder','abbrFullName','reprint']
	for clname in data1.columns:
		if clname not in clkeep1:
			data1.drop([clname],axis=1,inplace=True)
	#delete the unnecessary information in data1
	#print('the columns after delete:\n',data1.columns,'\n')
	#now merge the two dataframe according to their articleID and AuthorOrder
	ndata=pd.merge(data,data1,how='outer',on=['ArticleID','AuthorOrder'])
	#ndata now is the dataframe containing the authors' name and their address inf.
	ndata=ndata.fillna('*')
	ndata.to_hdf('/mnt/sdb/wos2018-wwh/Disambiguation/Authorship_Address/Authorship_address_'+str(CRY)+'.hdf5','s')
	if CRY==STY:
		print('Ignore The Warining!!')
	CRY+=1




