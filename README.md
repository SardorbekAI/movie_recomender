# 🎬 Movie Recommender System

This is a simple **Movie Recommendation Web App** built with **Streamlit** and **The Movie Database (TMDb) API**.
The app recommends 5 similar movies based on a movie selected by the user and displays their posters.

---

## 🚀 Features

* Choose your favorite movie from a dropdown list.
* Get **5 movie recommendations** with titles and posters.
* Uses **cosine similarity** (precomputed and stored in `similarity.pkl`) for recommendations.
* Fetches posters dynamically from the **TMDb API**.

---

## 📂 Project Structure

```
Movie_Recommender/
│── app.py               # Main Streamlit application
│── movies.pkl           # Pickle file containing movie dataset
│── similarity.pkl       # Pickle file with similarity matrix
│── README.md            # Project documentation
│── requirements.txt     # Python dependencies
```

---

## ⚙️ Installation (Local)

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/Movie_Recommender.git
   cd Movie_Recommender
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**

   ```bash
   streamlit run app.py
   ```

Then open **[http://localhost:8501](http://localhost:8501)** in your browser.

---

## 🛠️ Requirements

In your `requirements.txt`, include:

```
streamlit
pickle5
requests
pandas
```

---

## ☁️ Deployment on Streamlit Cloud

1. Push your project to a **public GitHub repository**.
2. Go to [Streamlit Cloud](https://share.streamlit.io/).
3. Sign in with GitHub and click **New app**.
4. Select your repository and `app.py` as the entry file.
5. Click **Deploy** 🎉

Streamlit will install dependencies from `requirements.txt` automatically.

---

## 🔑 API Key

This project uses the **TMDb API**.
Replace the placeholder key inside `fetch_poster` function in `app.py`:

```python
response = requests.get(
    f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=YOUR_API_KEY&language=en-US"
)
```

👉 You can set your API key as a **Streamlit Secret** (recommended for online use):

1. In Streamlit Cloud, go to your app → **Settings** → **Secrets**.
2. Add:

   ```toml
   TMDB_API_KEY="your_api_key_here"
   ```
3. Update your code:

   ```python
   import streamlit as st

   api_key = st.secrets["TMDB_API_KEY"]
   ```
