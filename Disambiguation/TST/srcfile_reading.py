import pickle
import pandas as pd

'''
filename = "/mnt/sdb/wos2018-parsed-AUTHOR-ADDRESS/data-wos-2018-WR_2007_20180216044010_DSSU_0003-author-addr.hdf5"
data=pd.read_hdf(filename)
#print('列的数据类型:\n',type(data.Country),'\n')
#print((data.Country).head(2))
print('数据类型:\n',data.dtypes,'\n')
print('index看行名:\n', data.index, '\n')
print('columns看行名:\n', data.columns, '\n')
print('看前两行:\n', data.head(2), '\n')
print('看后两行:\n', data.tail(2), '\n')
'''

'''
2008~
数据类型:
ArticleID          object
AuthorOrder         int64
AddressOrder        int64
Organization       object
SubOrganization    object
City               object
State              object
Country            object
PostalCode         object
dtype: object
'''

#ilename1="/mnt/sdb/wos2018-parsed-Article/data-wos-2018-WR_2010_20180219093404_DSSU_0001-article.hdf5"
#data1=pd.read_hdf(filename1)
'''
print('数据类型:\n',data1.dtypes,'\n')
print('index看行名:\n', data1.index, '\n')
print('columns看行名:\n', data1.columns, '\n')
print('看前两行:\n', data1.head(2), '\n')
print('看后两行:\n', data1.tail(2), '\n')
'''
'''
数据类型:
ArticleID                    object
Title                        object
PubYear                       int64
PubMonth                     object
CoverDate                    object
SortDate                     object
Volume                       object
Issue                        object
PageBegin                   float64
PageEnd                     float64
PageCount                     int64
TeamSize                      int64
PubType                      object
Doctypes                     object
HasAbstract                  object
Journal                      object
Journal Abbreviation ISO     object
ISSN                         object
eISSN                        object
DOI                          object
PublisherDisplayName         object
PublisherFullName            object
dtype: object
'''
'''
filename2="/mnt/sdb/wos2018-parsed-Authorship/data-wos-2018-WR_2010_20180219093404_DSSU_0001-authorship.hdf5"
data2=pd.read_hdf(filename2)

print('数据类型:\n',data2.dtypes,'\n')
print('index看行名:\n', data2.index, '\n')
print('columns看行名:\n', data2.columns, '\n')
print('看前两行:\n', data2.head(2), '\n')
print('看后两行:\n', data2.tail(2), '\n')
'''

'''
数据类型:
ArticleID      object
AuthorOrder     int64
AuthorDAIS     object
FullName       object
LastName       object
FirstName      object
Email          object
AuthorORCID    object
AuthorRID      object
reprint          bool
dtype: object
'''

#filename3="/mnt/sdb/wos2018-parsed-PAPER-ADDRESS/wos2017-v2019a-WR_2010_20170217091518_DSSU_0001-paper-addr.hdf5"
#data3=pd.read_hdf(filename3)
'''
print('数据类型:\n',data3.dtypes,'\n')
print('index看行名:\n', data3.index, '\n')
print('columns看行名:\n', data3.columns, '\n')
print('看前两行:\n', data3.head(2), '\n')
print('看后两行:\n', data3.tail(2), '\n')
'''
'''
数据类型:
ArticleID          object
AddressOrder        int64
Organization       object
SubOrganization    object
City               object
State              object
Country            object
PostalCode         object
Reprint              bool
dtype: object
'''

'''
filename4=open("/mnt/sdb/wos2018-junming/data-wos2paper.pickle", "rb") #a 'dict'
data4=pickle.load(filename4)
filename4.close()
print(type(data4))
''' 


