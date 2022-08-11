import pickle

file=open(r'D:\桌面\111\now research\CiData\whole_strict_fractionCounting\Disambiguation\FormalSteps\UpInit\CountryAddrNum\AD_CLC_CtryNMandAddrNumRank_2008_2014.pickle','rb')
data=pickle.load(file)
file.close()

for i in range(len(data)):
	if 'Hongkong' in data[i][0]:
		print(data[i])
