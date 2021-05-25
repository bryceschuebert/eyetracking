import pandas as pd
import numpy as np
from cleanQuestions import getClean
import math

dic_analysis, dic_responses = getClean()

# Binary Responses - Form Factor
df_binary_list = []

for (sheet,df) in dic_responses.items():
    df_binary = df.iloc[np.r_[29:35],:]
    df_binary_list.append(df_binary)

df_binary_all = pd.concat(df_binary_list,ignore_index=True)
df_binary_ofp = df_binary_all.iloc[:,[7,8,9]]
df_binary_all.drop(columns=[2,3,4,5,6,7,8,9], inplace=True)
df_binary_all.dropna(inplace=True)

def turntable(row):
    if row[0] == 'LG Optimus L1 II Tri' and row[1] == 'X':
        return 'Phone 1'
    if row[0] == 'Apple iPhone 5' and row[1] == 'X':
        return 'Phone 2'
    if row[0] == 'HTC One Mini' and row[1] == 'X':
        return 'Phone 1'
    if row[0] == 'Sony Xperia Z3V' and row[1] == 'X':
        return 'Phone 2'
    if row[0] == 'Samsung Galaxy Y' and row[1] == 'X':
        return 'Phone 1'
    if row[0] == ' Sony Xperia Z1' and row[1] == 'X':
        return 'Phone 2'
    


turntable_list = df_binary_all.apply(turntable, axis=1)
turntable_list.reset_index(drop=True,inplace=True)

print(turntable_list)
