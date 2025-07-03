
import streamlit as st


st.title("Nested button Check")

if 'Is_show_First_Button' not in st.session_state:
    st.session_state.Is_show_First_Button = False

if 'Is_show_Second_Button' not in st.session_state:
    st.session_state.Is_show_Second_Button = False


if st.button("First Button"):
    st.session_state.Is_show_Second_Button = True
    st.session_state.Is_show_First_Button = True

if st.session_state.Is_show_First_Button:
    st.write("This is First Button Click")

if st.session_state.Is_show_Second_Button:
         if st.button("Second Button"):
                st.write("This is Second Button Click")


   