# backend/llm_query.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY is not set in the environment.")

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

def parse_query_with_mistral(user_query: str) -> str:
    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct:free",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a smart assistant that rewrites user prompts to improve personalized recommendations "
                    "for books, movies, and songs. Extract key genres, preferences, or mood if possible. Make it short, natural, and optimized for semantic search."
                )
            },
            {
                "role": "user",
                "content": user_query
            }
        ]
    )

    return response.choices[0].message.content.strip()