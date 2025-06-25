# backend/embeddings.py
from sentence_transformers import SentenceTransformer

# Load embedding model only once
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text):
    return model.encode(text)
