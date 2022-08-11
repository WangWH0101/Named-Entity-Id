import os
import re
import pandas as pd

'''
This is the all_discipline version of step 1
1.extend to all disciplines
2.extend the time period
(No adjustment is needed in this step)


this step aims to create a new dataframe file including the articleID, Authors' Fullname and 
address information during the years you set

!!!
The authors' full names must be changed to the formation of "full FirstName+abbreviated LastName/surname"
e.g., 'Li, Y' , 'Jin, BH' or 'Glanzel W' as shown in the original paper:
"In this table the author name is abbreviated as surname and initials as provided in the WoS"
'''


#set the start and end year here (the start and end year themself will be included)
STY=2008 #<<-----------set start year #cann't be earlier than 2008 when the data has no author-address inf
EDY=2016 #<<-----------set end year


#the file of original WoS data containing address inf(no author name inf!)
filePath = '/mnt/sdb/wos2018-parsed-AUTHOR-ADDRESS/'
all_files = os.listdir(filePath)
'''
Data Structure of these files:
2008~
(Note that data before 2008 lacks the correspondence between author and addresses!!!)
数据类型:
ArticleID          object
AuthorOrder         int64
AddressOrder        int64
Organization       object
SubOrganization    object
City               object
State              object
Country            object
PostalCode         object
dtype: object
'''

#the file of original WoS data containing authors' name
filePath1='/mnt/sdb/wos2018-parsed-Authorship/'
all_files1=os.listdir(filePath1)
'''
Data structure of these files:
数据类型:
ArticleID      object
AuthorOrder     int64
AuthorDAIS     object
FullName       object
LastName       object
FirstName      object
Email          object
AuthorORCID    object
AuthorRID      object
reprint          bool
dtype: object
'''
#-----------------------------------------------------------------------


CRY=STY
while CRY<=EDY:
	print('Current Year:', CRY)

	data=pd.DataFrame() #DataFrame recording author-address
	for each_file in all_files:
		m = re.search("WR_" + str(CRY) + "_", each_file)
		if m is None:
			continue
		else:
			filename = filePath + each_file
			data = data.append(pd.read_hdf(filename),ignore_index=True)
	#data now is the dataframe containing all the inf of CRY's papers' addresses

	'''
	#Fine tuning of 'data':Remove rows without valid 'ArticleID' and 'AuthorOrder'
	print('Number of addresses before clean: ',data.shape[0])
	'''
	data=data.fillna('*') #unify the NaN data as '*'
	'''
	data=data[~data['ArticleID'].isin(['','*'])]
	data=data[~data['AuthorOrder'].isin(['','*'])]
	data.reset_index(drop=True)
	print('Number of addresses after clean: ',data.shape[0])
	'''

	data1=pd.DataFrame() #DataFrame recording authorship(name)
	for each_file in all_files1:
		m = re.search("WR_" + str(CRY) + "_", each_file)
		if m is None:
			continue
		else:
			filename = filePath1 + each_file
			data1 = data1.append(pd.read_hdf(filename),ignore_index=True)
	#data1 now is the dataframe containing the authorship inf of papers in CRY
	#There are some NoneType data in the orginal data1!!

	'''
	#Fine tuning of 'data1':Remove rows without valid 'ArticleID' and 'AuthorOrder'
	print('Number of AuthorShip before clean: ',data1.shape[0])
	'''
	data1=data1.fillna('*') #unify the NaN data as '*'
	'''
	data1=data1[~data1['ArticleID'].isin(['','*'])]
	data1=data1[~data1['AuthorOrder'].isin(['','*'])]
	data1.reset_index(drop=True)
	print('Number of AuthorShip after clean: ',data1.shape[0])
	'''

	#NOTICE! Now there are two kinds of invalid data ''(empty) and '*'


	#-----------------TEST-----------------
	#This test is carried out to see 
	#the forms of invalid name ''and'*' are the known type
	NewNMlist=list(data['Country'])
	NMlength = len(NewNMlist)
	print('Number of NameList: ',NMlength)
	strList=[]
	for i in range(NMlength):
		if i%1000000==0:
			print(i,'/',NMlength)
		NM=NewNMlist[i]
		if type(NM) is str:
			for j in NM:
				if j.isalpha():
					strList.append(NM)
					break
	
	InvldList=set(NewNMlist)-set(strList)
	print('The invalid data form: ')
	print(InvldList)
	input()
	#Output: {'*'}
	#-----------------TEST-----------------
	CRY+=1