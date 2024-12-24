import os
import streamlit as st
from groq import Groq



def render_sidebar():
    st.sidebar.title("API Key Setup")
    
    api_key = st.sidebar.text_input("Enter your [Groq](https://console.groq.com/keys) API key:", type="password")
    st.sidebar.markdown("""
To ensure your API key remains safe and accessible, please store it in a secure location. Here are some options:

- Use a **password manager** (recommended)
- Save it in a **secure note-taking app** ("like [Google Keep](https://keep.google.com)  or [Evernote](https://evernote.com/)")
- Write it down in a safe place

""")
    st.sidebar.link_button("Feedback Form", "https://forms.gle/EphDUS8x6Z1QdLLj9", type="secondary", icon=":material/forum:", use_container_width=False)
    
    client = None  # Global variable
    if api_key:
        client = Groq(api_key=api_key)
        st.sidebar.success("API Key is set. You can now use the summarization tool.")
        st.session_state["api_key"] = api_key  # Store in session state
    else:
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            client = Groq(api_key=api_key)
            st.sidebar.success("API Key loaded from environment variable.")
            st.session_state["api_key"] = api_key  # Store in session state
        else:
          st.sidebar.error("Please provide an API key to continue.")
    
    return client  # Return the client instance for further use
