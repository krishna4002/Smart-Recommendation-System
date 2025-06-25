import uuid
import os
import pandas as pd
from backend.embeddings import embed_text
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=api_key)
index_name = "recommendation-system"

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-west-2")
    )

index = pc.Index(index_name)

df = pd.read_csv("data/movies.csv", low_memory=False)
df = df.dropna(subset=["title", "description"])

total = len(df)
batch = []
processed = 0
print(f"🎬 Starting vectorization for {total} movies...")

for idx, row in df.iterrows():
    try:
        doc_id = str(uuid.uuid4())
        combined_text = f"{row['title']} ({int(row['year']) if not pd.isnull(row['year']) else 'unknown year'}). {row['description']}"
        vector = [float(v) for v in embed_text(combined_text)]
        metadata = {
            "title": row["title"],
            "author": str(row["year"]) if not pd.isnull(row["year"]) else "Unknown",
            "description": row["description"],
            "type": "movie"
        }
        batch.append((doc_id, vector, metadata))
        processed += 1

        if len(batch) >= 100:
            index.upsert(batch)
            print(f"✅ Indexed {processed}/{total} movies... Remaining: {total - processed}")
            batch = []

    except Exception as e:
        print(f"⚠ Error at row {idx}: {e}")

if batch:
    index.upsert(batch)
    print(f"✅ Final batch indexed. Total: {processed}/{total}")

print("🎬 Done indexing all movies!")