import openai
from .config import settings

openai.api_key = settings.OPENAI_API_KEY

