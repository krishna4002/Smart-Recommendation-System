# 📚🎬🎵 AI-Powered Smart Recommendation System

An intelligent multi-domain **Recommendation System for Books, Movies, and Songs**, combining the power of **LLMs (Mistral via OpenRouter)** with **vector similarity (Pinecone)**. This system understands user intent, personal preferences, and content metadata to provide **highly relevant recommendations** in real-time.

---

## Key Features

- **Supports 3 Domains in 1 App**: Books, Movies, and Songs  
- **LLM-Powered Search Understanding**: Uses Mistral to refine vague queries  
- **Semantic Search + Personalization**: Combines query with user interest vectors  
- **LLM-based Reranking**: Ensures most relevant results show first  
- **Interactive Streamlit UI**: Clean sidebar controls and dynamic content display  
- **Optional User Input**: Works with or without user profile  
- **Embeddings via SentenceTransformer**  
- **Vector Indexing via Pinecone**  
- **Progress batching for large dataset indexing**

---

## Why This Project Matters

This project is **resume-worthy** and valuable in real-world AI systems because:

- It simulates what companies like Netflix, Spotify, or Goodreads use.
- You combine **retrieval (search)** and **generation (LLM)** for smarter UX.
- You allow **personalization without mandatory login**, improving usability.
- You work with **real datasets from Kaggle**, making it scalable and modifiable.


---

## How It Works (Behind The Scenes)

```
USER QUERY (e.g., "biography of tech innovators")
       ⬇
LLM (Mistral) refines the query → "Biographies of famous tech entrepreneurs"
       ⬇
Embedding → Vector (via SentenceTransformer)
       ⬇
Combined with User Preference vector (optional)
       ⬇
Pinecone → Finds Top-K Similar Content
       ⬇
LLM Reranking → Prioritizes most relevant results
       ⬇
Streamlit UI → Shows Personalized & Accurate Recommendations
```

---

## Project Structure

```
recommendation-system/
│
├── app/
│   └── main.py                   # Streamlit UI with sidebar + LLM
│
├── backend/
│   ├── embeddings.py            # Embedding generation
│   ├── llm_query.py             # Mistral query refinement via OpenRouter
│   ├── recommender.py           # Search + rerank logic
│   ├── user_profile.py          # Converts user input to vector
│   └── vector_store.py          # Pinecone connector
│
├── scripts/
│   ├── fetch_books.py           # Load/clean book data
│   ├── fetch_movies.py          # Load/clean movie data
│   ├── fetch_songs.py           # Merge lyrics and metadata
│   ├── index_books.py           # Index book embeddings
│   ├── index_movies.py          # Index movie embeddings
│   └── index_songs.py           # Index song embeddings
│
├── data/
│   ├── books.csv
│   ├── movies.csv
│   └── songs.csv
│
├── .env                         # API keys (OpenRouter & Pinecone)
└── requirements.txt             # All required packages
```

---

## Installation and Setup

### 1. Clone the repository
```bash
git clone https://github.com/krishna4002/Smart-Recommendation-System.git
cd Smart-Recommendation-System
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your .env file
```env
OPENROUTER_API_KEY=your_openrouter_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENV=your_pinecone_environment
```

### 4. Download and place datasets
Place your cleaned:
- `books.csv`
- `movies.csv`
- `songs.csv`
  
into the `Data/` folder. (Datasets from Kaggle recommended)

### 5. Index your data
```bash
python scripts/index_books.py
python scripts/index_movies.py
python scripts/index_songs.py
```

### 6. Run the application
```bash
streamlit run app/main.py
```

---

## UI Controls (in Sidebar)

- **Select Content Type**: Choose between Book, Movie, or Song
- **(Optional) User Interests**: Add "I love sci-fi and acoustic music"
- **Enter Search Prompt**: e.g. "Inspiring biographies about innovation"

---

## Sample Prompts

Here are some great inputs to test:

### Book
- "Books like Harry Potter with magical worlds"
- "Motivational books for entrepreneurs"
- "Science fiction novels with strong female leads"

### Movie
- "Romantic comedies from the 90s"
- "Sci-fi thrillers about artificial intelligence"
- "Movies like Inception or Interstellar"

### Song
- "Relaxing acoustic songs"
- "Energetic pop hits for workouts"
- "Classical music for concentration"

---

## Understanding the User Feature

- If the user provides **interests** (optional), we embed them into a vector.
- That vector is combined with the query vector → Better personalization.
- If not provided, only the query vector is used.

So it’s flexible and user-friendly for both guests and regular users.

---

## Data Privacy

- No user login required.
- No storage of personal data or queries.
- Works fully offline after data/indexing.

---

## Future Enhancements

- Add support for image/video content.
- Integrate feedback loop for improving recommendations.
- Allow saving favorites, exporting results.
- Add genre-based filters.

---

## Author

Built by **[Krishnagopal Jay]**  
Powered by *OpenRouter, **Mistral, **Pinecone, and **Streamlit*

> “Not just search — it’s intelligent, personal, and scalable.”
