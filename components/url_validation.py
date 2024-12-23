import re
import streamlit as st
import requests
from urllib.parse import urlparse

def is_valid_youtube_url(url):
    # Comprehensive YouTube URL regex pattern
    youtube_regex = (
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    
    # Check if the URL matches the pattern
    if re.match(youtube_regex, url):
        try:
            # Additional validation by checking response
            response = requests.get(url)
            if response.status_code == 200 and "YouTube" in response.text:
                return True
        except requests.exceptions.RequestException:
            return False
    return False