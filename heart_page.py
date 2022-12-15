import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import csv
from db_fxns import  get_name, view_unique_name, edit_patient_data, create_usertable, login_user

def load_model():
    with open('saved_heart.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

classifiers = data["model"]

def show_heart_page():
    st.title("Heart Disease Prediction Service")

    st.write("""### We need some information to predict Patient's Heart Disease status""")
    col1,col2,col3 = st.columns(3)
    col4,col5,col6 = st.columns(3)
    col7,col8,col9 = st.columns(3)
    col10,col11,col12 = st.columns(3)
    col13,col14,col15 = st.columns(3)
   
    with col1:
        age = st.number_input("Age of patient", min_value=0, max_value=150, value=10, step=1)
    with col2:    
        gender = st.selectbox("Sex of patient" , ("Female","Male"))

        sex = 0 if gender == "Female" else 1
    with col3:
        cpselect = st.selectbox("Chest pain type" , ("Type 0","Type 1", "Type 2","Type 3"))
    
        ChestPain = 0 if cpselect == "Type 0" else 1 if cpselect == "Type 1"  else 2 if cpselect == "Type 2" else 3
    with col4:
        Restbp = st.number_input("Resting blood pressure (in mm Hg on admission to the hospital)", min_value=50, max_value=250, value=100, step=1)
    with col5:    
        chol = st.number_input("serum cholestoral in mg/dl", min_value=100, max_value=700, value=100, step=1)
    with col6:    
        fbsselect = st.selectbox("Fasting blood sugar & gt; 120 mg/dl", ("True","False"))

        fbs = 1 if fbsselect == "True" else 0
    with col7:
        electrocardiographic = st.number_input("resting electrocardiographic results", min_value=0.0, max_value=2.0, value=0.0, step=1.0 , format="%0f")
    with col8:
        heartrate = st.number_input("maximum heart rate achieved", min_value=0, max_value=300, value=0, step=1)
    with col9:
        anginaselect =st.selectbox("exercise induced angina",("Yes","No"))

        angina = 1 if anginaselect == "Yes" else 0
    with col10:
        oldpeak = st.number_input("ST depression induced by exercise relative to rest", min_value=0.0, max_value=10.0, value=1.0, step=0.1,format="%0f")
    with col11:
        slope = st.number_input("the slope of the peak exercise ST segment", min_value=0, max_value=2, value=0, step=1)
    with col12:
        ca = st.number_input("number of major vessels (0-3) colored by flourosopy", min_value=0, max_value=3, value=0, step=1)
    with col13:
        thal = st.number_input("thal: 3 = normal; 6 = fixed defect; 7 = reversable defect", min_value=0, max_value=8, value=0, step=1)
    st.write('<style>div.row-widget.stSelectbox>div{flex-direction:row;}</style>', unsafe_allow_html=True)

    ok = st.button("Predict heart disease status")
    if ok:
        # loading the csv data to a Pandas DataFrame
        heart_data = pd.read_csv('heart.csv')

        X = heart_data.drop(columns='target', axis=1)
        Y = heart_data['target']

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)

        model = LogisticRegression()

        # training the LogisticRegression model with Training data
        model.fit(X_train, Y_train)

        # accuracy on training data
        X_train_prediction = model.predict(X_train)
        training_data_accuracy = accuracy_score(X_train_prediction, Y_train)

        # accuracy on test data
        X_test_prediction = model.predict(X_test)
        test_data_accuracy = accuracy_score(X_test_prediction, Y_test)

        input_data = (age,sex,ChestPain,Restbp,chol,fbs,electrocardiographic,heartrate,angina,oldpeak,slope,ca,thal)

        # change the input data to a numpy array
        input_data_as_numpy_array= np.asarray(input_data)

        # reshape the numpy array as we are predicting for only on instance
        input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

        prediction = model.predict(input_data_reshaped)
        print(prediction)

        if(prediction[0] ==0):
             predict_target=0
             st.subheader(f"The Patient does not have a Heart Disease")
        else:
             predict_target=1
             st.subheader(f"The Patient has Heart Disease")
        train_accuracy = training_data_accuracy*100
        st.subheader(f"The Accuracy Of The Model is : {train_accuracy:.2f} %")
        st.write("___________________________________________________________")
        with open ('newheart.csv','a',newline='') as file:
            myFile = csv.writer(file)
            #myFile.writerow(["age","sex","cp","trestbps","chol","fbs","thalach","exang","oldpeak","slope","ca","thal","target"])
            myFile.writerow([age,sex,ChestPain,Restbp,chol,fbs,electrocardiographic,heartrate,angina,oldpeak,slope,ca,thal,predict_target])
    
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
            st.subheader("Update Patient's Heart Disease Status To Database")
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


            add = st.button("Update Patient Heart Disease Status")
            if add:
                edit_patient_data(new_name,new_id,new_diabetis,new_heart,new_parkinsons,new_Hospital,new_date,name,id,diabetis,heart,parkinsons,Hospital,date)
                st.success("sucessfully updated :: {}'s :: Heart Disease status  ".format(name)) 
        else:
            st.sidebar.warning("Incorrect Username/password combination")

        

       
    
    
