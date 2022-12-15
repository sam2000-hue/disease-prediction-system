import streamlit as st
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn.metrics import accuracy_score
import csv

from db_fxns import  get_name, view_unique_name, edit_patient_data, create_usertable ,login_user

def load_model():
    with open('saved_park.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

classifiers = data["model"]

def show_parkinson_page():
    st.title("Parkinson's disease Prediction Service")

    st.write("""### We need some information to predict Patient's Parkinson's disease status""")
   
   


    st.write("""### Several measures of variation in fundamental frequency""")

    col1,col2,col3 = st.columns(3)
    col4,col5,col6 = st.columns(3)
    col7,col8,col9 = st.columns(3)
    with col1:
        MDVPFoHz = st.number_input("MDVP:Fo(Hz) - Average vocal fundamental frequency", min_value=50.0, max_value=300.0, value=100.1, step=1.0, format="%0f")
    with col2:
        MDVPFhiHz = st.number_input("MDVP:Fhi(Hz) - Maximum vocal fundamental frequency", min_value=100.0, max_value=600.0, value=100.1, step=1.0, format="%0f")
    with col3:
        MDVPFloHz = st.number_input("MDVP:Flo(Hz) - Minimum vocal fundamental frequency", min_value=60.0, max_value=250.0, value=100.1, step=1.0, format="%0f")
    with col4:
        MDVPJitterPercent = st.number_input("MDVP:Jitter(%)", value=0.1, step=1.0, format="%0f")
    with col5:
        MDVPJitterAbs = st.number_input("MDVP:Jitter(Abs)",  max_value=1.0, value=0.1, step=0.1, format="%0f")
    with col6:
        MDVPRAP = st.number_input("MDVP:RAP",  max_value=1.0, value=0.1, step=0.1, format="%0f")
    with col7:
        MDVPPPQ = st.number_input("MDVP:PPQ",  max_value=1.0, value=0.1, step=0.1 , format="%0f")
    with col8:
        st.write(".")
    with col9:
        st.write(".")
    
    

    st.write("""### Several measures of variation in amplitude""")

    col10,col11,col12 = st.columns(3)
    col13,col14,col15 = st.columns(3)
    col16,col17,col18 = st.columns(3)
    with col10:
        JitterDDP = st.number_input("Jitter:DDP",  max_value=1.0, value=0.1, step=1.0, format="%0f")
    with col11:
        MDVPShimmer = st.number_input("MDVP:Shimmer", max_value=1.0, value=0.1, step=0.1, format="%0f")
    with col12:
        MDVPShimmerdB = st.number_input("MDVP:Shimmer(dB)", max_value=2.0, value=1.0, step=0.1, format="%0f")
    with col13:
        ShimmerAPQ3 = st.number_input("Shimmer:APQ3", max_value=1.0, value=0.1, step=0.1, format="%0f")
    with col14:
        ShimmerAPQ5 = st.number_input("Shimmer:APQ5", max_value=1.0, value=0.1, step=0.1, format="%0f")
    with col15:
        MDVPAPQ = st.number_input("MDVP:APQ", max_value=1.0, value=0.1, step=0.1, format="%0f")
    with col16:
        ShimmerDDA = st.number_input("Shimmer:DDA", max_value=1.0, value=0.1, step=0.1, format="%0f")
    with col17:
        st.write(".")
    with col18:
        st.write(".")

    st.write("""### Two measures of ratio of noise to tonal components in the voice""")
    col19,col20 = st.columns(2)
    with col19:

        NHR = st.number_input("NHR",  max_value=1.0, value=0.1, step=0.1, format="%0f")
    with col20:
        HNR = st.number_input("HNR", max_value=40.0, value=10.1, step=0.1, format="%0f")

    st.write("""### Two nonlinear dynamical complexity measures""")
    col21,col22 = st.columns(2)
    with col21:
        RPDE = st.number_input("RPDE", max_value=1.0, value=0.1, step=0.1, format="%0f")
    with col22:
        D2 = st.number_input("D2",min_value=0.0, max_value=1.0, value=0.1, step=0.1, format="%0f")

    st.write("""### Signal fractal scaling exponent""")

    DFA = st.number_input("DFA",  max_value=1.0, value=0.1, step=0.1, format="%0f")

    st.write("""### Three nonlinear measures of fundamental frequency variation""")
    col23,col24,col25 = st.columns(3)
    with col23:
        spread1 = st.number_input("spread1",  max_value=1.0, value=0.1, step=0.1, format="%0f")
    with col24:
        spread2 = st.number_input("spread2", max_value=5.0, value=0.1, step=0.1, format="%0f")
    with col25:
        PPE = st.number_input("PPE", max_value=1.0, value=0.1, step=0.1 , format="%0f")






    ok = st.button("Predict parkinson's status")
    if ok:
        # loading the data from csv file to a Pandas DataFrame
        parkinsons_data = pd.read_csv('parkinsons.csv')

        X = parkinsons_data.drop(columns=['name','status'], axis=1)
        Y = parkinsons_data['status']

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)

        scaler = StandardScaler()

        scaler.fit(X_train)

        X_train = scaler.transform(X_train)

        X_test = scaler.transform(X_test)

        model = svm.SVC(kernel='linear')

        # training the SVM model with training data
        model.fit(X_train, Y_train)

        X_train_prediction = model.predict(X_train)
        training_data_accuracy = accuracy_score(Y_train, X_train_prediction)

       
        # accuracy score on training data
        X_test_prediction = model.predict(X_test)
        test_data_accuracy = accuracy_score(Y_test, X_test_prediction)

        input_data = (MDVPFoHz,MDVPFhiHz, MDVPFloHz,MDVPJitterPercent,MDVPJitterAbs,MDVPRAP,MDVPPPQ,JitterDDP,MDVPShimmer,MDVPShimmerdB,ShimmerAPQ3,ShimmerAPQ5,MDVPAPQ,ShimmerDDA,NHR,HNR,RPDE,D2,DFA,spread1,spread2,PPE)

        # changing input data to a numpy array
        input_data_as_numpy_array = np.asarray(input_data)

        # reshape the numpy array
        input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

        # standardize the data
        std_data = scaler.transform(input_data_reshaped)

        prediction = model.predict(std_data)
        print(prediction)
        if(prediction[0] ==0):
             st.subheader(f"The Patient does not have Parkinson's Disease")
             predict_target=0
        else:
             st.subheader(f"The Patient has Parkinson's Disease")
             predict_target=1
        train_accuracy = training_data_accuracy*100
        st.subheader(f"The Accuracy Of The Model is : {train_accuracy:.2f} %")
        st.write("___________________________________________________________")
        with open ('newparkinson.csv','a',newline='') as file:
            myFile = csv.writer(file)
            #myFile.writerow(["MDVP:Fo(Hz)","MDVP:Fhi(Hz)","MDVP:Flo(Hz)","MDVP:Jitter(%)","MDVP:Jitter(Abs)","MDVP:RAP","MDVP:PPQ","Jitter:DDP","MDVP:Shimmer","MDVP:Shimmer(dB)","Shimmer:APQ3","Shimmer:APQ5","MDVP:APQ","Shimmer:DDA","NHR","HNR","status","RPDE","D2","DFA","spread1","spread2","PPE"])
            myFile.writerow([MDVPFoHz,MDVPFhiHz, MDVPFloHz,MDVPJitterPercent,MDVPJitterAbs,MDVPRAP,MDVPPPQ,JitterDDP,MDVPShimmer,MDVPShimmerdB,ShimmerAPQ3,ShimmerAPQ5,MDVPAPQ,ShimmerDDA,NHR,HNR,predict_target,RPDE,D2,DFA,spread1,spread2,PPE])
    
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
            st.subheader("Update Patient's Parkinson's Status To Database")
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


                col27,col28 = st.columns(2)
                col29,col30,col31 = st.columns(3)
                col32,col33 = st.columns(2)

                
                with col27:
                    new_name = st.text_input("Patient's Full Name",name)
                with col28:
                    new_id = st.text_input("Patient's ID Number",id)
                with col29:
                    new_diabetis = st.selectbox("Diabetis Status" , ["Not Tested","Positive", "Negative"])
                with col30:
                    new_heart = st.selectbox("Heart Disease Status" , ["Not Tested","Positive", "Negative"])
                with col31:
                    new_parkinsons = st.selectbox("Parkinson's Disease  Status" , ["Not Tested","Positive", "Negative"])
                with col32:
                    new_Hospital = st.text_input("Hosipital Name",Hospital)
                with col33:
                    new_date = st.date_input("Date of last testing")


            add = st.button("Update Patient Parkinson's Disease Status")
            if add:
                edit_patient_data(new_name,new_id,new_diabetis,new_heart,new_parkinsons,new_Hospital,new_date,name,id,diabetis,heart,parkinsons,Hospital,date)
                st.sidebar.success("sucessfully updated :: {}'s :: Parkinson's Disease status  ".format(name))
        else:
            st.sidebar.warning("Incorrect Username/password combination")

        

       
    
    
