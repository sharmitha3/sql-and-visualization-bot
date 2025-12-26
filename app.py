import streamlit as st
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
mysql_host = os.getenv("MYSQL_HOST")
mysql_user = os.getenv("MYSQL_USER")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_db = os.getenv("MYSQL_DATABASE")

# Import the page functions
from sql_bot import show_sql_bot
from viz_bot import show_viz_bot

# Sidebar
st.sidebar.title("Groq SQL Chatbot")
st.sidebar.write("Upload CSV, ask questions in English, get SQL-powered answers.")
st.sidebar.success(
    """
🕵️ SQL? Nah, just talk to me.  
💬 Your data’s best friend.  
🔥 Less typing, more vibing.
"""
)

if not api_key:
    st.sidebar.error("GROQ_API_KEY missing in .env file.")
    st.stop()

# Session state
if "animation_done" not in st.session_state:
    st.session_state.animation_done = False

if "page" not in st.session_state:
    st.session_state.page = "landing"

# ---------------- Animation ----------------
def sliding_words_animation():
    words = [
        "Upload your CSV and explore data.",
        "Ask questions in plain English.",
        "Instant SQL query generation.",
        "Simple & powerful data insights."
    ]
    placeholder = st.empty()
    for w in words:
        placeholder.markdown(f"### {w}")
        time.sleep(1)
    placeholder.empty()
    st.session_state.animation_done = True

# ---------------- LANDING PAGE ----------------
if st.session_state.page == "landing":
    st.title("LLM-Powered SQL AND Vizualization bot")

    if not st.session_state.animation_done:
        sliding_words_animation()

    st.write("### Choose your bot:")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🟦 SQL Bot")
        st.write(
            """
- Upload a CSV  
- Ask questions in English  
- Auto SQL generation  
- See SQL results  
"""
        )
        if st.button("Go to SQL Bot"):
            st.session_state.page = "sql_bot"
            st.rerun()

    with col2:
        st.markdown("### 📊 Viz Bot")
        st.write(
            """
- Upload CSV  
- Explore with charts  
- Bar, Line, Scatter, Pie, Histogram  
"""
        )
        if st.button("Go to Viz Bot"):
            st.session_state.page = "viz_bot"
            st.rerun()

# ---------------- SQL BOT PAGE ----------------
elif st.session_state.page == "sql_bot":
    show_sql_bot(api_key, mysql_host, mysql_user, mysql_password, mysql_db)

# ---------------- VIZ BOT PAGE ----------------
elif st.session_state.page == "viz_bot":
    show_viz_bot(mysql_host, mysql_user, mysql_password, mysql_db)
