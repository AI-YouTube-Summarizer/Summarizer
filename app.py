# Import necessary libraries
import time
import streamlit as st
from groq import Groq
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from yt_dlp import YoutubeDL
from components.intro import display_intro
from components.chatbot import display_chat, initialize_client
from components.url_validation import is_valid_youtube_url
from utils.summarization import get_summary
from components.sidebar import render_sidebar
from styles.styles import get_titleCenter_css

st.set_page_config(
    page_title="AI YouTube Summarizer",
    page_icon="AI_YouTube_Summarizer.png",
    initial_sidebar_state="expanded",
    )


# Initialize session state variables in one place for better organization
if "accepted_terms" not in st.session_state:
    st.session_state.accepted_terms = False
if "show_prompt" not in st.session_state:
    st.session_state.show_prompt = False
if "cached_summary_timestamp" not in st.session_state:
    st.session_state.cached_summary_timestamp = None
if "summary_file_name" not in st.session_state:
    st.session_state.summary_file_name = ""
if "cached_summary" not in st.session_state:
    st.session_state.cached_summary = None

# Define the Terms and Conditions dialog
@st.dialog("Terms and Conditions", width="large")
def terms_dialog():
    """
    Display the terms and conditions dialog, requiring user acceptance before proceeding.
    """
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

    # Add "I Accept" button for the user to accept the terms
    if st.button("I Accept"):
        st.session_state.accepted_terms = True
        st.rerun()  # Rerun the app to close the dialog and proceed

# Show terms dialog if not accepted
if not st.session_state.accepted_terms:
    terms_dialog()

# Load environment variables
load_dotenv()

# Language options for subtitle extraction and summary generation
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

def extract_transcript_details(video_url, lang="en"):
    """
    Extract subtitles for a given YouTube video using yt-dlp.

    Args:
        video_url (str): The YouTube video URL.
        lang (str): The language code for subtitles (default is 'en').

    Returns:
        str: The subtitles as text if available, otherwise None.
    """
    options = {
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': [lang],
        'skip_download': True,
        'quiet': True,
    }

    try:
        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(video_url, download=False)
            subtitles = info.get('requested_subtitles', {})
            subtitle_info = subtitles.get(lang)

            if subtitle_info:
                subtitle_url = subtitle_info['url']
                response = requests.get(subtitle_url)
                response.raise_for_status()
                return response.text
            else:
                st.error(f"⚠️ Subtitles not available in the selected language ({lang}).")
                return None
    except Exception as e:
        st.error(f"Error fetching subtitles: {e}")
        return None

# Main application logic if terms are accepted
if st.session_state.accepted_terms:
    # Placeholder for success message
    success_placeholder = st.empty()
    success_placeholder.success("Thank you for accepting the terms! You may now use the summarization tool.", icon="✅")

    # Render the sidebar and initialize the client
    client = render_sidebar()

    if client:
        # Display application title
        st.markdown("<h1 class='centered-title'>AI YouTube Summarizer 📝</h1>", unsafe_allow_html=True)
        st.markdown(get_titleCenter_css, unsafe_allow_html=True)
        st.write("")

        # Initialize intro display state
        if 'show_intro' not in st.session_state:
            st.session_state.show_intro = True 

        # Layout with two columns: video input and language selection
        col1, col2 = st.columns([3, 1])

        with col1:
            # Input field for YouTube video link
            youtube_link = st.text_input("Enter YouTube Video Link:", placeholder="https://www.youtube.com/watch?v=example")
            
            if youtube_link:
                # Validate the provided YouTube URL
                if not is_valid_youtube_url(youtube_link):
                    st.error("⚠️ Invalid YouTube URL. Please enter a valid YouTube video link.")
                    st.stop()

        with col2:
            # Dropdown menu to select the video language
            selected_language = st.selectbox("Select video language:", list(LANGUAGES.keys()), format_func=lambda x: LANGUAGES[x])    

        if youtube_link:
            # Fetch video title and prepare summary filename
            response = requests.get(youtube_link, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.title.string.replace(" - YouTube", "").strip()
            summary_file_name = f"{title}_Summary.txt"
            st.session_state.summary_file_name = summary_file_name
            success_placeholder.empty()

            # Display the YouTube video
            st.video(youtube_link, format="video/mp4")
            st.write("")  # Space for layout adjustment

            # Button to fetch detailed notes
            button_placeholder = st.empty()
            # Create a placeholder for the follow-up section
            follow_up_placeholder = st.empty()

            if button_placeholder.button("Get Detailed Notes", icon="📓", use_container_width=True):
                button_placeholder.empty()
                st.session_state.show_prompt = True

                # Generate or fetch cached summary
                current_time = time.time()
                cache_expiry = 3600  # 1 hour expiration for cached summary

                if ('cached_summary' not in st.session_state or 
                    st.session_state.cached_summary_timestamp is None or 
                    current_time - st.session_state.cached_summary_timestamp > cache_expiry):

                    # Extract transcript details for the video
                    transcript_text = extract_transcript_details(youtube_link, selected_language)

                    if transcript_text:
                        # Generate a summary using the transcript
                        summary = get_summary(client, transcript_text, LANGUAGES[selected_language], youtube_link.split("=")[1])
                        if summary is not None:
                            # Cache the generated summary and timestamp
                            st.session_state.cached_summary = summary
                            st.session_state.cached_summary_timestamp = current_time
                        else:
                            st.error("❌ Unable to generate the summary.")
                    else:
                        st.error("❌ No subtitles found for the provided video link.")
                else:
                    # Use cached summary if available
                    summary = st.session_state.cached_summary

                # Display summary and provide actions
                if summary:
                    st.session_state.follow_up_summary = summary  # Store the summary in session state for chatbot access
                    st.markdown("## Detailed Notes:")
                    st.markdown(summary)

                    # Actions: clear cache and download summary
                    c1, c2 = st.columns(2)
                    with c1:
                        @st.fragment
                        def clearCache():
                            if st.button("Clear Cache", icon="🗑️", use_container_width=True):
                                # Clear cache data and notify the user
                                st.cache_data.clear()
                                st.session_state.is_cached = False
                                st.toast("Cache cleared successfully!")
                        clearCache()

                    with c2:
                        # Provide a button to download the summary
                        @st.fragment
                        def downloadSubs():
                            if st.download_button(
                                label="Download Summary",
                                icon=":material/download:",
                                data=summary,
                                file_name=summary_file_name,
                                mime="text/plain", 
                                use_container_width=True
                            ):
                                st.toast("Summary download successfully!")
                        downloadSubs()
                            
                else:
                    st.warning("⚠️ No summary available.")

                st.session_state.show_intro = False

        # Display introductory information if needed
        if st.session_state.show_intro:
            display_intro()
    else:
        display_intro()

    # Display chatbot interface
    def main():
        """
        Main function to display the chatbot interface if the client is initialized.
        """
        if client:
            display_chat(client)

    if __name__ == "__main__":
        main()
else:
    # Show message if terms are not accepted
    time.sleep(1)
    st.title("Terms and Conditions Not Accepted")
    st.warning("We're sorry, but you must accept our Terms and Conditions to proceed. Your understanding and agreement help us maintain a safe and trustworthy environment for all users. If you have any questions or concerns about our terms, please feel free to reach out to us for clarification.")
    st.caption("Reload to continue")
