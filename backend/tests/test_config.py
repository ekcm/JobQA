from app.core.config import settings

def test_openai_api_key():
    assert settings.OPENAI_API_KEY is not None