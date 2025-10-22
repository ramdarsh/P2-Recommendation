import streamlit as st
import pickle
import pandas as pd
import gdown


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

file_id = "1ePtoMq-FnbW27Z3YEVktlZoM3Vg3W43w"
pkl_url = f"https://drive.google.com/uc?id={file_id}"

try:
    # Download the file from Google Drive
    gdown.download(pkl_url, "movie_similarity_matrix.pkl", quiet=False)

    # Load the pickle file
    with open('movie_similarity_matrix.pkl', 'rb') as f:
        movie_similarity_matrix = pickle.load(f)

except Exception as e:
    st.error(f"Error loading movie similarity matrix: {e}")
    st.stop()

try:
    yearCertificate = pd.read_csv('yearCertificate.csv')
    movieList = yearCertificate['movielist'].tolist()
    movie_year_dict = dict(zip(yearCertificate['movielist'], yearCertificate['year']))
    movie_cert_dict = dict(zip(yearCertificate['movielist'], yearCertificate['certificate']))
except FileNotFoundError:
    st.error("Error: yearCertificate.csv not found. Please place the file in the app directory.")
    st.stop()


st.set_page_config(page_title="Movie Recommendation System", layout="wide")
st.title('🎬 Movie Recommendation System')

selected_movie = st.selectbox('Select a movie:', movieList)
num_recommendations = st.slider('Number of recommendations:', 1, 20, 10)

# Recommendation Logic
# -----------------------------
def get_recommendations(movie_name, num):
    if movie_name not in movieList:
        st.warning("Movie not found in database!")
        return []

    movie_index = movieList.index(movie_name)
    similarity_scores = movie_similarity_matrix.iloc[movie_index]
    sorted_movies = similarity_scores.sort_values(ascending=False)

    recommendations = []
    for i, (movie, score) in enumerate(sorted_movies.items()):
        if i == 0:
            continue
        recommendations.append({
            'title': movie,
            'year': movie_year_dict.get(movie, 'N/A'),
            'certificate': movie_cert_dict.get(movie, 'N/A')
        })
        if len(recommendations) >= num:
            break
    return recommendations

# -----------------------------
# Display Recommendations
# -----------------------------
if selected_movie:
    recommendations = get_recommendations(selected_movie, num_recommendations)
    if recommendations:
        st.subheader(f"Top {num_recommendations} recommendations for '{selected_movie}':")
        for rec in recommendations:
            st.write(f"- {rec['title']} ({rec['year']})  [{rec['certificate']}]")
    else:
        st.info("No recommendations found.")



