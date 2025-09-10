# P2-Recommendation
1. Introduction
Online platforms like IMDb, Netflix, and Prime Video host huge movie libraries.
Users often struggle to find movies they might enjoy.
A Recommendation System helps by suggesting similar movies automatically.
In this project, we built a Content-Based Movie Recommendation System using movie data scraped from IMDb.

Dataset Collection 
(IMDb Scraping) The movie dataset was collected by scraping the IMDb website using Python libraries such as: 
requests (to fetch web pages)
BeautifulSoup (to parse HTML)
pandas (to store data in tabular form)

Strengths 
Dataset scraped directly from IMDb (real & up-to-date). 
Handles spelling mistakes in input movie names. 
Doesn’t require user ratings (works with movie metadata).

Limitations 
All features are treated equally (genre = director = stars, etc.). 
Doesn’t use popularity (votes, ratings) in ranking. 
Only works with content similarity, not user behavior.

Future Enhancements 
Assign higher weights to Genre and Description compared to other fields. 
Add popularity factor (IMDb rating, number of votes). 
Build a Hybrid System combining Content + Collaborative Filtering. 
Deploy as a web app using Flask/Streamlit.
