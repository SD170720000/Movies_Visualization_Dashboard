# scripts/scrapper.py

import pandas as pd
import ast
import os

# ---------- Parsing helpers ----------
def parse_json(x):
    try:
        return ast.literal_eval(x)
    except:
        return []

def parse_genres(entry):
    items = parse_json(entry)
    return [d["name"] for d in items] if isinstance(items, list) else []

def parse_keywords(entry):
    items = parse_json(entry)
    return [d["name"] for d in items] if isinstance(items, list) else []

def parse_countries(entry):
    items = parse_json(entry)
    return [d["name"] for d in items] if isinstance(items, list) else []


# ---------- Load datasets ----------
def load_data():
    print("[INFO] Loading TMDB datasets...")

    base_path = os.path.dirname(__file__)
    data_dir = os.path.join(base_path, "..", "data")

    movies = pd.read_csv(os.path.join(data_dir, "movies_metadata.csv"), low_memory=False)
    credits = pd.read_csv(os.path.join(data_dir, "credits.csv"))
    keywords = pd.read_csv(os.path.join(data_dir, "keywords.csv"))

    # ---------- Clean release dates ----------
    movies['release_date'] = pd.to_datetime(movies['release_date'], errors='coerce')
    movies = movies.dropna(subset=['release_date'])
    movies['year'] = movies['release_date'].dt.year
    movies = movies[(movies['year'] >= 1960) & (movies['year'] <= 2023)]

    # ---------- Clean IDs ----------
    # Convert 'id' to numeric, coerce errors (some IDs are dates or trash strings)
    movies['id'] = pd.to_numeric(movies['id'], errors='coerce')
    movies = movies.dropna(subset=['id'])
    movies['id'] = movies['id'].astype(int)

    # Clean numeric columns for Panel 2
    movies['revenue'] = pd.to_numeric(movies['revenue'], errors='coerce')
    movies['vote_average'] = pd.to_numeric(movies['vote_average'], errors='coerce')
    
    # Optional: Fill NaNs or drop them? 
    # For now, let's keep them as NaN so they are ignored in mean() or dropped later
    
    credits['id'] = pd.to_numeric(credits['id'], errors='coerce')
    credits = credits.dropna(subset=['id'])
    credits['id'] = credits['id'].astype(int)

    # ---------- Parse lists ----------
    movies['genres_list'] = movies['genres'].apply(parse_genres)
    movies['countries'] = movies['production_countries'].apply(parse_countries)

    keywords['keywords_list'] = keywords['keywords'].apply(parse_keywords)
    movies['keywords_list'] = keywords['keywords_list']

    # ---------- Parse credits ----------
    credits['cast'] = credits['cast'].apply(parse_json)
    credits['crew'] = credits['crew'].apply(parse_json)

    def get_top_actor(cast_list):
        return cast_list[0]['name'] if cast_list else None

    def get_director(crew_list):
        for item in crew_list:
            if item.get('job') == 'Director':
                return item.get('name')
        return None

    credits['top_actor'] = credits['cast'].apply(get_top_actor)
    credits['director'] = credits['crew'].apply(get_director)

    # ---------- Merge ----------
    movies = movies.merge(
        credits[['id', 'top_actor', 'director']],
        on='id',
        how='left'
    )

    print("[INFO] Datasets loaded successfully.")
    return movies
