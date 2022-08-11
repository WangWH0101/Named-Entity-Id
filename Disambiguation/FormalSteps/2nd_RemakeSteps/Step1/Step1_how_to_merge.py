import pandas as pd
import numpy as np


Author=pd.DataFrame({'ArticleID':[1,1,2,2,3,4],'AuthorOrder':[1,2,1,2,1,1],'Name':['a1','a2','b1','b2','c1','d1']})
Address=pd.DataFrame({'ArticleID':[1,1,1,2,2,2,3,3],'AuthorOrder':[1,1,2,1,2,2,1,1],'AdressOrder':[1,2,1,1,2,3,1,2],'Org':['ad1','ad2','ad1','bd1','bd2','bd3','cd1','cd2']})
print(Author)
print(Address)
AuAd=pd.merge(Author,Address,how='outer',on=['ArticleID','AuthorOrder'])
print(AuAd)
AuAd=AuAd.fillna('*')
lst=list(AuAd['Org'])
print(lst)




