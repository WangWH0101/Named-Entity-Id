import pickle

WdFrdata=open(r'D:\桌面\111\now research\CiData\whole_strict_fractionCounting\Disambiguation\InsNM_WordFrequency\WordFrequency_insNM_2008_2016.pickle','rb')
WdFr=pickle.load(WdFrdata)
WdFrdata.close()


WFRK=list(WdFr.items())
WFRK.sort(key=lambda x:x[1],reverse=True)


for i in WFRK:
	print(i,'\n')
	input()