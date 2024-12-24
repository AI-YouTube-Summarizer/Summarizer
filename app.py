import time
import streamlit as st
from groq import Groq
import requests
from bs4 import BeautifulSoup # type: ignore
from dotenv import load_dotenv
from components.intro import display_intro
from components.chatbot import display_chat, initialize_client
from components.url_validation import is_valid_youtube_url
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from utils.summarization import get_summary
from utils.youtube_transcript import extract_transcript_details
from components.sidebar import render_sidebar
from styles.styles import get_titleCenter_css

# Initialize the acceptance state
if "accepted_terms" not in st.session_state:
    st.session_state.accepted_terms = False
# Initialize session state variables
if "show_prompt" not in st.session_state:
    st.session_state.show_prompt = False


# Define the Terms and Conditions dialog
@st.dialog("Terms and Conditions", width="large")
def terms_dialog():
    st.write("By using this tool, you agree to the following terms and conditions:")

    st.subheader("1. Developmental Status")
    st.markdown(
        """
        This tool is currently in development, and occasional bugs or inaccuracies may occur. 
        We encourage users to provide feedback to help improve the experience.
        """
    )

    st.subheader("2. Liability")
    st.markdown(
        """
        The creators are not liable for any misuse or unintended consequences resulting from the use of this tool. 
        Users are solely responsible for how they utilize and interpret the generated summaries.
        """
    )

    st.subheader("3. Content Compliance")
    st.markdown(
        """
        Users are responsible for ensuring that the video content they summarize complies with platform policies and copyright 
        regulations. We hold no responsibility for issues arising from summarizing or sharing content that violates third-party terms.
        """
    )

    st.subheader("4. Data Privacy")
    st.markdown(
        """
        This tool does not store your API keys, video content, or generated summaries on external servers. 
        All processing occurs in real-time, ensuring your data remains private and secure.
        """
    )

    # "I Accept" button within the dialog
    if st.button("I Accept"):
        st.session_state.accepted_terms = True
        st.rerun()  # Rerun the app to close the dialog and proceed

# Display the Terms dialog if terms have not been accepted
if not st.session_state.accepted_terms:
    terms_dialog()

# Load environment variables
load_dotenv()

# Supported languages for Llama 3
LANGUAGES = {
    "en": "English",
    "en-GB": "English (UK)",
    "hi": "Hindi",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "zh": "Chinese (Simplified)",
    "ar": "Arabic",
    "ru": "Russian",
    "pt": "Portuguese"
}


# Main app content, shown only if terms are accepted
if st.session_state.accepted_terms:
    # Define a function to show a temporary success message
    success_placeholder = st.empty()  # Create a placeholder
    success_placeholder.success("Thank you for accepting the terms! You may now use the summarization tool.", icon="✅")
    # Render sidebar and get client instance
    client = render_sidebar()
    
    if client:
        # Streamlit app layout
        st.markdown("<h1 class='centered-title'>AI YouTube Summarizer 📝</h1>", unsafe_allow_html=True)
        st.markdown(get_titleCenter_css, unsafe_allow_html=True)
        st.write("")  # You can adjust this line for more space; use "st.write('\n')" for more lines.
        
        # Check if the intro should be displayed
        if 'show_intro' not in st.session_state:
            st.session_state.show_intro = True 
            
        col1, col2 = st.columns([3, 1])

        with col1:
            youtube_link = st.text_input("Enter YouTube Video Link:", placeholder="https://www.youtube.com/watch?v=example")
            # Validate YouTube URL
            if youtube_link:
                if not is_valid_youtube_url(youtube_link):
                    st.error("⚠️ Invalid YouTube URL. Please enter a valid YouTube video link.")
                    st.stop()
                    
        with col2:
            # Language selection dropdown
            selected_language = st.selectbox("Select video language:", list(LANGUAGES.keys()), format_func=lambda x: LANGUAGES[x])    
    
        # Handle YouTube link and fetch video ID
        if youtube_link:
            response = requests.get(youtube_link, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract and clean the video title
            title = soup.title.string.replace(" - YouTube", "").strip()
            summary_file_name = f"{title}_Summary.txt"
            st.session_state.summary_file_name = summary_file_name
            success_placeholder.empty()  # Clear the message
            video_id = youtube_link.split("=")[1]
                        
            # display_youtube_thumbnail(video_id)
            st.video(youtube_link, format="video/mp4", start_time=0, subtitles=None, end_time=None, loop=False, autoplay=False, muted=False)
            
            st.write("")  # Space for layout adjustment
    
            # Button placeholder for detailed notes
            button_placeholder = st.empty()
            

            # Create a placeholder for the follow-up section
            follow_up_placeholder = st.empty()

            # Button to fetch detailed notes and display summary
            if button_placeholder.button("Get Detailed Notes", icon="📓", use_container_width=True):
                button_placeholder.empty()  # Hides the button
                st.session_state.show_prompt = True

                if 'cached_summary' not in st.session_state:
                    transcript_text = extract_transcript_details(youtube_link, selected_language)

                    if transcript_text:
                        summary = get_summary(client, transcript_text, LANGUAGES[selected_language], video_id)
                        if summary is not None:
                            st.session_state.cached_summary = summary
                        else:
                            summary = None
                            st.error("❌ Unable to generate the summary.")
                    else:
                        summary = None
                        st.error("❌ No transcript found for the provided video link.")
                else:
                    summary = st.session_state.cached_summary

               
                # Display the summary
                if summary:
                    st.session_state.follow_up_summary = summary  # Store the summary in session state for chatbot access
                    st.markdown("## Detailed Notes:")
                    st.markdown(summary)
                    

                    # Add buttons for cache clearing, clipboard copy, and download
                    c1, c2 = st.columns(2)

                    with c1:
                            @st.fragment
                             # Button to clear cache
                            def clearCache():
                                if st.button("Clear Cache", icon="🗑️", use_container_width=True):
                                    st.cache_data.clear()
                                    st.session_state.is_cached = False  # Reset cache status
                                    st.toast("Cache cleared successfully!" )
                            clearCache()
                            
                    with c2:
                            @st.fragment
                            def main():
                                # Create the download button
                                st.download_button(
                                    label="Download Summary",
                                    icon=":material/download:",
                                    data=summary,  # Directly pass the string without encoding
                                    file_name=summary_file_name,
                                    mime="text/plain", 
                                    use_container_width=True
                                )
                            if __name__ == "__main__":
                                main()
                else:
                    st.warning("⚠️ No summary available.")

                st.session_state.show_intro = False  # Hide intro once summary is displayed
                 
        # Display the intro if the condition is met
        if st.session_state.show_intro:
            display_intro()

    else:
        display_intro()

    def main():"""Main function to run the Streamlit app."""
    
    if client:  # Ensure client is initialized before calling display_chat.
        display_chat(client)
    else:
        pass
    if __name__ == "__main__":
        main()
else:
    time.sleep(1)
    st.title("Terms and Conditions Not Accepted")
    st.warning("We're sorry, but you must accept our Terms and Conditions to proceed. Your understanding and agreement help us maintain a safe and trustworthy environment for all users. If you have any questions or concerns about our terms, please feel free to reach out to us for clarification.")
    st.caption("Reload to continue")
    
