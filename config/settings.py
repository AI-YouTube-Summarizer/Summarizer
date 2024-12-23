import os
from dotenv import load_dotenv

def load_api_key():
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("API Key not found. Please set it in your environment.")
    return api_key
