# YouTube Video Summarizer

A web application that generates concise summaries of YouTube videos using OpenAI's GPT.

## Features

- **YouTube URL Processing**: Supports standard and shortened URLs
- **Transcript Extraction**: Fetches video subtitles via YouTube Transcript API
- **AI-Powered Summaries**: Generates bullet-point summaries using OpenAI 3o-mini
- **Error Handling**: Gracefully manages invalid URLs and missing transcripts

## Installation

1. **Clone Repository**:
   ```bash
   git clone https://github.com/EricNSuarez/YoutubeSummarizer
   cd YoutubeSummarizer
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


## YouTube Video Summarizer (Local Development Only)

⚠️ **Important Notice**  
This project now focuses exclusively on local development due to YouTube API restrictions.  
I've encountered IP blocking issues when deploying to cloud servers. Feel free to use this locally!

### Why Local Only?

YouTube actively blocks transcript requests from:

- Cloud provider IPs (AWS, DigitalOcean, etc.)
- High-volume IP addresses

I would rather prioritize putting effort on other projects over thinking of workarounds that violate YouTube's ToS.

**Technical Note:** While the project could be modified to use YouTube's official API for transcript retrieval, this alternative approach would only work for videos with manually added captions and wouldn't support auto-generated transcripts. I've chosen to maintain the current implementation for its simplicity and broader compatibility with most YouTube content.

## Quick Local Start
```bash
git clone https://github.com/EricNSuarez/YoutubeSummarizer
cd YoutubeSummarizer
docker-compose up --build
```

## Demo

![Demo](../assets/demo.gif?raw=true)

*Demo showing the full workflow: URL input → summary generation → formatted output*

## Acknowledgements

- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api)
- [OpenAI Python Client](https://github.com/openai/openai-python)
- [Flask Documentation](https://flask.palletsprojects.com/)