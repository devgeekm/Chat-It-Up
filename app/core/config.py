import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    AI_SERVICE_ENDPOINT = os.getenv('AI_SERVICE_ENDPOINT')
    AI_SERVICE_KEY = os.getenv('AI_SERVICE_KEY')
    AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
    AZURE_CONTENT_SAFETY_KEY = os.getenv('AZURE_CONTENT_SAFETY_KEY')
    AZURE_GPT_ENDPOINT = os.getenv('AZURE_GPT_ENDPOINT')
    AZURE_GPT_API_KEY = os.getenv('AZURE_GPT_API_KEY')
    AZURE_TRANSLATOR_KEY = os.getenv('AZURE_TRANSLATOR_KEY')
    AZURE_TRANSLATOR_ENDPOINT = os.getenv('AZURE_TRANSLATOR_ENDPOINT')
    AZURE_TRANSLATOR_LOCATION = os.getenv('AZURE_TRANSLATOR_LOCATION')
    AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')