import streamlit as st
from helper import movies, recommend
import time



# ── Page config (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="FlickFind – Movie Recommender",
    page_icon="🎬",
    layout="wide"
)


# ── Load CSS ────────────────────────────────────────────────────────────────
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("css/styles.css")


# ── UI ───────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">🎬 FlickFind</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Discover movies you\'ll love — powered by AI</div>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# Search box
col_left, col_center, col_right = st.columns([1, 2, 1])
with col_center:
    selected_movie_name = st.selectbox(
        '🔍 Search for a movie',
        movies['title'].values
    )

# Recommend button
_, btn_col, _ = st.columns([2, 1, 2])
with btn_col:
    search = st.button('✨ Get Recommendations')

# Results
if search:
    loading_text = st.empty()
    loading_text.markdown(
        '<p style="text-align:center; font-weight:700; font-size:1.1rem; color:#ffd200;">Finding movies you\'ll love...</p>', 
        unsafe_allow_html=True
    )
    progress_bar = st.progress(0)
    
    for percent in range(30):
        time.sleep(0.005)
        progress_bar.progress(percent + 1)
    
    names, posters = recommend(selected_movie_name)
    
    for percent in range(30, 100):
        time.sleep(0.005)
        progress_bar.progress(percent + 1)
    
    loading_text.empty()
    progress_bar.empty()

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-heading">Because you liked &nbsp;<span style="color:#fff">'
        f'"{selected_movie_name}"</span></div>',
        unsafe_allow_html=True
    )

    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.markdown(f"""
            <div class="movie-card">
                <img src="{poster}" alt="{name}">
                <div class="movie-title">{name}</div>
            </div>
            """, unsafe_allow_html=True)


# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center; color:#555; font-size:0.8rem;">'
    'Built with ❤️ using Streamlit & TMDB API</p>',
    unsafe_allow_html=True
)