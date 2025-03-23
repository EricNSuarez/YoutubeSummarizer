import pytest
from unittest.mock import MagicMock, patch
from app.services.summarizer import SummarizerService
from openai import APIStatusError, APIConnectionError, APIResponseValidationError
from httpx import Response
import os


@pytest.fixture(autouse=True)
def mock_env():
    # Mock environment variables for all tests
    with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-thisisafakekey123456789"}):
        yield


@pytest.fixture
def mock_response():
    response = MagicMock(spec=Response)
    response.status_code = 200
    response.headers = {}
    return response


def test_handle_401_error(mock_response):
    mock_response.status_code = 401
    error = APIStatusError(
        message="Invalid auth",
        response=mock_response,
        body={}
    )

    summarizer = SummarizerService()
    with pytest.raises(PermissionError):
        summarizer._handle_api_status_error(error)


def test_handle_429_error(mock_response):
    mock_response.status_code = 429
    error = APIStatusError(
        message="Rate limited",
        response=mock_response,
        body={}
    )

    summarizer = SummarizerService()
    with pytest.raises(RuntimeError):
        summarizer._handle_api_status_error(error)


@pytest.mark.parametrize("error_class,params", [
    (APIConnectionError, {"message": "Connection failed", "request": MagicMock()}),
    (APIResponseValidationError, {"response": MagicMock(), "body": b"test"}),
])
def test_connection_errors(error_class, params):
    with patch("app.services.summarizer.OpenAI") as mock_openai:
        mock_client = mock_openai.return_value
        mock_client.chat.completions.create.side_effect = error_class(**params)

        summarizer = SummarizerService()
        with pytest.raises(RuntimeError):
            summarizer.summarize("Valid text")


def test_server_error(mock_response):
    mock_response.status_code = 503
    error = APIStatusError(
        message="Server overloaded",
        response=mock_response,
        body={}
    )

    summarizer = SummarizerService()
    with pytest.raises(RuntimeError):
        summarizer._handle_api_status_error(error)