'''
print('Reprint Authorship:')
filename5="/mnt/sdb/wos2017reprint-AUTHORSHIP/data-wos-2017-WR_2008_20170203223619_DSSU_0001-authorship.hdf5"
data5=pd.read_hdf(filename5)
print('数据类型:\n',data5.dtypes,'\n')
print('index看行名:\n', data5.index, '\n')
print('columns看行名:\n', data5.columns, '\n')
print('看前两行:\n', data5.head(2), '\n')
print('看后两行:\n', data5.tail(2), '\n')
'''
'''
数据类型:
 ArticleID       object
AuthorOrder      int64
AuthorDAIS     float64
FullName        object
LastName        object
FirstName       object
Email           object
AuthorORCID     object
AuthorRID       object
reprint           bool
dtype: object

index看行名:
 Int64Index([      0,       1,       2,       3,       4,       5,       6,
                  7,       8,       9,
            ...
            1096813, 1096814, 1096815, 1096816, 1096817, 1096818, 1096819,
            1096820, 1096821, 1096822],
           dtype='int64', length=1096823)

columns看行名:
 Index(['ArticleID', 'AuthorOrder', 'AuthorDAIS', 'FullName', 'LastName',
       'FirstName', 'Email', 'AuthorORCID', 'AuthorRID', 'reprint'],
      dtype='object')

看前两行:
          ArticleID  AuthorOrder  AuthorDAIS         FullName  LastName FirstName Email AuthorORCID AuthorRID  reprint
0  000258261800306            1         NaN      Meli, A. L.      Meli     A. L.  None        None      None    False
1  000258261800306            2         NaN  Castilho, P. C.  Castilho     P. C.  None        None      None    False

看后两行:
                ArticleID  AuthorOrder  AuthorDAIS             FullName  LastName  FirstName           Email AuthorORCID AuthorRID  reprint
1096821  000256839900056            4         NaN  Whitford, Andrew S.  Whitford  Andrew S.            None        None      None    False
1096822  000256839900056            5   2267951.0  Schwartz, Andrew B.  Schwartz  Andrew B.  abs21@pitt.edu        None      None     True
'''


'''
print('\nReprint Address')
filename6="/mnt/sdb/wos2017reprint-AUTHOR-ADDRESS/data-wos-2017-WR_2008_20170203223619_DSSU_0001-author-addr.hdf5"
data6=pd.read_hdf(filename6)
print('数据类型:\n',data6.dtypes,'\n')
print('index看行名:\n', data6.index, '\n')
print('columns看行名:\n', data6.columns, '\n')
print('看前两行:\n', data6.head(2), '\n')
print('看后两行:\n', data6.tail(2), '\n')
'''
'''
数据类型:
 ArticleID          object
AuthorOrder         int64
AddressOrder        int64
Organization       object
SubOrganization    object
City               object
State              object
Country            object
PostalCode         object
dtype: object

index看行名:
 Int64Index([      0,       1,       2,       3,       4,       5,       6,
                  7,       8,       9,
            ...
            1094061, 1094062, 1094063, 1094064, 1094065, 1094066, 1094067,
            1094068, 1094069, 1094070],
           dtype='int64', length=1094071)

columns看行名:
 Index(['ArticleID', 'AuthorOrder', 'AddressOrder', 'Organization',
       'SubOrganization', 'City', 'State', 'Country', 'PostalCode'],
      dtype='object')

看前两行:
          ArticleID  AuthorOrder  AddressOrder             Organization              SubOrganization     City State   Country PostalCode
0  000258261800306            1             1  University of Yaounde I     Dept Organ Chem, Fac Sci  Yaounde  None  Cameroon       None
1  000258261800306            2             2  Universidade da Madeira  Dept Quim, Ctr Quim Madeira  Funchal  None  Portugal  P-9000390

看后两行:
                ArticleID  AuthorOrder  AddressOrder                                       Organization    ...            City State Country PostalCode
1094069  000256839900056            5             6  Pennsylvania Commonwealth System of Higher Edu...    ...      Pittsburgh    PA     USA      15219
1094070  000256839900056            5             7                         Carnegie Mellon University    ...      Pittsburgh    PA     USA      15213
'''







































