import pandas as pd
import numpy as np
import os
import glob
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn import metrics
from sklearn.utils import shuffle
from nltk.corpus import stopwords
from word2number import w2n
import re



package_path = os.path.dirname(os.path.abspath(__file__))
my_data_path = package_path + "/jesse_labeled_requirements"
#other_data_path = package_path + "/user_data"
my_files = glob.glob(my_data_path + "/*.xlsx")
#other_files = glob.glob(other_data_path + "/*.xlsx")
#all_files = my_files + other_files
df = pd.concat((pd.read_excel(f,usecols="A,B") for f in my_files),ignore_index=True)
df = df.loc[(df.Label == 'excessible') | (df.Label == 'not excessible')] # get rid of entries without the correct labels

# Split into Training and Testing Datasets
X = df.Requirements.tolist()
y = df.Label.tolist()
X_train, X_test, y_train, y_test = train_test_split(X,y,stratify=y,test_size=0.2,random_state=501)

def remove_noise(requirements):
    clean_requirements = []
    typed_nums = ['one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen','twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety']
    for requ in requirements:
        for typed_num in typed_nums:
            num = str(w2n.word_to_num(typed_num))
            requ = requ.replace(typed_num,num)
        requ = re.sub(r'\d+',"numeric",requ)
        requ = re.sub(r'[.,"\'-?:!;]', '', requ)
        clean_requirements.append(requ)
    return clean_requirements

X_train_clean = remove_noise(X_train)
X_test_clean = remove_noise(X_test)

# Get Stopwords
my_stop_words = stopwords.words('english')

# Create Pipeline
requ_clf = Pipeline([
('vect', CountVectorizer()),
('tfidf', TfidfTransformer()),
('clf', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3,random_state=42,max_iter=10,tol=None)),
])

# Train Model & Get Specs
requ_clf.fit(X_train_clean, y_train)
predicted = requ_clf.predict(X_test_clean)

#print(np.mean(predicted == y_test))
print(metrics.confusion_matrix(y_test, predicted))
print(metrics.classification_report(y_test, predicted, target_names=['Excessible','Not Excessible']))



# Get Testing Set with Equal Number of Labels

test_dict = {'Requirements':X_test, 'Label':y_test}
test_df = pd.DataFrame(test_dict)
test_excessible = test_df.loc[(test_df.Label == 'excessible')]
test_non_excessible = test_df.loc[(test_df.Label == 'not excessible')]
test_non_excess_sample = test_non_excessible.sample(n=len(test_excessible.index))

equal_df = shuffle(pd.concat([test_excessible,test_non_excess_sample],ignore_index=True))
X_equal = equal_df.Requirements.tolist()
y_equal = equal_df.Label.tolist()

X_equal_clean = remove_noise(X_equal)

equal_predicted = requ_clf.predict(X_equal_clean)
print(metrics.confusion_matrix(y_equal, equal_predicted))
print(metrics.classification_report(y_equal, equal_predicted, target_names=['Excessible', 'Not Excessible']))
