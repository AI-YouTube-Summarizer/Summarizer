import logging
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

def extract_transcript_details(youtube_video_url, selected_language):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Check if the selected language is available
        transcript = transcript_list.find_transcript([selected_language])
        transcript_text = transcript.fetch()

        return " ".join([entry["text"] for entry in transcript_text])
    
    except TranscriptsDisabled:
        logging.error("Transcripts are disabled for this video.")
        return None
    
    except NoTranscriptFound as e:
        available_languages = transcript_list.languages
        fallback_language = "en-GB" # Fallback to English (United Kingdom) if available

        if fallback_language in available_languages:
            logging.warning(f"No transcript found for {selected_language}. Trying fallback language: {fallback_language}.")
            transcript = transcript_list.find_transcript([fallback_language])
            transcript_text = transcript.fetch()
            return " ".join([entry["text"] for entry in transcript_text])
        else:
            logging.error(f"No transcripts were found for the requested language codes: {selected_language}. Available languages: {available_languages}.")
            return None
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None
