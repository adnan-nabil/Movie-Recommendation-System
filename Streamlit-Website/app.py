import streamlit as st
import pickle
import pandas as pd
import requests
import numpy as np



# streamlit run app.py


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies_df = pd.DataFrame(movies_dict)




def poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=ce96ffadb56092eaec7ab333967b505b".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommendation(movie):
    movie_index = movies_df[movies_df["title"] == movie].index[0]
    distances = similarity[movie_index] 
    recommended_movie_index = sorted(list(enumerate(distances)), reverse=True, key = lambda x: x[1])[1:6]
    
    recommended_movie_title = []
    recommended_movie_posters = []
    
    for i in recommended_movie_index:
        movie_id = movies_df.iloc[i[0]].movie_id
        recommended_movie_posters.append(poster(movie_id))
        recommended_movie_title.append(movies_df.iloc[i[0]].title)
        
    return recommended_movie_title, recommended_movie_posters


st.title("Movie Recommender App")
selected_movie_name = st.selectbox("which movie you have seen last", movies_df['title'].values)


if st.button("🎬 Show Recommendation"):
        rm_title, rm_poster = recommendation(selected_movie_name)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(rm_title[0])
            st.image(rm_poster[0])
        with col2:
            st.text(rm_title[1])
            st.image(rm_poster[1])
        with col3:
            st.text(rm_title[2])
            st.image(rm_poster[2])
        with col4:
            st.text(rm_title[3])
            st.image(rm_poster[3])
        with col5:
            st.text(rm_title[4])
            st.image(rm_poster[4])
 