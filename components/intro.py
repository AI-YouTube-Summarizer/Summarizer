import streamlit as st

def display_intro():
    # Introductory message
    st.divider()
    intro_message = """
    ### About AI-Powered YouTube Summarizer:

    Welcome to our **AI YouTube Summarizer**! This powerful tool allows you to effortlessly transform your favorite YouTube videos into concise and easy-to-read summaries. Whether you're looking to get quick insights for study purposes or just want to grasp the key points of a video without watching it in full, you've come to the right place!

    ### How to Get Started:
    1. **Find a Video:** Go to YouTube and search for a video you wish to summarize. 
    2. **Copy the Link:** Copy the URL from the browser address bar (e.g., `youtube.com/watch?v=video_id`).
    3. **Paste the URL:** Paste the video link into the input box above and press Enter.
    4. **Select Language:** Choose your preferred language for the summary from the dropdown menu.
    5. **Receive Your Summary:** Our AI will process the video and generate a clear, concise summary in just a few moments!

    The usage of our summarization tool is completely **free and secure**, accessible on any device—desktop, tablet, or mobile—without the need for any additional software installation. 

    Thank you for choosing our YouTube Summarizer! By continuing to use this service, you agree to our Terms of Use.
    """

    # Display the introductory message
    st.markdown(intro_message)
    st.divider()
    return display_intro