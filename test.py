import pandas as pd

file_path = './data.xlsx'

'''
df1 = pd.DataFrame(data=[[1,2,3],[4,5,6],[7,8,9]])
df2 = pd.DataFrame(data=[[2,2,3],[4,5,6],[7,8,9]])
df3 = pd.DataFrame(data=[[3,2,3],[4,5,6],[7,8,9]])

writer = pd.ExcelWriter(file_path, engine='xlsxwriter')

df1.to_excel(writer, sheet_name='1', index=False)
df2.to_excel(writer, sheet_name='2', index=False)
df3.to_excel(writer, sheet_name='3', index=False)

writer.save()
'''

d1 = pd.read_excel(file_path, sheet_name='1')
d2 = pd.read_excel(file_path, sheet_name='2')
d3 = pd.read_excel(file_path, sheet_name='3')
print(d1,d2,d3)