## import packages for this
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas_datareader as pdr # helps to pull the yahoo finance data
from sklearn.preprocessing import StandardScaler # helps to scale the data
from sklearn import metrics # helps to evaluate the model
from sklearn.naive_bayes import GaussianNB # helps to build the model
from sklearn.linear_model import LogisticRegression # helps to build the model
from sklearn.preprocessing import MinMaxScaler

test = pd.read_csv('Data/test_titanic.csv')
train = pd.read_csv('Data/train_titanic.csv')

train['family']= train['SibSp'] + train['Parch']
test['family']= test['SibSp'] + test['Parch']
train['Alone'] = np.where(train['family']==0,1,0)
test['Alone'] = np.where(test['family']==0,1,0)
train['No_cabin'] = np.where(train['Cabin'].isna(),1,0)
test['No_cabin'] = np.where(test['Cabin'].isna(),1,0)
train['Gender'] = np.where(train['Sex']=="male",1,0)
test['Gender'] = np.where(test['Sex']=="male",1,0)
# filling gaps of age and fare with median
train[['Age', 'Fare']] = train[['Age', 'Fare']].fillna(train[['Age', 'Fare']].median())
test[['Age', 'Fare']] = test[['Age', 'Fare']].fillna(test[['Age', 'Fare']].median())
#test = test.dropna(axis=0, subset=['Age'])
#train = train.dropna(axis=0, subset=['Age'])

del train['SibSp']
del train['Parch']
del test['SibSp']
del test['Parch']
del test['family']
del train['family']
del train['PassengerId']
del test['PassengerId']
del train['Name']
del test['Name']

train['Age_Cat']=pd.cut(train.Age,bins=[0,2,17,65,99],labels=['Toddler/Baby','Child','Adult','Elderly'])
test['Age_Cat']=pd.cut(test.Age,bins=[0,2,17,65,99],labels=['Toddler/Baby','Child','Adult','Elderly'])

train['Age_Cat_num'] = train['Age_Cat'].replace(['Toddler/Baby','Child','Adult','Elderly'],
                        [1,2,3,4], inplace=False)

test['Age_Cat_num'] = test['Age_Cat'].replace(['Toddler/Baby','Child','Adult','Elderly'],
                        [1,2,3,4], inplace=False)

del train['Ticket']
del test['Ticket']
del train['Cabin']
del test['Cabin']
del train['Sex']
del test['Sex']
del train['Embarked']
del test['Embarked']

train['Age_Cat_num']=pd.to_numeric(train['Age_Cat_num'])
test['Age_Cat_num']=pd.to_numeric(test['Age_Cat_num'])

## headings for our data application
st.title('Who survived the titanic?')
#st.sidebar.header('Passenger data')
st.subheader('Statistical picture of the data')
st.write (train.describe())

## Setting my dependent and independent variable
X_train = train.iloc[:,1:7].values # selection of variables based on previous analysis
Y_train = train.iloc[:, 0].values # survival is outcome

X_test = test.iloc[:,0:6].values # selection of variables based on previous analysis



scaler_X = StandardScaler()
X_train = scaler_X.fit_transform(X_train) # Scaling  training set
X_test = scaler_X.transform(X_test) # Scaling test set

logisticRegression_model = LogisticRegression(random_state=0) # Logistic Regression model
logisticRegression_model.fit(X_train, Y_train) # Training the model

prediction = logisticRegression_model.predict(X_test) # Predict the response


import statsmodels.api as sm

#log_clf = LogisticRegression()

log_clf =sm.Logit(train.iloc[:,0],train.iloc[:,1:7])

classifier = log_clf.fit()

y_pred = classifier.predict(X_test)

print(classifier.summary2())

## Output
st.subheader('Logistic regression on survival of the titanic')

st.write(classifier.summary().as_html(), unsafe_allow_html=True)

# to run type: streamlit run logregressionapp.py