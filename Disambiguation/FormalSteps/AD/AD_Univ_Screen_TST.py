from collections import defaultdict
import pickle

#Manually choose the original authorship_address file you want. mind: 1.the field 2.time period
AuAddata=open('/mnt/sdb/wos2018-wwh/Disambiguation/Authorship_Institution/AD_AuthorShip_AddrDict_2008to2016.pickle','rb')
AuAd=pickle.load(AuAddata)
AuAddata.close()

STY=2008 #<<--------set the start year
EDY=2016 #<<--------set the end year

STPWD=['University','university','of','&','(',')','de','Institute','-','Univ','univ','Universidade','universidade','Inst','inst','Ctr','ctr','for','la','Universite','universite','Universidad','universidad','do','Istituto','istituto','Institut','institut','di','Universiti','universiti','Universitat','universitat','Universidade','universidade','Ltd','Co','Universitario','universitario','Universitaire','universitaire','Universita','universita','Corp','Inc']
#the common stop words that will disrupt the disambiguation process (optional for use or not)
UnivWD=['Univ','univ','U']
#the words represent university
THRESHOLD=2 #<<<-------------set the threshold HERE!!
#set the threshold for filtering
AuAdPOOL=defaultdict(dict)



Author_Num=len(AuAd)
print('number of authors:', Author_Num,'\n')


for nm0 in AuAd.keys():
	print(nm0)
	org=AuAd[nm0]['Organization']
	print('institution list:\n',org)
	print('Institution Country List:',AuAd[nm0]['Country'])
	addrlen=len(AuAd[nm0]['Organization'])
	AuAdPOOL[nm0]=defaultdict(list)
	if addrlen<=1:
		para0+=1
		continue
	for i in range(addrlen):
		print('Candidate i:',org[i])
		print('Cd i Crty:',AuAd[nm0]['Country'][i])
		input()
		if org[i]=='*' or org[i]=='' or AuAd[nm0]['Country'][i]=='*' or AuAd[nm0]['Country'][i]=='':
			continue
		elif UnivWD[0] not in org[i] and UnivWD[1] not in org[i]:
			if not org[i].isupper() or UnivWD[2] not in org[i]:
				continue
		i_org=org[i]
		print('Qualified i:',i_org)
		print('Country i:',AuAd[nm0]['Country'][i])
		input()
		for j in range(i+1,addrlen):
			print('Candidate:',org[j])
			print('Cd j Crty:',AuAd[nm0]['Country'][j])
			input()
			if org[j]=='*' or org[j]=='' or AuAd[nm0]['Country'][j]=='*' or AuAd[nm0]['Country'][j]=='':
				continue
			elif UnivWD[0] not in org[i] and UnivWD[1] not in org[i]:
				if not org[i].isupper() or UnivWD[2] not in org[i]:
					continue
			elif AuAd[nm0]['Country'][i]!=AuAd[nm0]['Country'][j]: #make sure they have valid country inf. and are from the same country (rule 5)
				continue
			j_org=org[j]
			print('Qualified j:',j_org)
			print('Country j:',AuAd[nm0]['Country'][j])
			#deal with the stop words and punctuations
			i_STW=i_org.split() #the 'list' of split institution name
			i_len=len(i_STW)
			j_STW=j_org.split()
			j_len=len(j_STW)
			for stw in STPWD:
				for i0 in range(i_len):
					if stw in i_STW:
						i_STW.remove(stw)
				for j0 in range(j_len):
					if stw in j_STW:
						j_STW.remove(stw)
			i_Nspc="".join(i_STW) #Recombine the institution name without space
			j_Nspc="".join(j_STW)
			print('Recombined i:',i_Nspc)
			print('Recombined j:',j_Nspc)
			input()