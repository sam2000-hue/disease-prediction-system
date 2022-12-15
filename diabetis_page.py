import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import numpy as np
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn import svm
import csv

from db_fxns import  get_name, view_unique_name, edit_patient_data, create_usertable, login_user

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

classifiers = data["model"]

def show_diabetes_page():
    st.title("Diabetes Prediction Service")

    st.write("""### We need some information to predict Patient's Diabetes status""")
    col1,col2,col3 = st.columns(3)
    col4,col5,col6 = st.columns(3)
    col7,col8 = st.columns(2)

    
    with col1:
        Pregnancies = st.number_input("Pregnancies", min_value=0, max_value=30, value=1, step=1)
    with col2:
        Glucose = st.number_input("Glucose", min_value=0, max_value=250, value=85, step=1)
    with col3:
        BloodPressure = st.number_input("Blood Pressure", min_value=0, max_value=150, value=66, step=1)
    with col4:
        SkinThickness = st.number_input("Skin Thickness", min_value=0, max_value=150, value=29, step=1)
    with col5:
        Insulin = st.number_input("Insulin Level", min_value=0, max_value=650, value=0, step=1)
    with col6:
        bmi = st.number_input("BMI value", min_value=0.0, max_value=50.0, value=26.6, step=0.1, format="%0f")
    with col7:
        DiabetesPedigreeFunction = st.number_input("Diabetes Pedigree Function", min_value=0.0000, max_value=5.0000, value=0.03, step=0.01 , format="%0f")
    with col8:
        Agee = st.number_input("Age", min_value=0, max_value=150, value=31, step=1)

    ok = st.button("Predict diabetes status")
    if ok:
        diabetes_dataset=pd.read_csv('diabetes.csv')

        X = diabetes_dataset.drop(columns= 'Outcome' , axis=1)
        Y = diabetes_dataset['Outcome']

        scaler= StandardScaler()

        scaler.fit(X)

        standardized_data=scaler.transform(X)

        X = standardized_data
        Y = diabetes_dataset['Outcome']

        X_train,X_test,Y_train,Y_test=train_test_split(X,Y, test_size=0.2, stratify=Y , random_state=2)

        classifier=svm.SVC(kernel='linear')

        classifier.fit(X_train,Y_train)

        X_train_prediction=classifier.predict(X_train)

        training_data_accuracy=accuracy_score(X_train_prediction,Y_train)

        X_test_prediction=classifier.predict(X_test)
        test_data_accuracy=accuracy_score(X_test_prediction,Y_test)

        input_data =(Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,bmi,DiabetesPedigreeFunction,Agee)

        input_data_as_numpy_array=np.asarray(input_data)
        #reshape the array as we are predicting for one instance

        input_data_reshaped=input_data_as_numpy_array.reshape(1,-1)
        
        std_data=scaler.transform(input_data_reshaped)

        prediction=classifiers.predict(std_data)

        if(prediction[0] ==0):
             predict_outcome=0
             st.subheader(f"The Patient is not Diabetic")
        else:
             predict_outcome=1
             st.subheader(f"The Patient is Diabetic")
        train_accuracy = training_data_accuracy*100
        st.subheader(f"The Accuracy Of The Model is : {train_accuracy:.2f} %")
        st.write("___________________________________________________________")
        with open ('newdiabetes.csv','a',newline='') as file:
            myFile = csv.writer(file)
            #myFile.writerow(["Pregnancies","Glucose","BloodPressure","SkinThickness","Insulin","BMI","DiabetesPedigreeFunction","Age","Outcome"])
            myFile.writerow([Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,bmi,DiabetesPedigreeFunction,Agee,predict_outcome])
   
    st.sidebar.info("You need to login to access professional features of this service")
    st.sidebar.write(" # Login Here #")
    username = st.sidebar.text_input("User Name")
    password = st.sidebar.text_input("Password" ,type="password")
    authstatus = "verified"
    if st.sidebar.checkbox("Login"):
        create_usertable()
        resultss = login_user(username,password,authstatus)
        #if password == "1234":
        if resultss:
            st.sidebar.success("Succesfully logged in as {}".format(username))
            st.subheader("Update Patient's Diabetes Status To Database")
            list_of_name = [i [0] for i in view_unique_name()]
            selected_name = st.selectbox("Patient's Detail To Edit",list_of_name)
            selected_result = get_name(selected_name)

            if selected_result:
                

                name = selected_result[0][0]
                id = selected_result[0][1]
                diabetis = selected_result[0][2]
                heart = selected_result[0][3]
                parkinsons = selected_result[0][4]
                Hospital = selected_result[0][5]
                date = selected_result[0][6]

                


                


                col20,col21 = st.columns(2)
                col22,col23,col24 = st.columns(3)
                col25,col26 = st.columns(2)

                
                with col20:
                    new_name = st.text_input("Patient's Full Name",name)
                with col21:
                    new_id = st.text_input("Patient's ID Number",id)
                with col22:
                    new_diabetis = st.selectbox("Diabetis Status" , ["Not Tested","Positive", "Negative"])
                with col23:
                    new_heart = st.selectbox("Heart Disease Status" , ["Not Tested","Positive", "Negative"])
                with col24:
                    new_parkinsons = st.selectbox("Parkinson's Disease  Status" , ["Not Tested","Positive", "Negative"])
                with col25:
                    new_Hospital = st.text_input("Hosipital Name",Hospital)
                with col26:
                    new_date = st.date_input("Date of last testing")


            add = st.button("Update Patient Diabetes Status")
            if add:
                edit_patient_data(new_name,new_id,new_diabetis,new_heart,new_parkinsons,new_Hospital,new_date,name,id,diabetis,heart,parkinsons,Hospital,date)
                st.success("sucessfully updated :: {}'s :: diabetis status  ".format(name))
        else:
            st.sidebar.warning("Incorrect Username/password combination")

        

       
    
    
