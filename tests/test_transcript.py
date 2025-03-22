import pytest
from unittest.mock import MagicMock
from app.services.transcript import TranscriptService
from youtube_transcript_api import NoTranscriptFound, TranscriptsDisabled

# Test extract_video_id with various URL formats
@pytest.mark.parametrize("url, expected", [
    # Standard URLs
    ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
    ("https://youtube.com/watch?v=dQw4w9WgXcQ&feature=shared", "dQw4w9WgXcQ"),
    
    # Shortened URLs
    ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
    ("https://youtu.be/dQw4w9WgXcQ?si=abc123", "dQw4w9WgXcQ"),
    
    # Embedded URLs
    ("https://www.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
    ("https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ?rel=0", "dQw4w9WgXcQ"),
    
    # Invalid URLs
    ("https://example.com", None),
    ("not_a_url", None),
    (None, None),
    ("", None)
])
def test_extract_video_id(url, expected):
    assert TranscriptService.extract_video_id(url) == expected

# Test successful transcript fetch
def test_get_transcript_success(mocker):
    # Mock the YouTubeTranscriptApi instance and its fetch method
    mock_yta = mocker.patch('app.services.transcript.YouTubeTranscriptApi')
    mock_instance = mock_yta.return_value

    # Create mock transcript snippets
    mock_snippets = [
        MagicMock(text="Hello"),
        MagicMock(text="world"),
        MagicMock(text="!")
    ]
    mock_transcript = MagicMock()
    mock_transcript.snippets = mock_snippets
    mock_instance.fetch.return_value = mock_transcript

    result = TranscriptService.get_transcript("valid_id")
    assert result == "Hello world !"

    # Verify API call with language prioritization
    mock_instance.fetch.assert_called_once_with(
        "valid_id",
        languages=['es', 'en']  # Spanish first, then English
    )

# Error testing with language parameter check
@pytest.mark.parametrize("exception, expected_message", [
    (NoTranscriptFound(video_id="No transcript", requested_language_codes= ['es', 'en'], transcript_data=""), "Transcript error: No transcript"),
    (TranscriptsDisabled("Disabled"), "Transcript error: Disabled"),
    (Exception("API Error"), "Transcript error: API Error")
])
def test_get_transcript_errors(mocker, exception, expected_message):
    mock_yta = mocker.patch('app.services.transcript.YouTubeTranscriptApi')
    mock_instance = mock_yta.return_value
    mock_instance.fetch.side_effect = exception

    with pytest.raises(ValueError) as exc_info:
        TranscriptService.get_transcript("invalid_id")

    assert str(exc_info.value) == expected_message
    mock_instance.fetch.assert_called_once_with(
        "invalid_id",
        languages=['es', 'en']
    )


# Test for empty video ID handling
def test_get_transcript_empty_id():
    with pytest.raises(ValueError) as exc_info:
        TranscriptService.get_transcript("")

    assert "Invalid video ID" in str(exc_info.value)
