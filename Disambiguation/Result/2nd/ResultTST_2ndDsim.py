import pickle

ISSdata = open(r"D:\桌面\111\now research\CiData\whole_strict_fractionCounting\Disambiguation\Result\2nd\Remake2nd_IND_Threshold_2_Math_2008to2016.pickle", 'rb')
ISS = pickle.load(ISSdata)
ISSdata.close()

def get_keys1(d, value):
    return [k for k, v in d.items() if value in v]

InsISS = set()
for i in ISS:
    InsISS = InsISS | ISS[i]

for InsNM in InsISS:
    RepNm=get_keys1(ISS, InsNM)
    if len(RepNm)>1:
        print('More than 1 matched!!!\n')
        print('Institution Name: ', InsNM)
        print('Represent ISS Name: \n', RepNm)
        print('Corresponding Groups:\n')
        for nm1 in RepNm:
            print('Group Name: ', nm1)
            print(ISS[nm1], '\n\n')
        print('+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n')
