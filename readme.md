# AI YouTube Summarizer

This project is a Streamlit-based web application designed to summarize YouTube videos or podcasts efficiently. It uses state-of-the-art AI models and offers features to customize summaries in terms of tone and length.

## Features

- Summarize YouTube videos (supports 1-2 hour videos with efficient token usage).
- Select summary language.
- Customize summaries with different tones and lengths.
- Cache management: summaries are cached for reuse to save computation.
- No database required; uses temporary storage.
- Download or copy generated summaries directly.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/ai-youtube-summarizer.git
   ```

2. Navigate to the project directory:
   ```bash
   cd ai-youtube-summarizer
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the environment variables:
   - Create a `.env` file in the root directory.
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key
     ```

5. Run the application:
   ```bash
   streamlit run app.py
   ```
---

### Clipboard Functionality Setup for Different Operating Systems

This project uses clipboard functionality for copying summaries directly to the clipboard. Depending on your operating system, follow the instructions below to ensure proper setup.

#### **For Linux**
The app uses `xclip` to enable clipboard functionality on Linux systems.

1. **Install xclip**:  
   Run the following command in your terminal:
   ```bash
   sudo apt-get install xclip
   ```

2. **Verify Installation**:  
   Test if `xclip` is installed by running:
   ```bash
   echo "Clipboard test" | xclip -selection clipboard
   ```
   Paste the clipboard content (e.g., in a text editor) to confirm.

3. **Run the App**:  
   Ensure that `xclip` is accessible in your environment, and the app will use it for clipboard operations automatically.

#### **For Windows**
The app uses `pyperclip` for clipboard functionality on Windows systems.

1. **Install pyperclip**:  
   Run the following command to install `pyperclip`:
   ```bash
   pip install pyperclip
   ```

2. **Verify Clipboard Support**:  
   Pyperclip works seamlessly on Windows without additional dependencies. Run this Python snippet to test:
   ```python
   import pyperclip
   pyperclip.copy("Clipboard test")
   print(pyperclip.paste())
   ```

3. **Run the App**:  
   The app will automatically use `pyperclip` on Windows for clipboard operations.

---

#### **Code Behavior**
The app detects the operating system and uses the appropriate library for clipboard operations. You don’t need to configure anything manually beyond ensuring `xclip` (Linux) or `pyperclip` (Windows) is installed.

---

### Example Usage
1. Click the "Copy to Clipboard" button in the app.
2. A notification will appear, confirming the text is copied to your clipboard.
3. Paste the copied content into any text editor (e.g., `Ctrl + V` or `Cmd + V`).

---

## Usage

1. Open the application in your browser (usually at `http://localhost:8501`).
2. Paste the YouTube video URL.
3. Select the desired summary language.
4. Generate the default summary or request customized summaries using the chatbot.
5. Download or copy the summary as needed.

## Project Structure

- `app.py`: Main Streamlit application.
- `chatbot.py`: Handles chatbot functionality for customizable summaries.
- `summarization.py`: Core logic for summarizing YouTube content.
- `utils/`: Helper functions and utilities.
- `assets/`: Static files like terms and guidelines.

## License

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0). See the `LICENSE` file for details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Disclaimer

This application is for personal use only. Redistribution or claiming ownership of this project is prohibited.
