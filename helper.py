import requests
import os
import pandas as pd
import pickle
from dotenv import load_dotenv



# ── Load data ────────────────────────────────────────────────────────────────
load_dotenv()
api_key = os.getenv('TMDB_API_KEY')

movies_list = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_list)


# ── Helpers ──────────────────────────────────────────────────────────────────
def fetch_poster(movie_id):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US",
            timeout=10
        )
        data = response.json()
        
        if data.get('poster_path'):
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except Exception:
        pass
    return "https://via.placeholder.com/500x750?text=No+Poster"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommeded_movies = []
    recommeded_movies_poster = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommeded_movies.append(movies.iloc[i[0]].title)
        
        # fetch poster from API
        recommeded_movies_poster.append(fetch_poster(movie_id))

    return recommeded_movies, recommeded_movies_poster