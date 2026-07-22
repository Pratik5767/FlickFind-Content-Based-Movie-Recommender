# 🎬 FlickFind — Content-Based Movie Recommender

FlickFind is a content-based movie recommendation web app that suggests similar movies based on a movie you already like — using overview text, genres, keywords, cast, and director metadata rather than user ratings or watch history.

Pick any movie from the dropdown, hit **Get Recommendations**, and FlickFind returns the 5 most similar movies complete with posters fetched live from TMDB.

---

## ✨ Features

- **Content-based recommendations** — similarity is computed from each movie's genres, plot overview, keywords, top cast, and director, not from collaborative user data.
- **Instant search** — searchable dropdown of 4,800+ movies from the TMDB 5000 dataset.
- **Live poster fetching** — posters are pulled in real time from The Movie Database (TMDB) API, with a placeholder fallback if a poster isn't available.
- **Custom dark UI** — a fully custom-styled Streamlit interface (gradient background, animated progress bar, hover-effect movie cards) instead of default Streamlit styling.
- **Precomputed similarity model** — the vectorization and similarity matrix are precomputed and serialized (`.pkl`), so recommendations are returned instantly without recomputing on every request.

---

## 🖥️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend / App | [Streamlit](https://streamlit.io/) |
| Data processing | Pandas, NumPy |
| NLP / Vectorization | scikit-learn (`CountVectorizer`), NLTK (`PorterStemmer`) |
| Similarity | Cosine Similarity (scikit-learn) |
| External data | [TMDB API](https://www.themoviedb.org/documentation/api) (poster images) |
| Dataset | [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) |
| Model storage | Python `pickle` |

---

## 🧠 How It Works

The recommendation logic is built in the Jupyter notebook (`notebook/movie_recommender_system.ipynb`) and then exported for the live app to use:

1. **Merge datasets** — `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` are merged on `title` to combine movie metadata with cast/crew data.
2. **Select relevant columns** — keeps only `movie_id`, `title`, `overview`, `genres`, `keywords`, `cast`, `crew`.
3. **Clean the data** — drops rows with missing values and checks for duplicates.
4. **Parse nested JSON-like fields** — `genres` and `keywords` arrive as stringified lists of dicts (e.g. `{"id": 28, "name": "Action"}`) and are parsed with `ast.literal_eval` into plain lists of names.
5. **Extract cast & crew**
   - Keeps only the **top 3 billed actors** from `cast`.
   - Extracts only the **Director** from `crew`.
6. **Normalize tokens** — removes spaces within multi-word names (e.g. `"Science Fiction"` → `"ScienceFiction"`, `"Sam Worthington"` → `"SamWorthington"`) so they're treated as single, distinct tokens during vectorization.
7. **Build a unified `tags` field** — concatenates `overview` + `genres` + `keywords` + `cast` + `crew` into one text blob per movie.
8. **Stem the text** — applies NLTK's `PorterStemmer` to reduce words to their root form (e.g. "loved", "loving" → "love"), then lowercases everything.
9. **Vectorize** — converts the `tags` text into numerical vectors using `CountVectorizer` (bag-of-words, top 5,000 features, English stop words removed).
10. **Compute similarity** — calculates pairwise **cosine similarity** across all movie vectors to build a similarity matrix.
11. **Serialize the model** — saves the processed DataFrame (`movies.pkl`) and similarity matrix (`similarity.pkl`) so the Streamlit app can load them instantly without repeating this pipeline.

At request time, `helper.py` simply looks up the selected movie's index, pulls its row from the similarity matrix, sorts by similarity score, and returns the top 5 closest matches (excluding the movie itself) — then fetches each poster live from TMDB.

---

## 📁 Project Structure

```
FlickFind-Content-Based-Movie-Recommender/
│
├── app.py                          # Streamlit app entry point (UI + interactions)
├── helper.py                       # Recommendation logic + TMDB poster fetching
├── movies.pkl                      # Serialized, preprocessed movies DataFrame
├── similarity.pkl                  # Serialized cosine similarity matrix
├── requirements.txt                # Python dependencies
│
├── css/
│   └── styles.css                  # Custom dark-themed UI styling
│
├── dataset/
│   ├── tmdb_5000_movies.csv        # Raw TMDB movies metadata
│   └── tmdb_5000_credits.csv       # Raw TMDB cast & crew data
│
└── notebook/
    └── movie_recommender_system.ipynb   # Full data preprocessing & model-building pipeline
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- A free [TMDB API key](https://www.themoviedb.org/settings/api) (required for fetching movie posters)

### 1. Clone the repository

```bash
git clone https://github.com/Pratik5767/FlickFind-Content-Based-Movie-Recommender.git
cd FlickFind-Content-Based-Movie-Recommender
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your TMDB API key

Create a `.env` file in the project root and add:

```
TMDB_API_KEY=your_tmdb_api_key_here
```

`helper.py` loads this automatically via `python-dotenv`.

### 5. Run the app

```bash
streamlit run app.py
```

The app will open in your browser, typically at `http://localhost:8501`.

---

## 🎯 Usage

1. Select a movie from the searchable dropdown.
2. Click **✨ Get Recommendations**.
3. FlickFind displays the top 5 most similar movies, each with its poster fetched live from TMDB.

---

## 🔮 Possible Improvements

- Add collaborative filtering or a hybrid recommender combining content-based and rating-based signals.
- Cache TMDB poster responses to reduce redundant API calls.
- Add movie detail pages (synopsis, ratings, cast) on click.
- Deploy the app (e.g. Streamlit Community Cloud) with the API key stored as a secret.
- Expand the dataset beyond the static TMDB 5000 snapshot for broader coverage.

---

## 📊 Dataset Credit

This project uses the **TMDB 5000 Movie Dataset**, sourced from [The Movie Database (TMDB)](https://www.themoviedb.org/), commonly distributed via Kaggle.

---

## 🙌 Acknowledgements

- [TMDB API](https://www.themoviedb.org/documentation/api) for movie metadata and poster images.
- [Streamlit](https://streamlit.io/) for making rapid, Python-only web app development possible.

---

## 👤 Author

**Pratik Salunkhe**
GitHub: [@Pratik5767](https://github.com/Pratik5767)