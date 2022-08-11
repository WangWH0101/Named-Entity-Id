import pickle

'''
This program aims to correct some obvious classification errors
'''

TGF="Mathematics" #<<-----------set the target field here!!
STY=2008 #<<---------set the start year here!
EDY=2016 #<<---------set the end year here!!
use_stwd=0 #<<-----------1 if you want to use the stop words/0 if you don't
#Check the stop words in step3
THRESHOLD=2 #<<-------------set the threshold HERE!!

#Read the corresponding file according to the settings
if use_stwd==1:
	file1 =open('/mnt/sdb/wos2018-wwh/Disambiguation/Result/IND_StopWd_Threshold_'+str(THRESHOLD)+'_'+TGF+'_'+str(STY)+'to'+str(EDY)+'.pickle', 'rb')
else:
	file1 =open('/mnt/sdb/wos2018-wwh/Disambiguation/Result/IND_Threshold_'+str(THRESHOLD)+'_'+TGF+'_'+str(STY)+'to'+str(EDY)+'.pickle', 'rb')
DisamDict=pickle.load(file1)
file1.close()

CalifSys="University of California System"
CaliUniv=[]


for rpnm in DisamDict.keys():
	if CalifSys in rpnm:
		print(rpnm,':')
		print(DisamDict[rpnm])