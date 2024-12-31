# chatbot.py

import os
import time
import streamlit as st
from groq import Groq

# Define the chatbot prompt template
chatbot_prompt_template = """The following is a summary of a YouTube video: {summary}.
You are an assistant that can provide more details based on this summary.
User question: {question}
Assistant response:"""

# Initialize show_prompt if not already done
if 'show_prompt' not in st.session_state:
    st.session_state.show_prompt = False

def initialize_client(api_key):
    """Initialize the Groq client with the provided API key."""
    return Groq(api_key=api_key)

def generate_chatbot_response(client, user_question):
    """Generate a response from the chatbot based on the cached summary and user question."""
    # Retrieve summary from session state
    summary = st.session_state.get('follow_up_summary', "")
    if not summary:
        return "No summary available. Please generate a summary first."

    # Format the prompt
    formatted_prompt = chatbot_prompt_template.format(summary=summary, question=user_question)

    # Generate response using the client
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": formatted_prompt}],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    # Accumulate response chunks
    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""

    return response

@st.fragment
def display_download_button(content, file_name):
    """Display a download button for the assistant's response."""
    if st.download_button(
        label="Save",
        data=content,
        file_name=file_name,
        mime="text/plain",
        icon=":material/download:"
    ):
        st.toast("ChatBot response download successfully!", icon="✅")

def display_typing_simulation(text, delay=0.008):
    """Simulate typing effect for displaying responses."""
    response_placeholder = st.empty()
    displayed_text = ""
    for char in text:
        displayed_text += char
        response_placeholder.markdown(displayed_text + "▌")  # Adds a cursor effect
        time.sleep(delay)  # Adjust typing speed here
    response_placeholder.markdown(displayed_text)  # Final display without cursor

def display_chat(client):
    """Display the chat interface and handle user interactions."""
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Chat container for messages
    container = st.container(border=True)

    # Display previous messages
    with container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat input and logic
    if st.session_state.show_prompt:
        prompt = st.chat_input("Type your queries here...")

        if prompt:
            # Append user message
            st.session_state.messages.append({"role": "user", "content": prompt})

            with container:
                # Display user input in chat
                with st.chat_message("user"):
                    st.markdown(prompt)

                # Generate assistant response
                with st.chat_message("assistant"):
                    try:
                        assistant_response = generate_chatbot_response(client, prompt)
                        display_typing_simulation(assistant_response)

                        # Append assistant response to session state
                        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

                        # Retrieve summary file name from session state
                        summary_file_name = st.session_state.get('summary_file_name', "default_summary.txt")

                        # Display the download button for the response
                        display_download_button(assistant_response, summary_file_name)

                    except Exception as e:
                        st.error(f"Error generating response: {e}")

