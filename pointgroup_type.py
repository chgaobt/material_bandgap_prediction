import pandas as pd

file_name =  'MPData_wSpaceGroup.xlsx'
sheet = 0

df = pd.read_excel(file_name, sheet_name=sheet)
df = pd.concat([df[df.columns[15]]])
# print(df.head)

types = set()

for row in df:
    types.add(row)

print(len(types))