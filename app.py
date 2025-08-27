import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gdown

# Access secrets safely with default None
API_KEY = st.secrets.get("API_KEY")
MOVIE_DICT_ID = st.secrets.get("MOVIE_DICT_ID")
SIMILARITY_ID = st.secrets.get("SIMILARITY_ID")

# Show debug info temporarily to verify secrets (remove/comment in production)
st.write("API_KEY:", "Set" if API_KEY else "Missing")
st.write("MOVIE_DICT_ID:", "Set" if MOVIE_DICT_ID else "Missing")
st.write("SIMILARITY_ID:", "Set" if SIMILARITY_ID else "Missing")

# Stop execution if secrets missing
if not all([API_KEY, MOVIE_DICT_ID, SIMILARITY_ID]):
    st.error("Missing required secrets. Please add API_KEY, MOVIE_DICT_ID, and SIMILARITY_ID in Streamlit Cloud Secrets.")
    st.stop()

def download_if_missing(file_id, output_name):
    if not os.path.exists(output_name):
        url = f"https://drive.google.com/uc?id={file_id}&export=download"
        gdown.download(url, output_name, quiet=False)

# Download files only if missing
download_if_missing(SIMILARITY_ID, "similarity.pkl")
download_if_missing(MOVIE_DICT_ID, "movie_dict.pkl")

@st.cache_data
def load_models():
    movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return pd.DataFrame(movies_dict), similarity

movies_list, similarity = load_models()

def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_url = "https://image.tmdb.org/t/p/w500" + data['poster_path'] if data.get('poster_path') else ""
    overview = data.get('overview', "No overview available.")
    rating = data.get('vote_average', "N/A")
    return poster_url, overview, rating

def recommend(movie_title):
    movie_index = movies_list[movies_list['title'] == movie_title].index[0]
    distances = similarity[movie_index]
    movies_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    recommended_ratings = []

    for i in movies_indices:
        movie_id = movies_list.iloc[i[0]].movie_id
        title = movies_list.iloc[i[0]].title
        poster, _, rating = fetch_movie_details(movie_id)

        recommended_movies.append(title)
        recommended_posters.append(poster)
        recommended_ratings.append(rating)

    return recommended_movies, recommended_posters, recommended_ratings

st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movies_list['title'].values
)

if st.button("Recommend"):
    names, posters, ratings = recommend(selected_movie_name)
    st.subheader("Top 5 Recommendations for You:")
    cols = st.columns(5)
    for idx, (col, name, poster, rating) in enumerate(zip(cols, names, posters, ratings)):
        with col:
            if poster:
                st.image(poster, width=200)
            st.markdown(f"<p style='text-align:center'><b>#{idx+1}: {name}</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center'>⭐ {rating}/10</p>", unsafe_allow_html=True)
