import pandas as pd
import numpy as np
from cleanQuestions import getClean
import re

dic_analysis, dic_responses = getClean()

# Three choice binary responses - Color
df_threechoice_list = []

for (sheet,df) in dic_responses.items():
    df_threechoice = df.iloc[[35,36,37,38,39,40],:]
    df_threechoice_list.append(df_threechoice)

df_threechoice_all = pd.concat(df_threechoice_list,ignore_index=True)
df_threechoice_ofp = df_threechoice_all.iloc[:,[7,8,9]].copy()
df_threechoice_all.drop(columns=[2,3,4,5,6,7,8,9], inplace=True)
df_threechoice_all.dropna(inplace=True)

df_threechoice_eyetracking_list = []

for (sheet,df) in dic_analysis.items():
    df_threechoice_eyetracking = df.iloc[[6,7,8,9,10,11],:]
    df_threechoice_eyetracking_list.append(df_threechoice_eyetracking)

df_threechoice_eyetracking_all = pd.concat(df_threechoice_eyetracking_list,ignore_index=True)

def threechoice_search(row):
    if bool(re.search('HTC One M8 Silver',row[0])) and bool(re.search('X',row[1])):
        return 'Phone 1'
    if bool(re.search('HTC One M8 Gold',row[0])) and bool(re.search('X',row[1])):
        return 'Phone 2'
    if bool(re.search('HTC One M8 Black',row[0])) and bool(re.search('X',row[1])):
        return 'Phone 3'
    if bool(re.search('Apple iPhone 5c Blue',row[0])) and bool(re.search('X',row[1])):
        return 'Phone 1'
    if bool(re.search('Apple iPhone 5c Green',row[0])) and bool(re.search('X',row[1])):
        return 'Phone 2'
    if bool(re.search('Apple iPhone 5c Yellow',row[0])) and bool(re.search('X',row[1])):
        return 'Phone 3'

phone_selection_color = df_threechoice_all.apply(threechoice_search, axis=1)
phone_selection_color.reset_index(drop=True,inplace=True)

phone1 = df_threechoice_ofp.iloc[::3].copy()
phone2 = df_threechoice_ofp.iloc[1::3].copy()
phone3 = df_threechoice_ofp.iloc[2::3].copy()


phone1.rename(columns={7:'Phone 1 - Owned',8:'Phone 1 - Familiarity',9:'Phone 1 - Present'},inplace=True)
phone1.reset_index(drop=True,inplace=True)
phone2.rename(columns={7:'Phone 2 - Owned',8:'Phone 2 - Familiarity',9:'Phone 2 - Present'},inplace=True)
phone2.reset_index(drop=True,inplace=True)
phone3.rename(columns={7:'Phone 3 - Owned',8:'Phone 3 - Familiarity',9:'Phone 3 - Present'},inplace=True)
phone3.reset_index(drop=True,inplace=True)

eyetracking_phone1 = df_threechoice_eyetracking_all.iloc[::3].copy()
eyetracking_phone2 = df_threechoice_eyetracking_all.iloc[1::3].copy()
eyetracking_phone3 = df_threechoice_eyetracking_all.iloc[2::3].copy()

eyetracking_phone1.reset_index(drop=True,inplace=True)
eyetracking_phone2.reset_index(drop=True,inplace=True)
eyetracking_phone3.reset_index(drop=True,inplace=True)

eyetracking_phone1.drop(columns=[' AOI Name', 'Unnamed: 11'], inplace=True)
eyetracking_phone2.drop(columns=[' AOI Name', ' AOI Start (sec)', ' AOI Duration (sec - U=UserControlled)', ' Viewers (#)', ' Total Viewers (#)', 'Unnamed: 11'], inplace=True)
eyetracking_phone3.drop(columns=[' AOI Name', ' AOI Start (sec)', ' AOI Duration (sec - U=UserControlled)', ' Viewers (#)', ' Total Viewers (#)', 'Unnamed: 11'], inplace=True)

eyetracking_phone1.rename(columns={' Ave Time to 1st View (sec)':'Phone 1 - Ave Time to 1st View (sec)', ' Ave Time Viewed (sec)':'Phone 1 - Ave Time Viewed (sec)', ' Ave Time Viewed (%)':'Phone 1 -  Ave Time Viewed (%)', ' Ave Fixations (#)':'Phone 1 -  Ave Fixations (#)', ' Revisitors (#)':'Phone 1 -  Revisitors (#)', ' Average Revisits (#)':'Phone 1 -  Average Revisits (#)'}, inplace=True)
eyetracking_phone2.rename(columns={' Ave Time to 1st View (sec)':'Phone 2 - Ave Time to 1st View (sec)', ' Ave Time Viewed (sec)':'Phone 2 - Ave Time Viewed (sec)', ' Ave Time Viewed (%)':'Phone 2 -  Ave Time Viewed (%)', ' Ave Fixations (#)':'Phone 2 -  Ave Fixations (#)', ' Revisitors (#)':'Phone 2 -  Revisitors (#)', ' Average Revisits (#)':'Phone 2 -  Average Revisits (#)'}, inplace=True)
eyetracking_phone3.rename(columns={' Ave Time to 1st View (sec)':'Phone 3 - Ave Time to 1st View (sec)', ' Ave Time Viewed (sec)':'Phone 3 - Ave Time Viewed (sec)', ' Ave Time Viewed (%)':'Phone 3 -  Ave Time Viewed (%)', ' Ave Fixations (#)':'Phone 3 -  Ave Fixations (#)', ' Revisitors (#)':'Phone 3 -  Revisitors (#)', ' Average Revisits (#)':'Phone 3 -  Average Revisits (#)'}, inplace=True)

threechoice_responses = pd.concat([phone_selection_color,phone1,phone2,phone3,eyetracking_phone1,eyetracking_phone2,eyetracking_phone3], axis=1)
threechoice_responses.rename(columns={0:'Phone Choice'}, inplace=True)

#print(threechoice_responses)

writer = pd.ExcelWriter('output.xlsx')
# write dataframe to excel
threechoice_responses.to_excel(writer)
# save the excel
writer.save()