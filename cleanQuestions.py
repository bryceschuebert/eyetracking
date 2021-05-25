import pandas as pd
import re
import numpy as np


def getClean():
    # Read in excel files
    dic_responses = pd.read_excel('excelFiles\Mobile Phone Eye Tracking Survey Responses.xlsx', header=None, sheet_name=None)
    dic_analysis = pd.read_excel('excelFiles\Mobile Phone Eye Tracking Survey Data Analysis.xlsx', sheet_name=None)

    # Pop personal info from sheet 1
    demographic_df = dic_responses['Sheet1']
    dic_responses.pop('Sheet1')

    user_code_df = dic_analysis['Sheet1']
    dic_analysis.pop('Sheet1')

    # Delete empty sheets from workbook
    empty_sheets_responses = [sheet for (sheet,df) in dic_responses.items() if df.empty]
    for sheet in empty_sheets_responses:
        dic_responses.pop(sheet)

    empty_sheets_analysis = [sheet for (sheet,df) in dic_analysis.items() if df.empty]
    for sheet in empty_sheets_analysis:
        dic_analysis.pop(sheet)

    # Delete rejected sheets from workbook
    rejected_sheets_responses = [sheet for (sheet,df) in dic_responses.items() if re.search(r'\AX',sheet)]
    for sheet in rejected_sheets_responses:
        dic_responses.pop(sheet)

    used_sheet_responses = [sheet for (sheet,df) in dic_responses.items()]
    sheets_analysis = [sheet for (sheet,df) in dic_analysis.items()]
    rejected_sheets_analysis = [sheet for sheet in sheets_analysis if sheet not in used_sheet_responses]

    for sheet in rejected_sheets_analysis:
        dic_analysis.pop(sheet)
    return dic_analysis, dic_responses