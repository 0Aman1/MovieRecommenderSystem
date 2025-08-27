import streamlit as st
import pickle
import pandas as pd
import requests

# 🔑 Your TMDb API key
API_KEY = "479916d10972f80eeeee140a1ad3b701"

# Function to fetch poster, overview, and rating from TMDb
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    data = response.json()

    poster_url = "https://image.tmdb.org/t/p/w500" + data['poster_path'] if data.get('poster_path') else ""
    overview = data.get('overview', "No overview available.")
    rating = data.get('vote_average', "N/A")
    return poster_url, overview, rating


# Recommendation function
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


# ----------------- Streamlit UI -----------------
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommender System")

# Load movies and similarity data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies_list = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Dropdown to select movie
selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movies_list['title'].values
)

# Show recommendations
if st.button("Recommend"):
    names, posters, ratings = recommend(selected_movie_name)

    st.subheader("Top 5 Recommendations for You:")

    # Layout: show 5 recommendations in a row
    cols = st.columns(5)
    for idx, (col, name, poster, rating) in enumerate(zip(cols, names, posters, ratings)):
        with col:
            if poster:  # show poster if available
                st.image(poster, width=200)
            st.markdown(f"<p style='text-align:center'><b>#{idx+1}: {name}</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center'>⭐ {rating}/10</p>", unsafe_allow_html=True)
