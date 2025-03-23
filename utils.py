import os


def get_openai_api_key() -> str:
    """Get OpenAI API key"""
    return os.getenv("OPENAI_API_KEY", "")
