from openai import AzureOpenAI
import os
from dotenv import load_dotenv

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

# Global conversation history
conversation_history = [{"role": "system", "content": "You are an AI assistant that helps people find information."}]

async def chat_with_openai( message: str ) -> str:
    # Append the new user message to the conversation history
    conversation_history.append({"role": "user", "content": message})

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

    return {chat_response}
