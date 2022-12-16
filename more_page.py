import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px 
from PIL import Image
import re
import csv
from db_fxns import create_usertable, add_userdata, edit_userpassword, edit_userprofile, login_user, view_user, edit_userprofile,edit_userpassword

image = Image.open('images/PROFILEPHOTO.png')

@st.cache
def load_data():
    diabetes_dataset=pd.read_csv('diabetes.csv')
    return diabetes_dataset
def load_data1():
    heart_dataset=pd.read_csv('heart.csv')
    return heart_dataset
def load_data2():
    parkinson_dataset=pd.read_csv('parkinsons.csv')
    return parkinson_dataset
def load_data3():
    review_dataset=pd.read_csv('review.csv')
    return review_dataset

         


def show_more_page():
    st.title("Explore Project Information And Profile Page")

    moree  = option_menu(
        menu_title="User Profile Or Project Documentation",
        options= ["My Profile","Project Documentation"],
        icons =["person-check","file-word"],
        menu_icon = "globe",
        default_index=0,
        orientation="horizontal",
        )






    if moree == "My Profile":
        st.subheader("Your Profile")
        st.info("You need to be logged in to view your profile.")

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

                    profile_data = view_user(username)
                    #st.write(profile_data)
                    #st.write(profile_data[0][0])

                    profile_user = profile_data[0][0]
                    profile_password = profile_data[0][1]
                    profile_email = profile_data[0][2]
                    profile_regno = profile_data[0][3]
                    profile_authstatus = profile_data[0][4]
                    col5,col6 = st.columns([1,3])
                    with col5:
                     
                        st.image(image, caption='User Profile')
                    with col6:

                        st.subheader(f"User Name : {profile_user} ")
                        st.subheader(f"Email Address : {profile_email} ")
                        st.subheader(f"Medical Regstration Number : {profile_regno} ")
                        st.subheader(f"Verification Status : {profile_authstatus}")
                    st.write("___________________________________________________________")
                    st.subheader("Edit Profile")

                    st.write("Update Profile Info")
                    col1,col2 = st.columns(2)
                    with col1:
                        update_user = st.text_input("Update Username",profile_user)
                    with col2:
                        update_email = st.text_input("Update Email",profile_email)
                    submit1 = st.button("Submit Changes")
                    if submit1:
                        edit_userprofile(update_user,update_email,profile_user,profile_email)
                        st.success("Profile Updated Successfully")
                    
                    st.write("Change Password")

                    col3,col4 = st.columns(2)
                    with col3:
                        oldpassword = st.text_input("Enter Existing Password",type="password")
                    with col4:
                        updated_password = st.text_input("Enter New Password",type="password")
                    submit2 = st.button("Change Password")


                    if submit2:
                        if oldpassword == profile_password:
                            edit_userpassword(updated_password,profile_password)

                            st.success("Password Changed Successfully")
                        else:
                            st.warning("Existing Passwords Did Not Match.Please Try Again.")
                    


                else:

                    st.sidebar.warning("Incorrect Username/password combination Or  Your Account Maybe Unverifed")

        elif auth == "Signup":           

            st.sidebar.write(" # SignUp Here #")
            new_username = st.sidebar.text_input("User Name")
            new_email = st.sidebar.text_input("Email Address")
            new_regnumber = st.sidebar.text_input("Regestration Number")
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
    elif moree == "Project Documentation":

        st.write(
            """
        ### more info on data used to train the models and project documentations
        """
        )
        if st.button("View Diabetes Model Data Analysis"):
            st.subheader("Dataset Used To Train And Test The Model")

            

            result = load_data()
            
            with st.expander("View all Data Used To Train And Test The Diabetes Model"):
                st.dataframe(result)

            st.subheader("The Distribution Of The Labelled Data On The Dataset")
            with st.expander("View The Distribution Of The Labelled Data"):
                diabetis_df= result['Outcome'].value_counts().to_frame()
                diabetis_df = diabetis_df.reset_index()
                st.dataframe(diabetis_df)
                p1 = px.pie(diabetis_df,names='index',values='Outcome')
                st.plotly_chart(p1,use_container_width=True)
            st.subheader("The Distribution Of The Labelled Data On The Dataset Based On Age")
            with st.expander("View The Distribution Of The Labelled Data Based on Age"):
                data = result.groupby(["Age"])["Outcome"].mean().sort_values(ascending=True)
                st.bar_chart(data)

            st.subheader("The Distribution Of The Labelled Data On The Dataset Based On Blood Pressure")
            with st.expander("View The Distribution Of The Labelled Data Based on Blood Pressure"):

                data = result.groupby(["BloodPressure"])["Outcome"].mean().sort_values(ascending=True)
                st.line_chart(data)

        if st.button("View heart Disease Model Data Analysis"):
            st.subheader("Dataset Used To Train And Test The Model")

            

            result = load_data1()
            
            with st.expander("View all Data Used To Train And Test The Diabetis Model"):
                st.dataframe(result)

            st.subheader("The Distribution Of The Labelled Data On The Dataset")
            with st.expander("View The Distribution Of The Labelled Data"):
                heart_df= result['target'].value_counts().to_frame()
                heart_df = heart_df.reset_index()
                st.dataframe(heart_df)
                p1 = px.pie(heart_df,names='index',values='target')
                st.plotly_chart(p1,use_container_width=True)

            st.subheader("The Distribution Of The Labelled Data On The Dataset Based On Chest Pain Type")
            with st.expander("View The Distribution Of The Labelled Data Based on Chest Pain Type"):
                data = result.groupby(["cp"])["target"].mean().sort_values(ascending=True)
                st.bar_chart(data)

            st.subheader("The Distribution Of The Labelled Data On The Dataset Based On Age")
            with st.expander("View The Distribution Of The Labelled Data Based on Age"):

                data = result.groupby(["age"])["target"].mean().sort_values(ascending=True)
                st.line_chart(data)

        if st.button("View Parkinson's Disease Model Data Analysis"):
            st.subheader("Dataset Used To Train And Test The Model")

            

            result = load_data2()
            
            with st.expander("View all Data Used To Train And Test The Diabetis Model"):
                st.dataframe(result)

            st.subheader("The Distribution Of The Labelled Data On The Dataset")
            with st.expander("View The Distribution Of The Labelled Data"):
                parkinson_df= result['status'].value_counts().to_frame()
                parkinson_df = parkinson_df.reset_index()
                st.dataframe(parkinson_df)
                p1 = px.pie(parkinson_df,names='index',values='status')
                st.plotly_chart(p1,use_container_width=True)
            st.subheader("The Distribution Of The Labelled Data On The Dataset Based On MDVP:Jitter(Abs)")
            with st.expander("View The Distribution Of The Labelled Data Based on MDVP:Jitter(Abs)"):
                data = result.groupby(["MDVP:Jitter(Abs)"])["status"].mean().sort_values(ascending=True)
                st.bar_chart(data)

            st.subheader("The Distribution Of The Labelled Data On The Dataset Based On MDVP:Jitter(%)")
            with st.expander("View The Distribution Of The Labelled Data Based on Blood MDVP:Jitter(%)"):

                data = result.groupby(["MDVP:Jitter(%)"])["status"].mean().sort_values(ascending=True)
        #         st.line_chart(data)
        # if st.button("View Project Documentation"):
        #     st.subheader("About This Project")
        #     with st.expander("View Project Documentation"):
        #         st.write("[About The Project](https://drive.google.com/file/d/1P_kkvymKL5_S5Xm-ygz08kwn4TOYxscP/view?usp=drivesdk)")
        #     st.subheader("Disclaimer")
        #     with st.expander("View Disclaimer Documentation"):
        #         st.write("[Project Disclaimer](https://www.freeprivacypolicy.com/live/5ba5a14d-9e54-45e6-aade-bfb867ac184d)")
        #     st.subheader("Terms And Conditions")
        #     with st.expander("View Terms And Conditions Documentation"):
        #         st.write("[Project Terms And Conditions](https://www.freeprivacypolicy.com/live/0aaca50f-3b71-45b1-8b46-8753f28c2a81)")
                

    st.write("___________________________________________________________")
    st.subheader("Review Section")
    st.write("Leave a review,comment,questions or concerns about the system to help us improve the quality of services offered")
    col1,col2 = st.columns(2)

    with col1:
        review_name=st.text_input("Full Name")
        review_email=st.text_input("Email")
    with col2:
        review_text=st.text_area("Write Review Here")
    review_button = st.button("Submit Review")

    if review_button:
        with open ('review.csv','a',newline='') as file:
            myFile = csv.writer(file)
            #myFile.writerow(["User name","User Email","Review"])
            myFile.writerow([review_name,review_email,review_text])
            st.success("Thank you {} ,Your Review Was Submitted Successfully ".format(review_name))
    st.write("___________________________________________________________")
    st.subheader("Reviews")

            

    result3 = load_data3()
    review_table = result3.drop(columns= 'User Email' , axis=1)
    review_table.index += 1
            
    with st.expander("View all Reviews"):
            st.dataframe(review_table)
        

    
