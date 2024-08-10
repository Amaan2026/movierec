import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']
movies_dict = pickle.load(open('movie.pkl','rb'))
similar = pickle.load(open('similar.pkl','rb'))
movie = pd.DataFrame(movies_dict)
st.title('Movie Recommender System')
option = st.selectbox('How would you like to be connected ?',
movie['title'].values)

#recommend function
def recommend(film):
    film_index = movie[movie['title'] == film].index[0]
    similarity = similar[film_index]
    top_similarities = sorted(list(enumerate(similarity)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    for i in top_similarities:
        movie_id = movie.iloc[i[0]].id
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies.append(movie.iloc[i[0]].title)
    return recommended_movies,recommended_movies_poster



if st.button('Recommend'):
    name, poster = recommend(option)


    cols = st.columns(5)


    for i in range(5):
        with cols[i]:
            st.text(name[i])
            st.image(poster[i])

