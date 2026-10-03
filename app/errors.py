from groq import (
    APIConnectionError,
    AuthenticationError,
    BadRequestError,
    RateLimitError,
)


def user_friendly_error_message(error: Exception) -> str:
    if isinstance(error, RateLimitError):
        return (
            "The free AI service is temporarily rate-limited. "
            "Please wait approximately one minute and try again."
        )

    if isinstance(error, AuthenticationError):
        return (
            "The AI service could not authenticate. "
            "Check that GROQ_API_KEY is configured correctly."
        )

    if isinstance(error, APIConnectionError):
        return (
            "The AI service could not be reached. "
            "Check your internet connection and try again."
        )

    if isinstance(error, BadRequestError):
        return (
            "The AI service could not process this request. "
            "Try a shorter or more clearly formatted job description."
        )

    if isinstance(error, ValueError):
        return str(error)

    return (
        "An unexpected error occurred while analyzing the job. "
        "Please try again."
    )