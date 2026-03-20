from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

from dotenv import load_dotenv
import os

load_dotenv()  # 🔥 THIS IS REQUIRED

API_KEY = os.getenv("MISTRAL_API_KEY")

if not API_KEY:
    raise ValueError("API key not found!")

client = MistralClient(api_key=API_KEY)


def generate_answer(query, context):
    context_text = "\n".join(context)

    prompt = f"""
You are an intelligent business analyst.

Use the context to answer the question with reasoning.

Context:
{context_text}

Question:
{query}

Give a clear answer with explanation.
"""

    response = client.chat(
        model="mistral-small",
        messages=[
            ChatMessage(role="user", content=prompt)
        ]
    )

    return response.choices[0].message.content
    
def generate_summary(text):
    prompt = f"""
You are an expert analyst.

Summarize the following document clearly.

Focus on:
- Key points
- Important insights
- Risks (if any)

Document:
{text[:3000]}   # limit for safety

Summary:
"""

    response = client.chat(
        model="mistral-small",
        messages=[
            ChatMessage(role="user", content=prompt)
        ]
    )

    return response.choices[0].message.content