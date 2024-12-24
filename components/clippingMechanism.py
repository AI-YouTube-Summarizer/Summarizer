import os
import tempfile
import subprocess
import streamlit as st

def copy_summary(summary_text):
    try:
        # Create a temporary file to store the summary
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(summary_text.encode('utf-8'))
            temp_file_path = temp_file.name

        # Use xclip to copy the content to the clipboard (Linux only)
        subprocess.run(["xclip", "-selection", "clipboard", temp_file_path])

        # Delete the temporary file after copying to clipboard
        os.remove(temp_file_path)

        # Provide success feedback to the user
        st.toast("Summary copied to clipboard!", icon="✅")

    except Exception as e:
        # Provide error feedback to the user
        st.toast(f"Error: {str(e)}", icon="❌")

    return copy_summary

