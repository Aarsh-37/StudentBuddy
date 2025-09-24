import streamlit as st
from dotenv import load_dotenv
import os
from test import configure_gemini, get_response, save_to_history
import re
import uuid

# --- Page Setup ---
st.set_page_config(page_title="Student Buddy", layout="wide")

# --- Load API Key and Initialize Gemini ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
model = configure_gemini(API_KEY)

# --- Initialize Session State ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

# --- Helper Functions ---

def render_code_blocks(text):
    """Render code blocks with copyable textarea (single display)"""
    code_blocks = re.findall(r'```(.*?)\n(.*?)```', text, re.DOTALL)
    for i, (lang, code) in enumerate(code_blocks):
        st.code(code, language=lang.strip() if lang else "python")
        # Copy button
        key = str(uuid.uuid4())
        if st.button("Copy Code", key=key):
            st.text_area("Copy", value=code, height=1, key=f"tmp_{key}", label_visibility="collapsed")
            st.success("Select and copy the code above")
        # Remove code from text
        text = text.replace(f"```{lang}\n{code}```", "")
    return text

def render_references(text):
    """Convert markdown-style links to clickable links"""
    links = re.findall(r'\[([^\]]+)\]\((http[s]?://[^\)]+)\)', text)
    for link_text, url in links:
        text = text.replace(f"[{link_text}]({url})", f'<a href="{url}" target="_blank">{link_text}</a>')
    return text

def display_response(response_text):
    """Render response text with code and references"""
    response_text = render_references(response_text)
    response_text = render_code_blocks(response_text)
    st.markdown(response_text, unsafe_allow_html=True)

def send_query():
    """Callback when Enter or Send button is pressed"""
    user_input = st.session_state.user_input
    if user_input.strip():
        response = get_response(model, user_input)
        st.session_state.history.append((user_input, response))
        st.session_state.user_input = ""  # Clear input

# --- Sidebar ---
with st.sidebar:
    st.header("Settings")
    if st.button("Clear History"):
        st.session_state.history = []
        st.success("History cleared!")

# --- Header ---
st.markdown("## Student Buddy")

# --- Display History ---
for q, r in st.session_state.history:
    st.markdown(f"**Q:** {q}")
    display_response(r)
    st.markdown("---")

# --- Input at Bottom ---
st.text_input(
    "Type your query here...",
    key="user_input",
    placeholder="Press Enter to send",
    on_change=send_query
)
st.button("Send", on_click=send_query)
