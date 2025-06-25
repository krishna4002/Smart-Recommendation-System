import uuid
import os
from dotenv import load_dotenv
from backend.embeddings import embed_text
from pinecone import Pinecone, ServerlessSpec
from scripts.load_data import load_books  # ✅ Import here

# Load API key
load_dotenv()
api_key = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone
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

# ✅ Load books using the load_books function
df = load_books("Data/books.csv")
total = len(df)
batch = []
processed = 0
print(f"📚 Starting vectorization for {total} books...")

for idx, row in df.iterrows():
    try:
        doc_id = str(uuid.uuid4())
        combined_text = row["description"]  # already combined
        vector = [float(v) for v in embed_text(combined_text)]
        metadata = {
            "title": row["title"],
            "author": row["authors"],
            "description": row["description"],
            "type": "book"
        }
        batch.append((doc_id, vector, metadata))
        processed += 1

        if len(batch) >= 100:
            index.upsert(batch)
            print(f"✅ Indexed {processed}/{total} books... Remaining: {total - processed}")
            batch = []

    except Exception as e:
        print(f"⚠ Error at row {idx}: {e}")

if batch:
    index.upsert(batch)
    print(f"✅ Final batch indexed. Total: {processed}/{total}")

print("📚 Done indexing all books!")
