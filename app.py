import pickle
import streamlit as st
import requests

# Function to fetch movie details (poster and overview)
def fetch_movie_details(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get('poster_path', "")
        overview = data.get('overview', "Description not available.")
        poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Image"
        return poster_url, overview
    except Exception as e:
        return "https://via.placeholder.com/500x750?text=No+Image", "Description not available."

# Recommendation function
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        recommended_movie_descriptions = []

        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]]['id']
            poster_url, description = fetch_movie_details(movie_id)
            recommended_movie_posters.append(poster_url)
            recommended_movie_descriptions.append(description)
            recommended_movie_names.append(movies.iloc[i[0]].title)

        return recommended_movie_names, recommended_movie_posters, recommended_movie_descriptions
    except IndexError:
        return [], [], []

# Streamlit UI
st.markdown("<h1 style='text-align: center; color: #FF6347;'>🎥 Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Discover Your Next Favorite Movie!</h3>", unsafe_allow_html=True)

# Load data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Movie dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Search or select a movie from the dropdown below:",
    movie_list
)

# Show recommendations when button is clicked
if st.button('Show Recommendations'):
    with st.spinner('Fetching recommendations...'):
        recommended_movie_names, recommended_movie_posters, recommended_movie_descriptions = recommend(selected_movie)

    if recommended_movie_names:
        st.markdown("<h4 style='text-align: center;'>Here are some movies you might like:</h4>", unsafe_allow_html=True)

        # Display each movie in a horizontal layout
        for name, poster, description in zip(recommended_movie_names, recommended_movie_posters, recommended_movie_descriptions):
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; margin-bottom: 20px; background-color: #222; padding: 15px; border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
                    <img src="{poster}" alt="{name}" style="width: 150px; height: 225px; border-radius: 10px; margin-right: 20px;"/>
                    <div>
                        <h3 style="color: #FF6347; margin-bottom: 10px;">{name}</h3>
                        <p style="color: #DDD; line-height: 1.6;">{description}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.error("Sorry, no recommendations could be generated. Please try another movie.")
