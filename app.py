import pickle

import streamlit as st
import pandas as pd
import requests

@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=7112b4d5ba06bc6d9300bb5fa1c068fb&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except:
        return "https://via.placeholder.com/500x750?text=No+Image"



def recommend(movie):
    movie_index = movies[movies.title == movie].index[0]
    distances = similarity[movie_index]
    # sorting the enumerated tuple in descending order, on the basis of similarity.
    re_movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]


    # printing the 5 recommended movie list.
    recommended_movie = []
    recommended_movie_posters = []
    for i in re_movie_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movie.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie, recommended_movie_posters


st.title('Movie Recommender System')

movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open('Similarity.pkl', 'rb'))


Selected_Movie = st.selectbox("What's your favorite movie?", movies['title'].values)

if st.button("Recommend"):
    names, poster = recommend(Selected_Movie)
    col1, col2, col3, col4, col5 = st.columns(5)


    with col1:
        st.text(names[0])
        st.image(poster[0])

    with col2:
        st.text(names[1])
        st.image(poster[1])

    with col3:
        st.text(names[2])
        st.image(poster[2])

    with col4:
        st.text(names[3])
        st.image(poster[3])

    with col5:
        st.text(names[4])
        st.image(poster[4])


