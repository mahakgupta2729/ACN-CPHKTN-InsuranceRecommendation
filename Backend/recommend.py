import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2023-12-01-preview",
    azure_endpoint=os.getenv("OPENAI_ENDPOINT")
)

def generate_recommendation(age,conditions, extracted_text, plans):
    plans_text = "\n\n".join([str(plan) for plan in plans])

    prompt = (
        f"You are an expert insurance assistant. Based on the user's conditions and age: {conditions},{age}, "
        f"and medical history extracted from the documents: {extracted_text}, "
        f"suggest the most suitable plans from the following list:\n\n"
        f"{plans_text}\n\n"
        "Return a detailed explanation of why you recommend those plans."
    )

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_CHAT_DEPLOYMENT"),  # Your deployed model name (e.g., "gpt-35-turbo")
        messages=[
            {"role": "system", "content": "You are a helpful insurance assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
