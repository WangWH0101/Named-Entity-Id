import pandas as pd

orifile="/mnt/sdb/wos2018-wwh/Disambiguation/Authorship_Address/Authorship_address_2012.hdf5"
oridata=pd.read_hdf(orifile)
oridata=oridata.replace('"','',regex=True)


Refile="/mnt/sdb/wos2018-wwh/Disambiguation/Authorship_Address_2nd/Remake2nd_Authorship_address_2012.hdf5"
Redata=pd.read_hdf(Refile)

data=oridata.append(Redata)
data=data.drop_duplicates(keep=False)
data=data.reset_index(drop=True)
Num=data.shape[0]
print('Number of rows left: ',Num)
for i in range(Num):
	org=data.loc[i,'Organization']
	if org=='*' or org=='':
		continue
	else:
		print(data.loc[i])
		input()

'''
Result: 
The original version is no more useful,
larger due to junk inf.
'''