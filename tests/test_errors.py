import httpx
from groq import APIConnectionError, RateLimitError

from app.errors import user_friendly_error_message


def test_rate_limit_has_helpful_message() -> None:
    request = httpx.Request(
        "POST",
        "https://api.groq.com/openai/v1/chat/completions",
    )
    response = httpx.Response(
        status_code=429,
        request=request,
    )
    error = RateLimitError(
        "Rate limit exceeded",
        response=response,
        body=None,
    )

    message = user_friendly_error_message(error)

    assert "rate-limited" in message
    assert "one minute" in message


def test_connection_error_has_helpful_message() -> None:
    request = httpx.Request(
        "POST",
        "https://api.groq.com/openai/v1/chat/completions",
    )
    error = APIConnectionError(request=request)

    message = user_friendly_error_message(error)

    assert "could not be reached" in message
    assert "internet connection" in message


def test_unknown_error_hides_internal_details() -> None:
    error = RuntimeError("secret internal information")

    message = user_friendly_error_message(error)

    assert "unexpected error" in message
    assert "secret internal information" not in message