import pandas as pd

file="/mnt/sdb/wos2018-wwh/Disambiguation/Authorship_Address/Authorship_address_2012.hdf5"
data=pd.read_hdf(file)

print('数据类型:\n',data.dtypes,'\n')
print('index看行名:\n', data.index, '\n')
print('columns看行名:\n', data.columns, '\n')
print('看前两行:\n', data.head(2), '\n')
print('看后两行:\n', data.tail(2), '\n')