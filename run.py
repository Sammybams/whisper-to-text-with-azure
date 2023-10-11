import streamlit as st
st.set_page_config(page_title="Whisper-to-text bot run", page_icon="📊")


st.title("Whisper-to-text bot run")
# main.py
while True:
    with open("bot.py") as f:
        exec(f.read())