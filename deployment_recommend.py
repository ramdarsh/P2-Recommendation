import streamlit as st
import pickle
import pandas as pd
import gdown

# -----------------------------------------------------------
# 🎥 PAGE CONFIG (should always be first Streamlit command)
# -----------------------------------------------------------
st.set_page_config(
    page_title="🎬 Movie Recommendation System",
    layout="wide",
    page_icon="🎞️"
)

# -----------------------------------------------------------
# 🎨 BACKGROUND + HEADER IMAGE
# -----------------------------------------------------------
st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/IMDB_Logo_2016.svg/575px-IMDB_Logo_2016.svg.png', width=200)

background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://www.insightpublications.com.au/wp-content/uploads/Responding-to-film-Blog-Header_FINAL_19Apr2018.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
</style>
"""
st.markdown(background_image, unsafe_allow_html=True)

# -----------------------------------------------------------
# 📦 LOAD MODEL & DATA
# -----------------------------------------------------------
file_id = "1ePtoMq-FnbW27Z3YEVktlZoM3Vg3W43w"
pkl_url = f"https://drive.google.com/uc?id={file_id}"

@st.cache_resource
def load_similarity_matrix():
    gdown.download(pkl_url, "movie_similarity_matrix.pkl", quiet=True)
    with open('movie_similarity_matrix.pkl', 'rb') as f:
        return pickle.load(f)

try:
    movie_similarity_matrix = load_similarity_matrix()
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

# -----------------------------------------------------------
# 🎬 TITLE
# -----------------------------------------------------------
st.markdown("<h1 style='text-align: center; color: white;'>Movie Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("---")

# -----------------------------------------------------------
# 🎛️ USER INPUT
# -----------------------------------------------------------
selected_movie = st.selectbox('🎥 Select a movie:', movieList)
num_recommendations = st.slider('🔢 Number of recommendations:', 1, 20, 10)

# -----------------------------------------------------------
# 🧠 RECOMMENDATION LOGIC
# -----------------------------------------------------------
def get_recommendations(movie_name, num):
    if movie_name not in movieList:
        st.warning("Movie not found in database!")
        return []

    # Use movie name directly if matrix is indexed by movie titles
    if movie_name in movie_similarity_matrix.index:
        similarity_scores = movie_similarity_matrix.loc[movie_name]
    else:
        # fallback to index position
        movie_index = movieList.index(movie_name)
        similarity_scores = movie_similarity_matrix.iloc[movie_index]

    sorted_movies = similarity_scores.sort_values(ascending=False)
    recommendations = []

    for movie, score in sorted_movies.items():
        if movie == movie_name:
            continue
        recommendations.append({
            'title': movie,
            'year': movie_year_dict.get(movie, 'N/A'),
            'certificate': movie_cert_dict.get(movie, 'N/A')
        })
        if len(recommendations) >= num:
            break
    return recommendations

# -----------------------------------------------------------
# 🎞️ DISPLAY RESULTS
# -----------------------------------------------------------
if selected_movie:
    recommendations = get_recommendations(selected_movie, num_recommendations)
    if recommendations:
        st.subheader(f"🎬 Top {num_recommendations} recommendations for '{selected_movie}':")

        cols = st.columns(2)
        for i, rec in enumerate(recommendations):
            with cols[i % 2]:
                st.markdown(
                    f"""
                    <div style='background-color: rgba(0, 0, 0, 0.6); padding: 15px; 
                    border-radius: 10px; margin-bottom: 10px; color: white;'>
                        <h4>🎞️ {rec['title']}</h4>
                        <p>📅 Year: {rec['year']}<br>🎟️ Certificate: {rec['certificate']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.info("No recommendations found.")
