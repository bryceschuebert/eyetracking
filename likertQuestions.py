import pandas as pd
import numpy as np
from cleanQuestions import getClean

dic_analysis, dic_responses = getClean()

# Likert Scale Responses - How likely you are to purchase this phone
df_likert_list = []

for (sheet,df) in dic_responses.items():
    df_likert = df.iloc[np.r_[23:29,46:50,60:75],:]
    df_likert_list.append(df_likert)

df_eyetrack_likert_list = []

for (sheet,df) in dic_analysis.items():
    df_eyetrack_likert = df.iloc[np.r_[0:6,23:27,37:52],:]
    df_eyetrack_likert_list.append(df_eyetrack_likert)    

df_likert_all = pd.concat(df_likert_list,ignore_index=True)
df_eyetrack_likert_all = pd.concat(df_eyetrack_likert_list,ignore_index=True)
df_eyetrack_likert_all.drop(columns=[' AOI Name', 'Unnamed: 11'], inplace=True)

def get_likert_values(row):
    if row[1] == 'X':
        return '1'
    if row[2] == 'X':
        return '2'
    if row[3] == 'X':
        return '3'
    if row[4] == 'X':
        return '4'
    if row[5] == 'X':
        return '5'

df_likert_all['Likert Rating'] = df_likert_all.apply (get_likert_values, axis=1)
    
df_likert_all.drop(columns=[1,2,3,4,5,6],inplace=True)
df_likert_all.rename(columns={0:'Phone Name',7:'Owned',8:'Familiarity',9:'Present'},inplace=True)
df_likert = pd.concat([df_likert_all, df_eyetrack_likert_all],axis=1)

print(df_likert)