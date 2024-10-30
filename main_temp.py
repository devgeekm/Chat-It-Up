from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
from typing import List, Dict

# Load environment variables
load_dotenv()
azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
azure_oai_key = os.getenv("AZURE_OAI_KEY")
azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")
azure_oai_version = os.getenv("AZURE_OAI_VERSION")

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=azure_oai_endpoint,
    api_key=azure_oai_key,
    api_version=azure_oai_version
)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Adjust to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable to store conversation history (only works for single instance)
conversation_history = [{"role": "system", "content": "You are an AI assistant that helps people find information."}]

class ChatRequest( BaseModel ):
    message: str

@app.post('/chat')
async def chat_with_openai( request: ChatRequest ):
    try:
        # Append the new user message to the conversation history
        conversation_history.append({"role": "user", "content": request.message})

        # Send the conversation history to OpenAI
        response = client.chat.completions.create(
            model=azure_oai_deployment,
            max_tokens=100,
            temperature=0.7,
            messages=conversation_history
        )

        # Get the assistant's response
        chat_response = response.choices[0].message.content

        # Append the assistant's response to the conversation history
        conversation_history.append({"role": "assistant", "content": chat_response})

        return {'response': chat_response}

    except Exception as e:
        raise HTTPException( status_code=500, detail=str(e) )