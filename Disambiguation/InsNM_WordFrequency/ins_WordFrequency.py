import re
import os
import pickle
import pandas as pd

'''
This program aims to count the word frequency in institution name
so that the list of stop word can be constructed
'''

STY=2008
EDY=2016

#the file of original WoS data containing address inf(no author name inf!)
filePath = '/mnt/sdb/wos2018-parsed-AUTHOR-ADDRESS/'
all_files = os.listdir(filePath)

data=pd.DataFrame()
WF=dict()

CRY=STY
while CRY<=EDY:
	print('Current Year:',CRY)
	for each_file in all_files:
		m = re.search("WR_" + str(CRY) + "_", each_file)
		if m is None:
			continue
		else:
			filename = filePath + each_file
			data = data.append(pd.read_hdf(filename),ignore_index=True)
	CRY+=1

addr=data['Organization']
addr=addr.fillna('*')
addr=addr.tolist()

addrlen=len(addr)
print('Number of Institution name:',addrlen)

para0=0
for insNM in addr:
	if para0%100000==0:
		print(para0,'/',addrlen)
	if insNM=='*' or insNM=='':
		para0+=1
		continue
	else:
		insNM=insNM.replace('"','')
		insWD=insNM.split()
		#print(insNM)
		for WD in insWD:
			if WD in WF.keys():
				WF[WD]+=1
			else:
				WF[WD]=1
		#print(WF,'\n')
		#input()
		para0+=1

fp=open('/mnt/sdb/wos2018-wwh/Disambiguation/Authorship_Institution/WordFrequency_insNM_'+str(STY)+'_'+str(EDY)+'.pickle','wb')
pickle.dump(WF,fp)
fp.close()