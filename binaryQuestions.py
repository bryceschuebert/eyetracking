import pandas as pd
import numpy as np
from cleanQuestions import getClean
import re
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import ComplementNB
from sklearn import svm
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

dic_analysis, dic_responses = getClean()

# Binary Responses - Form Factor
df_binary_list = []

for (sheet,df) in dic_responses.items():
    df_binary = df.iloc[[29,30,31,32,33,34],:]
    df_binary_list.append(df_binary)

df_binary_all = pd.concat(df_binary_list,ignore_index=True)
df_binary_ofp = df_binary_all.iloc[:,[7,8,9]].copy()
df_binary_all.drop(columns=[2,3,4,5,6,7,8,9], inplace=True)
df_binary_all.dropna(inplace=True)

df_binary_eyetracking_list = []

for (sheet,df) in dic_analysis.items():
    df_binary_eyetracking = df.iloc[[6,7,8,9,10,11],:]
    df_binary_eyetracking_list.append(df_binary_eyetracking)

df_binary_eyetracking_all = pd.concat(df_binary_eyetracking_list,ignore_index=True)

# Making each question into phone 1 or phone 2
def turntable(row):
    if bool(re.search('LG Optimus L1 II Tri',row[0])) and bool(re.search('X',row[1])):
        return 'Phone 1'
    if bool(re.search('Apple iPhone 5',row[0])) and bool(re.search('X',row[1])):
        return 'Phone 2'
    if bool(re.search('HTC One Mini',row[0])) and bool(re.search('X',row[1])):
        return 'Phone 1'
    if bool(re.search('Sony Xperia Z3V',row[0])) and bool(re.search('X',row[1])):
        return 'Phone 2'
    if bool(re.search('Samsung Galaxy Y',row[0])) and bool(re.search('X',row[1])):
        return 'Phone 1'
    if bool(re.search('Sony Xperia Z1',row[0])) and bool(re.search('X',row[1])):
        return 'Phone 2'
    
phone_selection = df_binary_all.apply(turntable, axis=1)
phone_selection.reset_index(drop=True,inplace=True)

# OFP append to binary columns
phone1 = df_binary_ofp.iloc[::2].copy()
phone2 = df_binary_ofp.iloc[1::2].copy()

phone1.rename(columns={7:'Phone 1 - Owned',8:'Phone 1 - Familiarity',9:'Phone 1 - Present'},inplace=True)
phone1.reset_index(drop=True,inplace=True)
phone2.rename(columns={7:'Phone 2 - Owned',8:'Phone 2 - Familiarity',9:'Phone 2 - Present'},inplace=True)
phone2.reset_index(drop=True,inplace=True)

eyetracking_phone1 = df_binary_eyetracking_all.iloc[::2].copy()
eyetracking_phone2 = df_binary_eyetracking_all.iloc[1::2].copy()

eyetracking_phone1.reset_index(drop=True,inplace=True)
eyetracking_phone2.reset_index(drop=True,inplace=True)

eyetracking_phone1.drop(columns=[' AOI Name', 'Unnamed: 11', ' AOI Duration (sec - U=UserControlled)'], inplace=True)
eyetracking_phone2.drop(columns=[' AOI Name', ' AOI Start (sec)', ' AOI Duration (sec - U=UserControlled)', ' Viewers (#)', ' Total Viewers (#)', 'Unnamed: 11'], inplace=True)

eyetracking_phone1.rename(columns={' Ave Time to 1st View (sec)':'Phone 1 - Ave Time to 1st View (sec)', ' Ave Time Viewed (sec)':'Phone 1 - Ave Time Viewed (sec)', ' Ave Time Viewed (%)':'Phone 1 -  Ave Time Viewed (%)', ' Ave Fixations (#)':'Phone 1 -  Ave Fixations (#)', ' Revisitors (#)':'Phone 1 -  Revisitors (#)', ' Average Revisits (#)':'Phone 1 -  Average Revisits (#)'}, inplace=True)
eyetracking_phone2.rename(columns={' Ave Time to 1st View (sec)':'Phone 2 - Ave Time to 1st View (sec)', ' Ave Time Viewed (sec)':'Phone 2 - Ave Time Viewed (sec)', ' Ave Time Viewed (%)':'Phone 2 -  Ave Time Viewed (%)', ' Ave Fixations (#)':'Phone 2 -  Ave Fixations (#)', ' Revisitors (#)':'Phone 2 -  Revisitors (#)', ' Average Revisits (#)':'Phone 2 -  Average Revisits (#)'}, inplace=True)

binary_responses = pd.concat([phone_selection,phone1,phone2,eyetracking_phone1,eyetracking_phone2], axis=1)
binary_responses.rename(columns={0:'Phone Choice'}, inplace=True)


print(binary_responses.groupby(by='Phone Choice').size())

# Machine learning - Classification
y = binary_responses['Phone Choice'].tolist()
X_df = binary_responses.drop(columns=['Phone Choice'])
X = X_df.values.tolist()
X_train, X_test, y_train, y_test = train_test_split(X,y,stratify=y,test_size=0.2,random_state=501)

# clf = svm.SVC()
# clf = SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3,random_state=42,max_iter=10,tol=None)
# clf = KNeighborsClassifier(n_neighbors=8)
# clf = RandomForestClassifier(n_estimators=10)
clf = ComplementNB()
y_pred = clf.fit(X_train, y_train).predict(X_test)

print(metrics.confusion_matrix(y_test,y_pred))
print(metrics.classification_report(y_test, y_pred, target_names=['Phone 1','Phone 2']))