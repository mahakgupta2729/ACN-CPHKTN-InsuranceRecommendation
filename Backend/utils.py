import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_ENDPOINT")

def generate_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model=os.getenv("OPENAI_EMBEDDING_DEPLOYMENT")
    )
    return response['data'][0]['embedding']
