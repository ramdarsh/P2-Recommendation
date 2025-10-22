import streamlit as st
import pickle
import pandas as pd
import gdown
import requests

# -----------------------------------------------------------
# 🎥 PAGE CONFIG
# -----------------------------------------------------------
st.set_page_config(
    page_title="🎬 Movie Recommendation System",
    layout="wide",
    page_icon="🎞️"
)

# -----------------------------------------------------------
# 🖼️ BACKGROUND IMAGE + STYLING
# -----------------------------------------------------------
background_image = """
<style>
.stApp {
    background-image: url("https://www.insightpublications.com.au/wp-content/uploads/Responding-to-film-Blog-Header_FINAL_19Apr2018.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-color: rgba(0, 0, 0, 0.4);
    z-index: 0;
}
.block-container {
    background: rgba(0, 0, 0, 0.55);
    padding: 2rem;
    border-radius: 12px;
    color: white;
    position: relative;
    z-index: 1;
}
[data-testid="stSidebar"], [data-testid="stHeader"] {
    background: rgba(0, 0, 0, 0);
}
</style>
"""
st.markdown(background_image, unsafe_allow_html=True)

# -----------------------------------------------------------
# 🎬 APP HEADER
# -----------------------------------------------------------
st.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/IMDB_Logo_2016.svg/575px-IMDB_Logo_2016.svg.png",
    width=200,
)
st.markdown("<h1 style='text-align: center; color: white;'>Movie Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("---")

# -----------------------------------------------------------
# 📦 LOAD DATA AND MODEL
# -----------------------------------------------------------
file_id = "1ePtoMq-FnbW27Z3YEVktlZoM3Vg3W43w"
pkl_url = f"https://drive.google.com/uc?id={file_id}"

@st.cache_resource
def load_similarity_matrix():
    gdown.download(pkl_url, "movie_similarity_matrix.pkl", quiet=True)
    with open("movie_similarity_matrix.pkl", "rb") as f:
        return pickle.load(f)

try:
    movie_similarity_matrix = load_similarity_matrix()
except Exception as e:
    st.error(f"Error loading movie similarity matrix: {e}")
    st.stop()

try:
    yearCertificate = pd.read_csv("yearCertificate.csv")
    movieList = yearCertificate["movielist"].tolist()
    movie_year_dict = dict(zip(yearCertificate["movielist"], yearCertificate["year"]))
    movie_cert_dict = dict(zip(yearCertificate["movielist"], yearCertificate["certificate"]))
except FileNotFoundError:
    st.error("Error: yearCertificate.csv not found. Please place the file in the app directory.")
    st.stop()

# -----------------------------------------------------------
# 🧠 OMDb POSTER FETCH FUNCTION
# -----------------------------------------------------------
OMDB_API_KEY = "3705bfa"  # 🔑 Replace with your actual OMDb API key

@st.cache_data(show_spinner=False)
def get_movie_poster_omdb(movie_title):
    """Fetch poster URL from OMDb API"""
    if not OMDB_API_KEY:
        return None
    try:
        url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
        response = requests.get(url)
        data = response.json()
        if data.get("Poster") and data["Poster"] != "N/A":
            return data["Poster"]
    except Exception:
        pass
    return None

# -----------------------------------------------------------
# 🎛️ USER INPUT
# -----------------------------------------------------------
selected_movie = st.selectbox("🎥 Select a movie:", movieList)
num_recommendations = st.slider("🔢 Number of recommendations:", 1, 20, 10)

# -----------------------------------------------------------
# 🧮 RECOMMENDATION LOGIC
# -----------------------------------------------------------
def get_recommendations(movie_name, num):
    if movie_name not in movieList:
        st.warning("Movie not found in database!")
        return []

    # Handle both index and label-based access
    if movie_name in movie_similarity_matrix.index:
        similarity_scores = movie_similarity_matrix.loc[movie_name]
    else:
        movie_index = movieList.index(movie_name)
        similarity_scores = movie_similarity_matrix.iloc[movie_index]

    sorted_movies = similarity_scores.sort_values(ascending=False)
    recommendations = []

    for movie, score in sorted_movies.items():
        if movie == movie_name:
            continue
        recommendations.append({
            "title": movie,
            "year": movie_year_dict.get(movie, "N/A"),
            "certificate": movie_cert_dict.get(movie, "N/A"),
        })
        if len(recommendations) >= num:
            break
    return recommendations

# -----------------------------------------------------------
# 🎞️ DISPLAY RECOMMENDATIONS + POSTERS
# -----------------------------------------------------------
if selected_movie:
    recommendations = get_recommendations(selected_movie, num_recommendations)

    # Display the selected movie itself first (Now Showing)
    st.markdown(f"### 🍿 Now Showing: *{selected_movie}*")
    selected_poster = get_movie_poster_omdb(selected_movie)
    if selected_poster:
        st.image(selected_poster, width=200)
    st.markdown("---")

    # Display recommendations
    if recommendations:
        st.subheader(f"🎬 Top {num_recommendations} recommendations for '{selected_movie}':")

        cols = st.columns(2)
        for i, rec in enumerate(recommendations):
            with cols[i % 2]:
                poster_url = get_movie_poster_omdb(rec["title"])
                if poster_url:
                    st.image(poster_url, use_container_width=True)
                st.markdown(
                    f"""
                    <div style='background-color: rgba(255, 255, 255, 0.1); 
                    padding: 15px; border-radius: 10px; margin-bottom: 10px;'>
                        <h4 style='color: #FFD700;'>🎞️ {rec['title']}</h4>
                        <p style='color: white;'>📅 Year: {rec['year']}<br>🎟️ Certificate: {rec['certificate']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        st.info("No recommendations found.")
