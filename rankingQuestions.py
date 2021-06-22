import pandas as pd
import numpy as np
from cleanQuestions import getClean
import re

dic_analysis, dic_responses = getClean()

# Ranking 
df_ranking_list = []

# Participants didnt answer part of question
dic_analysis.pop('JH048')
dic_analysis.pop('AH001')
dic_responses.pop('JH048')
dic_responses.pop('AH001')

# Getting correct columns
for (sheet,df) in dic_responses.items():
    df_ranking_color = df.iloc[[41,42,43,44,45],:].copy()
    df_ranking_same_features = df.iloc[[50,51,52,53,54,55,56,57,58,59],:].copy()
    df_ranking_size = df.iloc[[75,76,77,78,79,80,81,82,83,84],:].copy()
    df_ranking_list.append(df_ranking_color)
    df_ranking_list.append(df_ranking_same_features)
    df_ranking_list.append(df_ranking_size)

df_ranking_all = pd.concat(df_ranking_list,ignore_index=True)
df_ranking_ofp = df_ranking_all.iloc[:,[7,8,9]].copy()
df_ranking_all.drop(columns=[6,7,8,9], inplace=True)

df_ranking_eyetracking_list = []

for (sheet,df) in dic_analysis.items():
    df_ranking_color_eyetracking = df.iloc[18:23,:]
    df_ranking_samefeatures_eyetracking = df.iloc[27:37,:]
    df_ranking_size_eyetracking = df.iloc[52:62,:]
    df_ranking_eyetracking_list.append(df_ranking_color_eyetracking)
    df_ranking_eyetracking_list.append(df_ranking_samefeatures_eyetracking)
    df_ranking_eyetracking_list.append(df_ranking_size_eyetracking)

df_ranking_eyetracking_all = pd.concat(df_ranking_eyetracking_list,ignore_index=True)

df_ranking_all[0] = df_ranking_all[0].str.lstrip()

phone1_names = ['Nokia Lumia 1520 Green','Samsung Galaxy S5','Micromax Canvas Gold','HTC One E8','Motorola Droid Turbo']
phone2_names = ['Nokia Lumia 1520 White','Motorola Droid Maxx','Huawei Ascend G620S','iPhone 6 Plus','iPhone 6 Plus White']
phone3_names = ['Nokia Lumia 1520 Red','LG G2','Samsung Galaxy A5','Blackberry Z30',"Blackberry Porsche Design P'9981"]
phone4_names = ['Nokia Lumia 1520 Black','Apple iPhone 6','Panasonic P31','Nokia Lumia 930','Blu Win HD']
phone5_names = ['Nokia Lumia 1520 Yellow','Google Nexus 5','HTC Butterfly','Nokia N8','Nokia 808 Pureview']

df_ranking_all.replace(phone1_names,'Phone 1',inplace=True)
df_ranking_all.replace(phone2_names,'Phone 2',inplace=True)
df_ranking_all.replace(phone3_names,'Phone 3',inplace=True)
df_ranking_all.replace(phone4_names,'Phone 4',inplace=True)
df_ranking_all.replace(phone5_names,'Phone 5',inplace=True)

df_rank1 = df_ranking_all.iloc[:,[0,1]].copy()
df_rank1.dropna(inplace=True)
df_rank1.drop(columns=[1], inplace=True)
df_rank1.reset_index(drop=True,inplace=True)

df_rank2 = df_ranking_all.iloc[:,[0,2]].copy()
df_rank2.dropna(inplace=True)
df_rank2.drop(columns=[2], inplace=True)
df_rank2.reset_index(drop=True,inplace=True)

df_rank3 = df_ranking_all.iloc[:,[0,3]].copy()
df_rank3.dropna(inplace=True)
df_rank3.drop(columns=[3], inplace=True)
df_rank3.reset_index(drop=True,inplace=True)

df_rank4 = df_ranking_all.iloc[:,[0,4]].copy()
df_rank4.dropna(inplace=True)
df_rank4.drop(columns=[4], inplace=True)
df_rank4.reset_index(drop=True,inplace=True)

df_rank5 = df_ranking_all.iloc[:,[0,5]].copy()
df_rank5.dropna(inplace=True)
df_rank5.drop(columns=[5], inplace=True)
df_rank5.reset_index(drop=True,inplace=True)

df_ranking_clean = pd.concat([df_rank1,df_rank2,df_rank3,df_rank4,df_rank5],axis=1,ignore_index=True)
df_ranking_clean.rename(columns={0:'Rank 1',1:'Rank 2',2:'Rank 3',3:'Rank 4',4:'Rank 5'},inplace=True)


# Eyetracking - splitting eyetracking into 5 phones
phone1_ofp = df_ranking_ofp.iloc[::5].copy()
phone2_ofp = df_ranking_ofp.iloc[1::5].copy()
phone3_ofp = df_ranking_ofp.iloc[2::5].copy()
phone4_ofp = df_ranking_ofp.iloc[3::5].copy()
phone5_ofp = df_ranking_ofp.iloc[4::5].copy()

