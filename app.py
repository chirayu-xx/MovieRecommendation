import streamlit as st
import pickle
import requests

# load the movie list and similarity matrix
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# function to fetch movie details from TMDB API
def fetch_movie_details(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    return data

# function to fetch movie cast from TMDB API
def fetch_movie_cast(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}/credits?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    return data

# function to recommend similar movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    for i in distances[1:6]:
        # fetch the movie details
        movie_id = movies.iloc[i[0]].movie_id
        movie_details = fetch_movie_details(movie_id)
        recommended_movies.append({
            'title': movie_details['title'],
            'poster_path': "https://image.tmdb.org/t/p/w500/" + movie_details['poster_path'],
            'overview': movie_details['overview'],
            'vote_count': movie_details['vote_count'],
            'vote_average': movie_details['vote_average']
        })

    return recommended_movies

# streamlit app
st.header('Movie Recommender System')

# movie selection dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# show recommendation button
hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''

st.markdown(hide_img_fs, unsafe_allow_html=True)
if st.button('Show Recommendation'):
    # display selected movie details
    selected_movie_details = fetch_movie_details(movies.iloc[movies[movies['title'] == selected_movie].index[0]].movie_id)
    st.subheader(f"{selected_movie_details['title']}")
    st.image("https://image.tmdb.org/t/p/w500/" + selected_movie_details['poster_path'], width=300)
    st.write(f"{selected_movie_details['overview']}")
    st.write(f"Rating: {selected_movie_details['vote_average']}")
    st.write(f"Vote Count: {selected_movie_details['vote_count']}")
    
    # display main cast of the selected movie
    cast = fetch_movie_cast(movies.iloc[movies[movies['title'] == selected_movie].index[0]].movie_id)
    st.subheader("Main Cast")
    for i in range(min(5, len(cast['cast']))):
        st.write(f"{cast['cast'][i]['name']} as {cast['cast'][i]['character']}")
    
    # display recommended movies
    recommended_movies = recommend(selected_movie)
    st.subheader("Recommended Movies")
    for i, movie in enumerate(recommended_movies):
        st.subheader(f"{i+1}. {movie['title']}")
        st.image(movie['poster_path'], width=200)
        st.write(f"{movie['overview']}")
        st.write(f"Rating: {movie['vote_average']}")
        st.write(f"Vote Count: {movie['vote_count']}")



    # Add spacing between recommendation and footer
    st.markdown('***')
    st.markdown('***')
    st.markdown("<h6 style='text-align: center; color: gray;'>Made with ❤️ by Chirayu</h6>", unsafe_allow_html=True)
