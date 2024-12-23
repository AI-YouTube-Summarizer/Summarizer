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
