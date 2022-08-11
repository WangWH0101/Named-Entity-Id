import pickle
import re
import os

FilePath=r"D:\桌面\111\now research\CiData\whole_strict_fractionCounting\Disambiguation\FormalSteps\AD\MiddleFile\Result"
all_files=os.listdir(FilePath)


print('Set the threshold value (2~10) :')
thrshd=input()




for each_file in all_files:
	m=re.search("Threshold_"+str(thrshd),each_file)
	if m is None:
		continue
	else:
		filename=FilePath+'\\'+each_file
		data=pickle.load(open(filename,'rb'))
	print('Number of groups:',len(data.keys()))
for ky in data.keys():
	print(ky)
	print(data[ky])
	input()
