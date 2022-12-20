## import packages for this
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('Data/diabetes.csv')

## headings for our data application
st.title('Diabetes check data application')
st.sidebar.header('Patient data')
st.subheader('Statistical picture of the data')
st.write (df.describe())

## Setting my dependent and independent variable
X = df.iloc[:, 0:8]
Y = df.iloc[:,-1]

## Data splitting
X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size=0.20, random_state=0)

#Function that accepts users input
def user_report():
    pregnancies = st.sidebar.slider('Pregnancies',0,17,4)# 0 is the bottom, 17 is the max value and 4 is the mean
    glucose = st.sidebar.slider('Glucose', 0,200, 120) # again min, max mean
    bp = st.sidebar.slider('BloodPressure', 0,122,70)
    skinthickness = st.sidebar.slider('Skinthickness', 0,100,20)
    insulin = st.sidebar.slider('Insulin', 0,846,80)
    bmi = st.sidebar.slider('BMI',0,67,21)
    dbf = st.sidebar.slider('DiabetesPedigreeFunction',0.0,2.4,0.47)
    age = st.sidebar.slider('Age',21,88,33)
    user_report_data = {
        'Pregnancies':pregnancies,
        'Glucose':glucose,
        'BloodPressure':bp,
        'SkinThickness':skinthickness,
        'Insulin':insulin,
        'BMI':bmi,
        'DiabetesPedigreeFunction':dbf,
        'Age':age
    } # so when people set their chosen value it gets saved into a dataframe
    report_data = pd.DataFrame(user_report_data,index = [0])# specifed the column
    return report_data

# Patient Data
user_data = user_report()
st.header('Patient data')
st.write(user_data)

# Model training/fitting
rf = RandomForestClassifier()
rf.fit(X_train,y_train)

user_result = rf.predict(user_data)

## Output
st.subheader('Your Diabetes Report: ')
output = ''
if user_result[0]==0: # this is if not diabetic
    output = 'You are not diabetic'
else:
    output = 'You are diabetic'
st.title(output)
st.subheader('Accuracy: ')
st.write(str(accuracy_score(y_test, rf.predict(X_test))*100)+"percent")