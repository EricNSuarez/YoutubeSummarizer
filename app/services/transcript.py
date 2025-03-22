from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
from urllib.parse import urlparse, parse_qs

class TranscriptService:
    @staticmethod
    def extract_video_id(url: str) -> str | None:
        """
        Extracts YouTube video ID from various URL formats
        """
        # Check for non iterables and return None
        if not isinstance(url, str):
            return None
        if "youtu.be/" in url:
            return url.split("youtu.be/")[-1].split("?")[0]
        elif "v=" in url:
            return parse_qs(urlparse(url).query)['v'][0]
        elif "embed/" in url:
            return url.split("embed/")[-1].split("?")[0]
        return None

    @staticmethod
    def get_transcript(video_id: str) -> str:
        """
        Fetches and concatenates transcript text
        """
        if not video_id:
            raise ValueError(f"Invalid video ID: {str(video_id)}")

        try:
            transcript = YouTubeTranscriptApi().fetch(video_id, languages=['es', 'en'])
            return " ".join(entry.text for entry in transcript.snippets)
        except NoTranscriptFound:
            raise ValueError("Transcript error: No transcript")
        except TranscriptsDisabled:
            raise ValueError("Transcript error: Disabled")
        except Exception as e:
            raise ValueError(f"Transcript error: {str(e)}")