phone1_ofp.rename(columns={7:'Phone 1 - Owned',8:'Phone 1 - Familiarity',9:'Phone 1 - Present'},inplace=True)
phone1_ofp.reset_index(drop=True,inplace=True)
phone2_ofp.rename(columns={7:'Phone 2 - Owned',8:'Phone 2 - Familiarity',9:'Phone 2 - Present'},inplace=True)
phone2_ofp.reset_index(drop=True,inplace=True)
phone3_ofp.rename(columns={7:'Phone 3 - Owned',8:'Phone 3 - Familiarity',9:'Phone 3 - Present'},inplace=True)
phone3_ofp.reset_index(drop=True,inplace=True)
phone4_ofp.rename(columns={7:'Phone 4 - Owned',8:'Phone 4 - Familiarity',9:'Phone 4 - Present'},inplace=True)
phone4_ofp.reset_index(drop=True,inplace=True)
phone5_ofp.rename(columns={7:'Phone 5 - Owned',8:'Phone 5 - Familiarity',9:'Phone 5 - Present'},inplace=True)
phone5_ofp.reset_index(drop=True,inplace=True)

eyetracking_phone1 = df_ranking_eyetracking_all.iloc[::5].copy()
eyetracking_phone2 = df_ranking_eyetracking_all.iloc[1::5].copy()
eyetracking_phone3 = df_ranking_eyetracking_all.iloc[2::5].copy()
eyetracking_phone4 = df_ranking_eyetracking_all.iloc[3::5].copy()
eyetracking_phone5 = df_ranking_eyetracking_all.iloc[4::5].copy()

eyetracking_phone1.reset_index(drop=True,inplace=True)
eyetracking_phone2.reset_index(drop=True,inplace=True)
eyetracking_phone3.reset_index(drop=True,inplace=True)
eyetracking_phone4.reset_index(drop=True,inplace=True)
eyetracking_phone5.reset_index(drop=True,inplace=True)

eyetracking_phone1.drop(columns=[' AOI Name', 'Unnamed: 11'], inplace=True)
eyetracking_phone2.drop(columns=[' AOI Name', ' AOI Start (sec)', ' AOI Duration (sec - U=UserControlled)', ' Viewers (#)', ' Ave Time to 1st View (sec)', ' Total Viewers (#)', ' Revisitors (#)', 'Unnamed: 11'], inplace=True)
eyetracking_phone3.drop(columns=[' AOI Name', ' AOI Start (sec)', ' AOI Duration (sec - U=UserControlled)', ' Viewers (#)', ' Ave Time to 1st View (sec)', ' Total Viewers (#)', ' Revisitors (#)', 'Unnamed: 11'], inplace=True)
eyetracking_phone4.drop(columns=[' AOI Name', ' AOI Start (sec)', ' AOI Duration (sec - U=UserControlled)', ' Viewers (#)', ' Ave Time to 1st View (sec)', ' Total Viewers (#)', ' Revisitors (#)', 'Unnamed: 11'], inplace=True)
eyetracking_phone5.drop(columns=[' AOI Name', ' AOI Start (sec)', ' AOI Duration (sec - U=UserControlled)', ' Viewers (#)', ' Ave Time to 1st View (sec)', ' Total Viewers (#)', ' Revisitors (#)', 'Unnamed: 11'], inplace=True)

eyetracking_phone1.rename(columns={' Ave Time Viewed (sec)':'Phone 1 - Ave Time Viewed (sec)', ' Ave Time Viewed (%)':'Phone 1 -  Ave Time Viewed (%)', ' Ave Fixations (#)':'Phone 1 -  Ave Fixations (#)', ' Average Revisits (#)':'Phone 1 -  Average Revisits (#)'}, inplace=True)
eyetracking_phone2.rename(columns={' Ave Time Viewed (sec)':'Phone 2 - Ave Time Viewed (sec)', ' Ave Time Viewed (%)':'Phone 2 -  Ave Time Viewed (%)', ' Ave Fixations (#)':'Phone 2 -  Ave Fixations (#)', ' Average Revisits (#)':'Phone 2 -  Average Revisits (#)'}, inplace=True)
eyetracking_phone3.rename(columns={' Ave Time Viewed (sec)':'Phone 3 - Ave Time Viewed (sec)', ' Ave Time Viewed (%)':'Phone 3 -  Ave Time Viewed (%)', ' Ave Fixations (#)':'Phone 3 -  Ave Fixations (#)', ' Average Revisits (#)':'Phone 3 -  Average Revisits (#)'}, inplace=True)
eyetracking_phone4.rename(columns={' Ave Time Viewed (sec)':'Phone 4 - Ave Time Viewed (sec)', ' Ave Time Viewed (%)':'Phone 4 -  Ave Time Viewed (%)', ' Ave Fixations (#)':'Phone 4 -  Ave Fixations (#)', ' Average Revisits (#)':'Phone 4 -  Average Revisits (#)'}, inplace=True)
eyetracking_phone5.rename(columns={' Ave Time Viewed (sec)':'Phone 5 - Ave Time Viewed (sec)', ' Ave Time Viewed (%)':'Phone 5 -  Ave Time Viewed (%)', ' Ave Fixations (#)':'Phone 5 -  Ave Fixations (#)', ' Average Revisits (#)':'Phone 5 -  Average Revisits (#)'}, inplace=True)

ranking_responses = pd.concat([df_ranking_clean,phone1_ofp,phone2_ofp,phone3_ofp,phone4_ofp,phone5_ofp,eyetracking_phone1,eyetracking_phone2,eyetracking_phone3,eyetracking_phone4,eyetracking_phone5], axis=1)
ranking_responses.rename(columns={0:'Phone Choice'}, inplace=True)

print(ranking_responses)
# writer = pd.ExcelWriter('output.xlsx')
# # write dataframe to excel
# ranking_responses.to_excel(writer)
# # save the excel
# writer.save()
