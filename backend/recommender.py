# backend/recommender.py

import os
import numpy as np
from dotenv import load_dotenv
from backend.embeddings import embed_text
from backend.vector_store import index
from backend.user_profile import build_user_vector
from openai import OpenAI

# Load environment variables
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def personalized_search(query, user_input_profile=None, content_type="book"):
    query_vec = embed_text(query)

    if user_input_profile:
        user_vec = embed_text(user_input_profile)
        final_vector = np.mean([query_vec, user_vec], axis=0)
    else:
        final_vector = query_vec  # Only query used if no user input provided

    final_vector = [float(v) for v in final_vector]  # Ensure float list

    results = index.query(
        vector=final_vector,
        top_k=10,
        include_metadata=True,
        filter={"type": content_type}
    )
    return results["matches"]

def rerank_results(query, items):
    prompt = f"User asked: \"{query}\"\nOptions: {[item['metadata']['title'] + ': ' + item['metadata']['description'] for item in items]}\nRank by relevance."

    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct:free",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip().split("\n")