import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.textanalytics import TextAnalyticsClient
from openai import AzureOpenAI

load_dotenv()

def initialize_azure_clients():
    whisper_client = AzureOpenAI(
        azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
        api_key=os.getenv('AZURE_OPENAI_API_KEY'),
        api_version="2024-06-01"
    )
    ai_client = TextAnalyticsClient(
        endpoint=os.getenv('AI_SERVICE_ENDPOINT'),
        credential=AzureKeyCredential(os.getenv('AI_SERVICE_KEY'))
    )
    content_safety_client = ContentSafetyClient(
        endpoint=os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT'),
        credential=AzureKeyCredential(os.getenv('AZURE_CONTENT_SAFETY_KEY'))
    )
    gpt_client = AzureOpenAI(
        azure_endpoint=os.getenv('AZURE_GPT_ENDPOINT'),
        api_key=os.getenv('AZURE_GPT_API_KEY'),
        api_version="2023-09-15-preview"
    )
    return {
        'whisper': whisper_client,
        'ai': ai_client,
        'content_safety': content_safety_client,
        'gpt': gpt_client
    }