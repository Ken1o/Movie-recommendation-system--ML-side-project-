import pickle
import streamlit as st
from tmdbv3api import Movie, TMDb

movie = Movie()
tmdb = TMDb()
tmdb.api_key = "your api key for tmdb"

def get_recommendations(title):
    # getting the index through the title of the movie
    idx = movies[movies['title'] == title].index[0]
    
    # getting the data of the idx from the cosine similarity matrix as (idx, cosine_sim)
    sim_scores = list(enumerate(cosine_sim[idx]))

    # sorting the sim_scores with the highest cosine_sim scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # getting the 10 recommendation movies through slicing
    sim_scores = sim_scores[1:11]

    # getting index data of the 10 recommendation movies
    movie_indices = [i[0] for i in sim_scores]

    # getting the movie title from the index data
    images = []
    titles = []
    for i in movie_indices:
        id = movies['id'].iloc[i]
        details = movie.details(id)

        image_path = details['poster_path']
        if image_path:
            image_path = 'https://image.tmdb.org/t/p/w500' + image_path
        else:
            image_path = 'no_image.jpg'

        images.append(image_path)
        titles.append(details['title'])

    return images, titles

movies = pickle.load(open('movies.pickle', 'rb'))
cosine_sim = pickle.load(open('cosine_sim.pickle', 'rb'))

st.set_page_config(layout='wide')
st.header('Movie Recommendation System')

movie_list = movies['title'].values
title = st.selectbox('Choose a movie', movie_list)
if st.button('Recommend'):
    with st.spinner('Please wait...'):
        images, titles = get_recommendations(title)

        idx = 0
        for i in range(0, 2):
            cols = st.columns(5)
            for col in cols:
                col.image(images[idx])
                col.write(titles[idx])
                idx += 1