import pandas as pd
import numpy as np
from cleanQuestions import getClean
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import ComplementNB
from sklearn import svm
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier

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

# Machine learning - Classification

df_likert.drop(columns=['Phone Name', ' AOI Start (sec)', ' AOI Duration (sec - U=UserControlled)', ' Viewers (#)', ' Total Viewers (#)', ' Ave Time to 1st View (sec)', ' Revisitors (#)'], inplace=True) #, 'Owned', 'Familiarity', 'Present'

print(df_likert.groupby(by='Likert Rating').size())

y = df_likert['Likert Rating'].tolist()
X_df = df_likert.drop(columns=['Likert Rating'])
X = X_df.values.tolist()
X_train, X_test, y_train, y_test = train_test_split(X,y,stratify=y,test_size=0.2,random_state=501)

# clf = svm.SVC()
# clf = SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3,random_state=42,max_iter=10,tol=None)
# clf = KNeighborsClassifier(n_neighbors=8)
# clf = RandomForestClassifier(n_estimators=10)
# clf = ComplementNB()
clf = AdaBoostClassifier()
y_pred = clf.fit(X_train, y_train).predict(X_test)

print(metrics.confusion_matrix(y_test,y_pred))
print(metrics.classification_report(y_test, y_pred, target_names=['Rank 1','Rank 2','Rank 3','Rank 4','Rank 5']))