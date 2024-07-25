import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=c169ff6de79e1c50c9130cf850bc8d0e&language=en-US'
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path', '')
    return "https://image.tmdb.org/t/p/w500" + poster_path if poster_path else None

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []
    for i in movies_list:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Load data
movies_dict = pickle.load(open('model/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

# Streamlit UI
st.set_page_config(page_title='Movie Recommendation System', page_icon=':movie_camera:', layout='wide')

# Custom CSS
st.markdown("""
    <style>
    body {
        background-color: #f0f2f6;
        color: #333;
    }
    .header {
        text-align: center;
        padding: 20px;
        background-color: #1f77b4;
        color: white;
        border-radius: 10px;
    }
    .recommendation-title {
        font-size: 1.2em;
        font-weight: bold;
        color: #1f77b4;
    }
    .recommendation-box {
        padding: 20px;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .recommendation-box img {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header"><h1>Movie Recommendation System</h1></div>', unsafe_allow_html=True)

selected_movie_name = st.selectbox(
    'Select a movie from the dropdown',
    movies['title'].values
)

if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            if i < len(names):
                col.markdown(f'<div class="recommendation-box"><h2 class="recommendation-title">{names[i]}</h2>', unsafe_allow_html=True)
                if posters[i]:
                    col.image(posters[i])
                col.markdown('</div>', unsafe_allow_html=True)
