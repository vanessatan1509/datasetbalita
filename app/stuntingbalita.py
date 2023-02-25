#Library
import numpy as np
import streamlit as st
import pandas as pd

from streamlit_option_menu import option_menu

#Side Bar
with st.sidebar :
    nav_bar = option_menu(
        menu_title = "Main Menu",
        options = ["Home" , "About" , "Predict", "Database" , "Admin"],
        icons = ["house-door-fill" , "person-fill" , "question-octagon-fill" , "file-earmark-fill" , "gear-fill"],
        menu_icon = "cast",
        default_index = 0,
)

#Menu Home
if nav_bar == "Home":
    st.write("Stunting is defined as low height-for-age. It is the result of chronic or recurrent undernutrition, usually associated with poverty, poor maternal health and nutrition, frequent illness and/or inappropriate feeding and care in early life. Stunting prevents children from reaching their physical and cognitive potential.")

#Menu About   
elif nav_bar == "About":

#Menu About   
elif nav_bar == "Predict":

#Menu About   
elif nav_bar == "Database":

#Menu About   
elif nav_bar == "Admin":