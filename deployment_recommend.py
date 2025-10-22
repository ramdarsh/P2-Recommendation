import streamlit as st
import pickle
import requests
import gdown
import os


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

# --- Step 2: Download similarity.pkl from Google Drive ---
file_id = "1ePtoMq-FnbW27Z3YEVktlZoM3Vg3W43w"  # 🔹 Replace with your actual Google Drive file ID
url = f"https://drive.google.com/uc?id={file_id}"
output = "movie_similarity_matrix.pkl"

if not os.path.exists(output):
    with st.spinner('Downloading similarity model... (this may take a few minutes)'):
        gdown.download(url, output, quiet=False)

# --- Step 3: Load similarity.pkl ---
similarity = pickle.load(open('movie_similarity_matrix.pkl', 'rb'))

movies_list = movies['Movie Title'].values

st.header("🎬 MOVIE RECOMMENDER SYSTEM")
selectvalue = st.selectbox('Select movie from dropdown', movies_list)

# --- Step 5: Fetch poster from OMDb API ---
def fetch_poster(movie_name):
    api_key = "3705bfa"  # 🔹 Replace with your OMDb key (get from https://www.omdbapi.com/apikey.aspx)
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('Poster', "https://via.placeholder.com/300x450?text=No+Poster")
    else:
        return "https://via.placeholder.com/300x450?text=Error+Loading"


# --- Step 6: Recommendation function ---
def recommend(movie):
    index = movies[movies['Movie Title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    for i in distances[1:6]:
        recommended_movies.append(movies.iloc[i[0]]['Movie Title'])
    return recommended_movies

# --- Step 7: Display recommendations ---
if st.button("🎥 Show Recommendations"):
    recommendations = recommend(selectvalue)
    st.subheader("Recommended Movies:")

    cols = st.columns(5)
    for col, name in zip(cols, recommendations):
        poster = fetch_poster(name)
        col.image(poster, use_container_width=True)
        col.caption(name)


