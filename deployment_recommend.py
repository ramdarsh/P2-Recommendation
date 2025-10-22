import streamlit as st
import pickle
import requests


st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/IMDB_Logo_2016.svg/575px-IMDB_Logo_2016.svg.png')

background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://www.insightpublications.com.au/wp-content/uploads/Responding-to-film-Blog-Header_FINAL_19Apr2018.jpg");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""

st.markdown(background_image, unsafe_allow_html=True)

movies = pickle.load(open("movies_list.pkl",'rb'))
similarity = pickle.load(open("similarity.pkl",'rb'))

movies_list = movies['Movie Title'].values

st.header("MOVIE RECOMMENDER SYSTEM")
selectvalue=st.selectbox('Select movie from dropdown', movies_list)

def fetch_poster(movie_list):
    # Make a request to the OMDb API
    response = requests.get('https://www.omdbapi.com/?t={}&apikey=3705bfa'.format(movie_list))
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON data from the response
        data = response.json()
        
        # Check if the 'Poster' key exists in the response
        if 'Poster' in data:
            return data['Poster']
        else:
            return "No poster available"
    else:
        return "Error fetching data"


def recommend(movie):
    index = movies[movies['Movie Title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movies = []

    for i in distance[1:6]:
        movie_entry = movies.iloc[i[0]].to_dict()
        recommend_movies.append(movie_entry)

    return recommend_movies

if st.button("Show Recommendations"):
    recommend_result = recommend(selectvalue)
    
    # Check if there are recommendations
    if recommend_result:
        # Unpack the first recommendation
        first_recommendation = recommend_result[0]
        first_movie_name = first_recommendation['Movie Title']
        first_poster = fetch_poster(first_movie_name)

        # Display the first recommendation
        st.header(first_movie_name)
        st.image(first_poster)

        # Display additional recommendations if available
        st.subheader("Additional Recommendations:")
        
        # Create a horizontal layout for posters and movie titles
        columns = st.columns(5)

        # Display posters and movie titles horizontally
        for recommendation, column in zip(recommend_result[1:6], columns):
            column.text(recommendation['Movie Title'])
            column.image(fetch_poster(recommendation['Movie Title']))

    else:
        st.warning("No recommendations available.")