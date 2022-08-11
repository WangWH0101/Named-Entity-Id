import pickle

DSRSTdata=open(r'D:\桌面\111\now research\CiData\whole_strict_fractionCounting\Disambiguation\AD_Univ_IND_Threshold_2_2008to2016.pickle','rb')
DSRST=pickle.load(DSRSTdata)
DSRSTdata.close()

for i in DSRST.keys():
	print(i,':',DSRST[i])
	input()
	'''
	for org in DSRST[i]:
		if 'California' in org:
			print(i,':',DSRST[i])
			input()
			break
	'''




