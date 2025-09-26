import streamlit as st

# Title
st.title("Streamlit Input Basics")

# Text input
name = st.text_input("Enter your name:")

# Number input
age = st.number_input("Enter your age:", min_value=0, max_value=120, step=1)

# Slider
rating = st.slider("Rate Streamlit (1-10):", 1, 10, 5)

# Select box
language = st.selectbox("Choose a programming language:", 
                        ["Python", "C++", "Java", "JavaScript"])

# Checkbox
subscribe = st.checkbox("Subscribe to newsletter")

# Radio buttons
gender = st.radio("Select Gender:", ["Male", "Female", "Other"])

# Button
if st.button("Submit"):
    st.write(f"👋 Hello {name}!")
    st.write(f"🎂 Age: {age}")
    st.write(f"⭐ Rating: {rating}")
    st.write(f"💻 Language: {language}")
    st.write(f"📩 Subscribed: {subscribe}")
    st.write(f"🧑 Gender: {gender}")
