# scripts/fetch_movies.py

import pandas as pd
import ast

def fetch_movies():
    # Load both datasets
    movies = pd.read_csv("Data/tmdb_5000_movies.csv")
    credits = pd.read_csv("Data/tmdb_5000_credits.csv")

    # Merge on 'title'
    merged = pd.merge(movies, credits, on="title")

    # Parse genres into a readable string
    def parse_genres(genre_str):
        try:
            genres = ast.literal_eval(genre_str)
            return ", ".join([g["name"] for g in genres])
        except:
            return "Unknown"

    # Extract director from crew
    def extract_director(crew_str):
        try:
            crew = ast.literal_eval(crew_str)
            for person in crew:
                if person["job"] == "Director":
                    return person["name"]
            return "Unknown"
        except:
            return "Unknown"

    # Create genre and director fields
    merged["genre"] = merged["genres"].apply(parse_genres)
    merged["director"] = merged["crew"].apply(extract_director)

    # Combine description
    merged["description"] = merged["overview"].fillna("") + ". Directed by " + merged["director"].fillna("Unknown")

    # Extract release year
    merged["year"] = pd.to_datetime(merged["release_date"], errors="coerce").dt.year

    # Final formatting
    df = merged.dropna(subset=["title", "genre", "description"])
    df = df[["title", "year", "genre", "description"]]

    # Save final movie dataset
    df.to_csv("data/movies.csv", index=False)
    print("✅ movies.csv saved with", len(df), "entries")

if __name__ == "__main__":
    fetch_movies()