import streamlit as st
st.set_page_config(page_title="Whisper-to-text bot run", page_icon="📊")

# main.py
with open("bot.py") as f:
    exec(f.read())