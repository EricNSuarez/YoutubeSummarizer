# YouTube Video Summarizer

A web application that generates concise summaries of YouTube videos using OpenAI's GPT.

## Features

- **YouTube URL Processing**: Supports standard and shortened URLs
- **Transcript Extraction**: Fetches video subtitles via YouTube Transcript API
- **AI-Powered Summaries**: Generates bullet-point summaries using OpenAI GPT-3.5-turbo/GPT-4
- **Error Handling**: Gracefully manages invalid URLs and missing transcripts

## Installation

1. **Clone Repository**:
   ```bash
   git clone https://github.com/yourusername/youtube-summarizer.git
   cd youtube-summarizer
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Setup**:
   - Create `.env` file:
     ```env
     OPENAI_API_KEY=your_openai_key_here
     FLASK_ENV=production
     ```
   - Replace `your_openai_key_here` with your [OpenAI API key](https://platform.openai.com/api-keys)

## Configuration

### Environment Variables
| Variable         | Required | Default          | Description                          |
|------------------|----------|------------------|--------------------------------------|
| `OPENAI_API_KEY` | Yes      | -                | OpenAI API key                       |
| `OPENAI_MODEL`   | No       | gpt-3.5-turbo    | GPT model version                    |
| `MAX_TOKENS`     | No       | 150              | Max tokens for summary               |

## Acknowledgements

- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api)
- [OpenAI Python Client](https://github.com/openai/openai-python)
- [Flask Documentation](https://flask.palletsprojects.com/)