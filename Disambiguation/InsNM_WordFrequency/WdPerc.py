import pickle

WdFrdata=open(r'D:\桌面\111\now research\CiData\whole_strict_fractionCounting\Disambiguation\InsNM_WordFrequency\WordFrequency_insNM_2008_2016.pickle','rb')
WdFr=pickle.load(WdFrdata)
WdFrdata.close()

TotalWdNM=0

for i in WdFr.keys():
	TotalWdNM+=WdFr[i]

WdPc=dict()

for i in WdFr.keys():
	WdPc[i]=WdFr[i]/TotalWdNM

fp=open(r'D:\桌面\111\now research\CiData\whole_strict_fractionCounting\Disambiguation\InsNM_WordFrequency\WdPerc.pickle','wb')
pickle.dump(WdPc,fp)
fp.close()
