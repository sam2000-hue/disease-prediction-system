from itertools import count
from numpy import poly1d
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import re
# Data Viz Pkgs
import plotly
import plotly.express as px 
import plotly.graph_objs as go

from db_fxns import add_data, create_table, view_all_data, get_name, view_unique_name, edit_patient_data, delete_data, create_usertable, add_userdata, login_user, view_user




def show_database_page():
    st.title("Explore database page")

    st.info("You need to be logged in as qualified medical personnel to access database services.")
    with st.sidebar:
        auth = option_menu(
            menu_title=None,
            options= [ "Login","Signup","Logout"] ,
            icons =["person-check","person-plus","person-x"],
            menu_icon = "cast",
            default_index=0,
            
            )
    


    
    
    if auth == "Login":
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
            

                st.write(
                    """
                ### View And Modify Patients' Database
                """
                )
                choice = option_menu(
                    menu_title="Database Menu",
                    options= ["Add New Patient Details","View All Patients Details","Update Patient Details","Delete Patient Details"] ,
                    icons =["folder-plus","folder2-open","folder-symlink","folder-x"],
                    menu_icon = "hdd-stack-fill",
                    default_index=0,
                    orientation="horizontal",
                    )

                

               
                
                create_table()

                if choice == "Add New Patient Details":
                    st.subheader("Add Patient Details")
                    col1,col2 = st.columns(2)
                    col3,col4,col5 = st.columns(3)
                    col6,col7,col8 = st.columns(3)

                    with col1:
                        name = st.text_input("Patient's Full Name")
                    with col2:
                        id = st.text_input("Patient's ID Number")
                    with col3:
                        diabetis = st.selectbox("Diabetis Status" , ("Not Tested","Positive", "Negative"))
                    with col4:
                        heart = st.selectbox("Heart Disease Status" , ("Not Tested","Positive", "Negative"))
                    with col5:
                        parkinsons = st.selectbox("Parkinson's Disease  Status" , ("Not Tested","Positive", "Negative"))
                    with col6:
                        Hospital = st.text_input("Hosipital Name")
                    with col8:
                        date = st.date_input("Date of last testing")
                    with col7:
                        county = st.selectbox("Patient's County" ,("Mombasa","Kwale","Kilifi","Tana River","Lamu","Taita/Taveta","Garissa","Wajir",
                        "Mandera","Marsabit","Isiolo","Meru","Tharaka-Nithi","Embu","Kitui", "Machakos", "Makueni","Nyandarua","Nyeri","Kirinyaga",
                        "Murang'a","Kiambu","Turkana","West Pokot","Samburu","Trans Nzoia","Uasin Gishu","Elgeyo/Marakwet","Nandi","Baringo","Laikipia",
                        "Nakuru","Narok","Kajiado","Kericho","Bomet","Kakamega","Vihiga","Bungoma","Busia","Siaya","Kisumu","Homa Bay","Migori","Kisii","Nyamira","Nairobi City"))
                      

                    add = st.button("Add Patient to database")
                    if add:
                        add_data(name,id,diabetis,heart,parkinsons,Hospital,date,county)
                        st.success("sucessfully added :: {} :: to database".format(name))
                elif choice == "View All Patients Details":
                    st.subheader("View Database")
                    result = view_all_data()
                    #st.write(result)
                    df = pd.DataFrame(result,columns=['Name of patient','ID Number.','Diabetis Status','Heart Status','Parkinsons Status','Hospital Name','Date of checking','Patients County'])
                    df.index += 1
                    with st.expander("View all Data"):
                        st.dataframe(df)
                    with st.expander("Diabetis Distribution  Summary"):
                        diabetis_df= df['Diabetis Status'].value_counts().to_frame()
                        diabetis_df = diabetis_df.reset_index()
                        st.dataframe(diabetis_df)
                        p1 = px.pie(diabetis_df,names='index',values='Diabetis Status')
                        st.plotly_chart(p1,use_container_width=True)

                        

                    with st.expander("heart Disease Distribution  Summary"):
                        heart_df= df['Heart Status'].value_counts().to_frame()
                        heart_df = heart_df.reset_index()
                        st.dataframe(heart_df)
                        p1 = px.pie(heart_df,names='index',values='Heart Status')
                        st.plotly_chart(p1,use_container_width=True)
                    with st.expander("Parkinson's Disease Distribution  Summary"):
                        parkinson_df= df['Parkinsons Status'].value_counts().to_frame()
                        parkinson_df = parkinson_df.reset_index()
                        st.dataframe(parkinson_df)
                        p1 = px.pie(parkinson_df,names='index',values='Parkinsons Status')
                        
                        st.plotly_chart(p1,use_container_width=True)

                    with st.expander("Diabetes Disease Distribution Graph By County In Kenya "):
                        county= df['Patients County']
                        countysort = st.selectbox("Please Select County" ,("Mombasa","Kwale","Kilifi","Tana River","Lamu","Taita/Taveta","Garissa","Wajir",
                        "Mandera","Marsabit","Isiolo","Meru","Tharaka-Nithi","Embu","Kitui", "Machakos", "Makueni","Nyandarua","Nyeri","Kirinyaga",
                        "Murang'a","Kiambu","Turkana","West Pokot","Samburu","Trans Nzoia","Uasin Gishu","Elgeyo/Marakwet","Nandi","Baringo","Laikipia",
                        "Nakuru","Narok","Kajiado","Kericho","Bomet","Kakamega","Vihiga","Bungoma","Busia","Siaya","Kisumu","Homa Bay","Migori","Kisii","Nyamira","Nairobi City"))
                      
                       
                        pos_responses = df[df['Diabetis Status'] == 'Positive'][df['Patients County'] == countysort]['Diabetis Status'].value_counts()
                        neg_responses = df[df['Diabetis Status'] == 'Negative'][df['Patients County'] == countysort]['Diabetis Status'].value_counts()
                        non_responses = df[df['Diabetis Status'] == 'Not Tested'][df['Patients County'] == countysort]['Diabetis Status'].value_counts()
                        
                        date =df['Date of checking']

                        trace1 = go.Bar(
                            x=pos_responses.index,
                            y=pos_responses.values,
                            name='Positive'
                        )
                        trace2 = go.Bar(
                            x=neg_responses.index,
                            y=neg_responses.values,
                            name='Negative'
                        )
                        trace3 = go.Bar(
                            x=non_responses.index,
                            y=non_responses.values,
                            name='Not Tested'
                        )

                        data = [trace1, trace2 ,trace3]
                        layout = go.Layout(
                            barmode='stack'
                        )

                    
                        fig = go.Figure(data=data, layout=layout)

                        st.plotly_chart(fig,use_container_width=True)
                    
                    with st.expander("Heart Disease Distribution Graph By County In Kenya "):
                        county= df['Patients County']
                        countysort = st.selectbox("Select County" ,("Mombasa","Kwale","Kilifi","Tana River","Lamu","Taita/Taveta","Garissa","Wajir",
                        "Mandera","Marsabit","Isiolo","Meru","Tharaka-Nithi","Embu","Kitui", "Machakos", "Makueni","Nyandarua","Nyeri","Kirinyaga",
                        "Murang'a","Kiambu","Turkana","West Pokot","Samburu","Trans Nzoia","Uasin Gishu","Elgeyo/Marakwet","Nandi","Baringo","Laikipia",
                        "Nakuru","Narok","Kajiado","Kericho","Bomet","Kakamega","Vihiga","Bungoma","Busia","Siaya","Kisumu","Homa Bay","Migori","Kisii","Nyamira","Nairobi City"))
                      
                       
                        pos_responses = df[df['Heart Status'] == 'Positive'][df['Patients County'] == countysort]['Heart Status'].value_counts()
                        neg_responses = df[df['Heart Status'] == 'Negative'][df['Patients County'] == countysort]['Heart Status'].value_counts()
                        non_responses = df[df['Heart Status'] == 'Not Tested'][df['Patients County'] == countysort]['Heart Status'].value_counts()
                        
                        date =df['Date of checking']

                        trace1 = go.Bar(
                            x=pos_responses.index,
                            y=pos_responses.values,
                            name='Positive'
                        )
                        trace2 = go.Bar(
                            x=neg_responses.index,
                            y=neg_responses.values,
                            name='Negative'
                        )
                        trace3 = go.Bar(
                            x=non_responses.index,
                            y=non_responses.values,
                            name='Not Tested'
                        )

                        data = [trace1, trace2 ,trace3]
                        layout = go.Layout(
                            barmode='stack'
                        )

                    
                        fig = go.Figure(data=data, layout=layout)

                        st.plotly_chart(fig,use_container_width=True)
                        
                    with st.expander("Parkinson's Disease Distribution Graph By County In Kenya "):
                        county= df['Patients County']
                        countysort = st.selectbox("Select County here" ,("Mombasa","Kwale","Kilifi","Tana River","Lamu","Taita/Taveta","Garissa","Wajir",
                        "Mandera","Marsabit","Isiolo","Meru","Tharaka-Nithi","Embu","Kitui", "Machakos", "Makueni","Nyandarua","Nyeri","Kirinyaga",
                        "Murang'a","Kiambu","Turkana","West Pokot","Samburu","Trans Nzoia","Uasin Gishu","Elgeyo/Marakwet","Nandi","Baringo","Laikipia",
                        "Nakuru","Narok","Kajiado","Kericho","Bomet","Kakamega","Vihiga","Bungoma","Busia","Siaya","Kisumu","Homa Bay","Migori","Kisii","Nyamira","Nairobi City"))
                      
                       
                        pos_responses = df[df['Parkinsons Status'] == 'Positive'][df['Patients County'] == countysort]['Parkinsons Status'].value_counts()
                        neg_responses = df[df['Parkinsons Status'] == 'Negative'][df['Patients County'] == countysort]['Parkinsons Status'].value_counts()
                        non_responses = df[df['Parkinsons Status'] == 'Not Tested'][df['Patients County'] == countysort]['Parkinsons Status'].value_counts()
                        
                        date =df['Date of checking']

                        trace1 = go.Bar(
                            x=pos_responses.index,
                            y=pos_responses.values,
                            name='Positive'
                        )
                        trace2 = go.Bar(
                            x=neg_responses.index,
                            y=neg_responses.values,
                            name='Negative'
                        )
                        trace3 = go.Bar(
                            x=non_responses.index,
                            y=non_responses.values,
                            name='Not Tested'
                        )

                        data = [trace1, trace2 ,trace3]
                        layout = go.Layout(
                            barmode='stack'
                        )

                    
                        fig = go.Figure(data=data, layout=layout)

                        st.plotly_chart(fig,use_container_width=True)


                elif choice == "Update Patient Details":
                    st.subheader("Edit / Update Patient Details")
                    with st.expander("View Patient Current Data"):
                        result = view_all_data()
                        df = pd.DataFrame(result,columns=['Name of patient','ID Number.','Diabetis Status','Heart Status','Parkinsons Status','Hospital Name','Date of checking','Patients county'])
                        df.index += 1
                        st.dataframe(df)

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

                        col1,col2 = st.columns(2)
                        col3,col4,col5 = st.columns(3)
                        col6,col7 = st.columns(2)

                        
                        with col1:
                            new_name = st.text_input("Patient's Full Name",name)
                        with col2:
                            new_id = st.text_input("Patient's ID Number",id)
                        with col3:
                            new_diabetis = st.selectbox("Diabetis Status" , ["Not Tested","Positive", "Negative"])
                        with col4:
                            new_heart = st.selectbox("Heart Disease Status" , ["Not Tested","Positive", "Negative"])
                        with col5:
                            new_parkinsons = st.selectbox("Parkinson's Disease  Status" , ["Not Tested","Positive", "Negative"])
                        with col6:
                            new_Hospital = st.text_input("Hosipital Name",Hospital)
                        with col7:
                            new_date = st.date_input("Date of last testing")
                        
                    add = st.button("Update Patient details")
                    if add:
                        edit_patient_data(new_name,new_id,new_diabetis,new_heart,new_parkinsons,new_Hospital,new_date,name,id,diabetis,heart,parkinsons,Hospital,date)
                        st.success("sucessfully updated :: {} :: details to :: {} ".format(name,new_name))
                
                    with st.expander("View Patient Updated Data"):
                        result2 = view_all_data()
                        df2 = pd.DataFrame(result2,columns=['Name of patient','ID Number.','Diabetis Status','Heart Status','Parkinsons Status','Hospital Name','Date of checking','Patients county'])
                        df2.index += 1
                        st.dataframe(df2)
                elif choice == "Delete Patient Details":
                    st.subheader("Delete Patient Details")
                    with st.expander("View Patient's Current Data"):
                        result = view_all_data()
                        df = pd.DataFrame(result,columns=['Name of patient','ID Number.','Diabetis Status','Heart Status','Parkinsons Status','Hospital Name','Date of checking','Patients county'])
                        df.index += 1
                        st.dataframe(df)

                    list_of_name = [i [0] for i in view_unique_name()]
                    selected_name = st.selectbox("Patient's Detail To Delete",list_of_name)
                    st.warning("Do You Want To Delete Patient :: {}  Details?".format(selected_name))
                    if st.button("Delete Patient's Details"):
                        delete_data(selected_name)
                        st.success("Patient Details Successfully deleted")
                    with st.expander("View Patient Updated Data"):
                        result3 = view_all_data()
                        df2 = pd.DataFrame(result3,columns=['Name of patient','ID Number.','Diabetis Status','Heart Status','Parkinsons Status','Hospital Name','Date of checking','Patients county'])
                        df2.index += 1
                        st.dataframe(df2)
            else:

                st.sidebar.warning("Incorrect Username/Password Combination Or Your Account Maybe Unverifed")    

 
    elif auth == "Signup":
        st.sidebar.write(" # SignUp Here #")
        new_username = st.sidebar.text_input("User Name")
        new_email = st.sidebar.text_input("Email Address")
        new_regnumber = st.sidebar.text_input("Registration Number")
        confirm_password = st.sidebar.text_input("Password" ,type="password")
        new_password = st.sidebar.text_input("Confirm Password" ,type="password")
        new_authstatus = "Pending"

        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

        vals = view_user(new_username)

        if st.sidebar.checkbox("SignUp"):

            if vals:
                st.sidebar.warning("This user is already regestered!")
                st.sidebar.info("If you are already verified by administrator please proceed to login")
            else:
                if re.fullmatch(regex, new_email):
                    if confirm_password == new_password:
                        create_usertable()
                        add_userdata(new_username,new_password,new_email,new_regnumber,new_authstatus)
                        st.sidebar.success("Successfully Signed Up")
                        st.sidebar.info("You Will Be notified Once Your Account Is Verified To Access Other Features Of The App")
                    else:
                        st.sidebar.warning("SignUp Unsuccessful!")
                        st.sidebar.info("Make sure the passwords entered match each other")
                else:
                    st.sidebar.warning("Invalid email format, Please check your eamil and try again")

       
           


    elif auth == "Logout":
        st.sidebar.info("Successfully Logged out")
        st.write("You are currently logged out")