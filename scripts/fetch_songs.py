# scripts/fetch_songs.py

import pandas as pd
import os

def fetch_songs():
    # Load song dataset
    base_path = "Data"  # Adjust if needed
    df = pd.read_csv(os.path.join(base_path, "data.csv"))

    # Rename and clean relevant columns
    df = df.rename(columns={
        "name": "track_name",
        "artists": "artist"
    })

    # Create genre column (not present in this CSV)
    df["genre"] = "Unknown"

    # Filter missing key fields
    df = df.dropna(subset=["track_name", "artist", "year"])

    # Format description
    df["description"] = df.apply(
        lambda row: f"A {row['genre']} song by {row['artist']} released in {int(row['year'])}.",
        axis=1
    )

    # Select final columns
    df = df[["track_name", "artist", "genre", "description"]]

    # Save final CSV
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/songs.csv", index=False)
    print(f"✅ songs.csv saved with {len(df)} entries")

if __name__ == "__main__":
    fetch_songs()