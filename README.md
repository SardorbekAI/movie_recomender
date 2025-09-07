# 🎬 Movie Recommendation System

This project is a **Content-Based Movie Recommendation System**.
It uses **TMDB 5000 Movies Dataset** and **Streamlit** for the user interface.

## 🚀 Features

* Preprocess movie data (genres, keywords, cast, crew).
* Create tags for each movie using NLP and stemming.
* Vectorize tags with **CountVectorizer**.
* Find similarity with **cosine similarity**.
* Recommend top 5 movies with **posters** from TMDB API.

## 📂 Dataset

The dataset is from Kaggle:

* `tmdb_5000_movies.csv`
* `tmdb_5000_credits.csv`

If you have a zip file, extract it before running the code.

## ⚙️ Installation

Clone the repo:

```bash
git clone https://github.com/your-username/movie-recommender.git
cd movie-recommender
```

Install requirements:

```bash
pip install -r requirements.txt
```

## 📄 Requirements

Create a file named `requirements.txt` with this content:

```
numpy
pandas
requests
streamlit
scikit-learn
nltk
```

After install, run:

```python
import nltk
nltk.download('punkt')
```

## ▶️ Run Locally

```bash
streamlit run app.py
```

## 🌍 Run Online

1. Push this project to GitHub.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) → deploy new app.
3. Select your GitHub repo and `app.py` file.
4. Done! Your movie recommender will be online.

## 🎥 Demo

The app asks you to choose a movie and shows **5 recommended movies** with their posters.
