from groq import Groq
import streamlit as st

client = None  # This should be set in your main app.py after loading the API key

prompt_template = """Summarize the given YouTube video transcript in bullet points, focusing only on the most important information. The summary should be clear, concise, and within 250 words. Please summarize it in {language}."""

def generate_llama3_content(client, transcript_text, prompt, language):
    formatted_prompt = prompt.format(language=language)
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "user",
                "content": formatted_prompt + transcript_text
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    
    summary = ""
    for chunk in completion:
        summary += chunk.choices[0].delta.content or ""
    
    return summary


# Caching function for generating summary
@st.cache_data(show_spinner=True)
def get_summary(_client, transcript_text, language, video_id):
    """Generate and cache the summary based on the transcript."""
    # Create a unique cache key based on video ID and language to avoid regenerating the summary
    cache_key = f"summary_{video_id}_{language}"
    
    # Check if the summary is already in Streamlit's session state cache
    if cache_key in st.session_state:
        # Return the cached summary
        return st.session_state[cache_key]
    
    # Generate a new summary and cache it in session state
    summary = generate_llama3_content(_client, transcript_text, prompt_template, language)
    
    # Store the generated summary in session state for future use
    st.session_state[cache_key] = summary
    
    return summary
