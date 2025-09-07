import os
import ast
import requests
import numpy as np
import pandas as pd
import streamlit as st
import zipfile
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================
# Load and preprocess data
# =========================

# Path to your zip file
zip_path1 = "tmdb_5000_credits.csv.zip"   # change if filename is different
zip_path2 = "tmdb_5000_movies.csv.zip"   # change if filename is different

# Extract zip contents
with zipfile.ZipFile(zip_path1, "r") as zip_ref:
    zip_ref.extractall("data1")  # extracts into a folder named "data"
with zipfile.ZipFile(zip_path2, "r") as zip_ref:
    zip_ref.extractall("data2")  # extracts into a folder named "data"

# Now read the CSV files
movies = pd.read_csv("data2/tmdb_5000_movies.csv")
credits = pd.read_csv("data1/tmdb_5000_credits.csv")


movies = movies.merge(credits, on="title")

movies = movies[["movie_id", "title", "overview", "genres", "keywords", "cast", "crew"]]
movies.dropna(inplace=True)


def convert(obj):
    """Convert JSON-like string to list of names."""
    lst = []
    for i in ast.literal_eval(obj):
        lst.append(i["name"])
    return lst


def convert_cast(obj):
    """Take top 3 actors."""
    lst = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            lst.append(i["name"])
            counter += 1
        else:
            break
    return lst


def fetch_director(obj):
    """Fetch director from crew list."""
    lst = []
    for i in ast.literal_eval(obj):
        if i["job"] == "Director":
            lst.append(i["name"])
    return lst


# Apply transformations
movies["genres"] = movies["genres"].apply(convert)
movies["keywords"] = movies["keywords"].apply(convert)
movies["cast"] = movies["cast"].apply(convert_cast)
movies["crew"] = movies["crew"].apply(fetch_director)
movies["overview"] = movies["overview"].apply(lambda x: x.split())

# Remove spaces in names
movies["genres"] = movies["genres"].apply(lambda x: [i.replace(" ", "") for i in x])
movies["keywords"] = movies["keywords"].apply(lambda x: [i.replace(" ", "") for i in x])
movies["cast"] = movies["cast"].apply(lambda x: [i.replace(" ", "") for i in x])
movies["crew"] = movies["crew"].apply(lambda x: [i.replace(" ", "") for i in x])

# Combine into tags
movies["tags"] = (
    movies["overview"]
    + movies["genres"]
    + movies["keywords"]
    + movies["cast"]
    + movies["crew"]
)

new_df = movies[["movie_id", "title", "tags"]]
new_df["tags"] = new_df["tags"].apply(lambda x: " ".join(x))

# Text preprocessing
ps = PorterStemmer()


def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)


new_df["tags"] = new_df["tags"].apply(stem)
new_df["tags"] = new_df["tags"].apply(lambda x: x.lower())

# Vectorization
cv = CountVectorizer(max_features=5000, stop_words="english")
vectors = cv.fit_transform(new_df["tags"]).toarray()
similarity = cosine_similarity(vectors)


# =========================
# Streamlit App
# =========================
movie_list = new_df
movies_titles = new_df["title"].values


def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}"
        f"?api_key=fce04cd6f32aa9ccefa96f8a6dd4e675&language=en-US"
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]


def recommend(movie):
    movie_index = movie_list[movie_list["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in movies_list:
        movie_id = movie_list.iloc[i[0]].movie_id
        recommended_movie_names.append(movie_list.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters


# Streamlit UI
st.title("Movie Recommendation System")
selected_movie = st.selectbox("Choose your favorite movie:", movies_titles)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(names[idx])
            st.image(posters[idx])
