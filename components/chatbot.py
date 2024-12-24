# components/chatbot.py
import streamlit as st
import time
from groq import Groq


chatbot_prompt_template = """The following is a summary of a YouTube video: {summary}. You are an assistant that can provide more details based on this summary. 
User question: {question} 
Assistant response:"""

def initialize_client(api_key):
    """Initialize the Groq client with the provided API key."""
    return Groq(api_key=api_key)

# chatbot.py

def generate_chatbot_response(client, user_question):
    """Generate a response from the chatbot based on the cached summary and user question."""
    
    # Ensure we have a summary available in session state
    summary = st.session_state.get('follow_up_summary', "")  # Retrieve from session state
    if not summary:
        return "No summary available. Please generate a summary first."
    
    summary_file_name = st.session_state.get("summary_file_name")
    if not summary_file_name:
        st.toast("No summary found")
        
    # Format the prompt using the retrieved summary
    formatted_prompt = chatbot_prompt_template.format(summary=summary, question=user_question)

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "user",
                "content": formatted_prompt
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""

    return response


def display_chat(client):
    """Display the chat interface and handle user interactions."""
    # Initialize session state for messages if not already done
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Initialize show_prompt if not already done
    if 'show_prompt' not in st.session_state:
        st.session_state.show_prompt = False

    # Container for displaying chat messages
    container = st.container(border=True)

    # Display previous messages in the chat
    with container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Conditionally render the chat input field based on the button click
    if st.session_state.show_prompt:
        prompt = st.chat_input("Type your queries here...")  # Capture user input

        if prompt:  # Ensure prompt is not empty before calling function
            # Append user message to session state
            st.session_state.messages.append({"role": "user", "content": prompt})

            with container:
                with st.chat_message("user"):
                    st.markdown(prompt)  # Display user input

                assistant_response = ""  # Initialize assistant_response

                with st.chat_message("assistant"):
                    try:
                        # Generate assistant response using summary from session state
                        summary = st.session_state.get('follow_up_summary', "")
                        assistant_response = generate_chatbot_response(client, prompt)  # Pass client, summary, and prompt

                        display_typing_simulation(assistant_response)  # Simulate typing
                    except TypeError as e:
                        st.error(f"Error: {e}")
                        print(f"TypeError in generate_chatbot_response: {e}")
                # Define the function for the copy button
                @st.fragment
                def download_button():
                    # Create the download button
                    if st.download_button(
                        label="Download Response",
                        icon=":material/download:",
                        data=assistant_response,  # Directly pass the string without encoding
                        file_name=summary_file_name,
                        mime="text/plain", 
                        use_container_width=True):
                            st.toast("Assistant response copied to clipboard!") 

                # Append assistant response to session state if it has a value
                if assistant_response:  # Only append if assistant_response has a value
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                    
                    # Call the function to render the button
                    download_button()
                else:
                    st.error("Assistant response was not generated.")  # Optional error message
                
                


def display_typing_simulation(text, delay=0.008):
    """Simulate typing effect for displaying responses."""
    response_placeholder = st.empty()
    
    displayed_text = ""
    
    for char in text:
        displayed_text += char
        response_placeholder.markdown(displayed_text + "▌")  # Adds a cursor effect
        time.sleep(delay)  # Adjust typing speed here

    response_placeholder.markdown(displayed_text)  # Final display without cursor
