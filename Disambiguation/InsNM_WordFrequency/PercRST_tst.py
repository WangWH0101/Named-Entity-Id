import pickle
import pandas as pd

WdPcdata=open(r'D:\桌面\111\now research\CiData\whole_strict_fractionCounting\Disambiguation\InsNM_WordFrequency\WdPerc.pickle','rb')
WdPc=pickle.load(WdPcdata)
WdPcdata.close()


WPRK=list(WdPc.items())
WPRK.sort(key=lambda x:x[1],reverse=True)

WPRKPD=pd.DataFrame(WPRK)

WPRKPD.to_excel(r'D:\桌面\111\now research\CiData\whole_strict_fractionCounting\Disambiguation\InsNM_WordFrequency\WdPerc.xlsx')


