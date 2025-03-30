from openai import OpenAI, APIError, APIStatusError, APIConnectionError, APIResponseValidationError
import os
import tiktoken

class SummarizerService:
    MAX_TOKENS = 4096  # GPT-3.5-turbo context window
    DEFAULT_PROMPT = """Act as a professional content summarizer with expertise in distilling key information from videos. Summarize the YouTube video transcript provided below. Follow these guidelines:

Objective:

    Capture the core message, main arguments, and essential details of the video.
    Prioritize accuracy and avoid introducing external knowledge.

Structure:

    Overview: Start with a 1-2 sentence summary of the video’s primary topic and purpose.
    Key Points: Extract 3-5 critical ideas, examples, or steps. Use bullet points for clarity.
    Conclusion: Highlight the final takeaways, recommendations, or calls-to-action.

Tone & Style:

    Keep the summary concise (aim for [X] words/paragraphs) and neutral.
    Use simple, accessible language (avoid jargon unless necessary).
    Paraphrase effectively to avoid redundancy.

Additional Instructions:

    Ignore ads, sponsor segments, or non-essential tangents.
    Note any biases or unsupported claims in the video (if applicable).
    If the video is technical, adjust terminology for a general audience.

Provide the summary in the following format:
[Overview]
[Concise summary]

[Key Points]

    [Point 1]
    
    [Point 2]
    ...

[Conclusion]
[Final takeaways]

Note: If the transcript is unclear or incomplete, state what information is missing."""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable not set")

        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "o3-mini")
        self.encoder = tiktoken.encoding_for_model(self.model)

    def _count_tokens(self, text: str) -> int:
        """Count tokens using the model's encoder"""
        return len(self.encoder.encode(text))

    def summarize(self, text: str) -> str:
        """
        Generates a summary using OpenAI with robust error handling
        """
        # Input validation
        if not text.strip():
            raise ValueError("Input text cannot be empty")

        input_tokens = self._count_tokens(text)
        if input_tokens > self.MAX_TOKENS:
            raise ValueError(
                f"Input exceeds {self.MAX_TOKENS} tokens ({input_tokens} detected). "
                "Please provide shorter text."
            )

        try:
            return self._call_openai_api(text)
        except APIStatusError as e:
            return self._handle_api_status_error(e)
        except (APIConnectionError, APIResponseValidationError) as e:
            raise RuntimeError(f"Connection error: {str(e)}") from e
        except Exception as e:
            raise RuntimeError(f"Unexpected error: {str(e)}") from e

    def _call_openai_api(self, text: str) -> str:
        """Execute the OpenAI API call with proper error handling"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.DEFAULT_PROMPT},
                    {"role": "user", "content": text}
                ],
                max_completion_tokens=1500
            )

            if not response.choices or not response.choices[0].message.content:
                raise APIError("Empty response from OpenAI API")

            return response.choices[0].message.content

        except APIError as e:
            raise

    @staticmethod
    def _handle_api_status_error(error: APIStatusError) -> None:
        """Handle different API status code errors"""
        if error.status_code == 401:
            raise PermissionError("Invalid OpenAI API credentials") from error
        if error.status_code == 429:
            raise RuntimeError("OpenAI API rate limit exceeded - please wait before retrying") from error
        if 500 <= error.status_code < 600:
            raise RuntimeError("OpenAI server error - try again later") from error

        raise RuntimeError(f"OpenAI API request failed: {error.message}") from error
