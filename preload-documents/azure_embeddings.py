import os
from openai import AzureOpenAI
from openai.types.create_embedding_response import CreateEmbeddingResponse
from dotenv import load_dotenv
load_dotenv()


def generate_embeddings(text: str) -> CreateEmbeddingResponse: 
  client = AzureOpenAI(
    api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version = os.getenv("AZURE_OPENAI_VERSION"),
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT") 
  )

  return client.embeddings.create(
      input = text,
      model= os.getenv("AZURE_OPENAI_MODEL")
  )

