import pandas as pd
import re
import numpy as np

# Read in excel files
dic_responses = pd.read_excel('excelFiles\Mobile Phone Eye Tracking Survey Responses.xlsx', header=None, sheet_name=None)
dic_analysis = pd.read_excel('excelFiles\Mobile Phone Eye Tracking Survey Data Analysis.xlsx', sheet_name=None)

demographic_df = dic_responses['Sheet1']
dic_responses.pop('Sheet1')

# Delete empty sheets from workbook
empty_sheets_responses = [sheet for (sheet,df) in dic_responses.items() if df.empty]
for sheet in empty_sheets_responses:
    dic_responses.pop(sheet)

empty_sheets_analysis = [sheet for (sheet,df) in dic_responses.items() if df.empty]
for sheet in empty_sheets_analysis:
    dic_analysis.pop(sheet)

# Delete rejected sheets from workbook
rejected_sheets_responses = [sheet for (sheet,df) in dic_responses.items() if re.search(r'\AX',sheet)]
for sheet in rejected_sheets_responses:
    dic_responses.pop(sheet)

# Likert Scale Responses - How likely you are to purchase this phone
df_likert_list = []

for (sheet,df) in dic_responses.items():
    df_likert = df.iloc[np.r_[23:29,46:50,60:75],:]
    df_likert_list.append(df_likert)

df_likert_all = pd.concat(df_likert_list,ignore_index=True)

print(df_likert_all)