import subprocess
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
from heart_page import show_heart_page
from diabetis_page import show_diabetes_page
from parkinson_page import show_parkinson_page
from more_page import show_more_page
from database_page import show_database_page
from admin_page import show_adminn_page


print("launching app...please wait.")

subprocess.call('streamlit run app.py')