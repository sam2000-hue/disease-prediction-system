import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
from heart_page import show_heart_page
from diabetis_page import show_diabetes_page
from parkinson_page import show_parkinson_page
from more_page import show_more_page
from database_page import show_database_page
from admin_page import show_adminn_page



img = Image.open('images/Main.png')
hide_menu_style = """
        <style>
        #MainMenu {visibility: show; }
        footer {visibility: hidden; }
        </style>

"""
st.set_page_config(page_title='Disease Prediction System', page_icon=img)
#st.set_page_config(page_title='Disease Prediction System', page_icon=":shark:")
st.markdown(hide_menu_style, unsafe_allow_html=True)

page = option_menu(
    menu_title=None,
    options= [ "Database Page", "Diabetes Prediction", "Heart Disease Prediction", "Parkinsons Disease Prediction", "Administrator Page" ,"Project Information And Profile"] ,
    icons =["device-ssd","activity","heart","ear","person-check","file-bar-graph"],
    menu_icon = "cast",
    default_index=1,
    orientation="horizontal",
    )




#page = st.sidebar.selectbox("Main Menu", ( "Home", "Diabetes", "Heart", "Parkinson", "Admin" ,"More"))

if page == "Heart Disease Prediction":
    show_heart_page()
elif page  == "Diabetes Prediction":
    show_diabetes_page()
elif page  == "Parkinsons Disease Prediction":
    show_parkinson_page()
elif page  == "Database Page":
    show_database_page()

elif page  == "Administrator Page":
    show_adminn_page()
elif page == "Project Information And Profile":

    show_more_page()