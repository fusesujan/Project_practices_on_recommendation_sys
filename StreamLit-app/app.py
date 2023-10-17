import streamlit as st
import pandas as pd
import random
import numpy as np
# Create a Streamlit app
st.set_page_config(
    page_title="Recommendation App",
    layout="wide",
    initial_sidebar_state="expanded",
)

song_data = pd.read_csv("clean_songs_similarities_score.csv")
movie_indices_data = pd.read_csv("indices_df.csv")
movie_data = pd.read_csv("few_movies.csv")
# product_data = pd.read_csv("sample_products.csv")

data_dict = {
    "Songs": song_data,
    "Movies": movie_data,
    # "Products": product_data,
}


def song_recommendations():
    st.title("Song Recommendations")
    st.write("Enter a song name, and we'll suggest 10 matching songs!")

    song_names = [song for song in data_dict["Songs"]
                  ["Song Name"]]

    selected_song = st.selectbox(
        "Select a song:", [""] + song_names, key="suggestions")

    css = f"""
        <style>
            .song-container {{
                display: flex;
                flex-wrap: wrap;
                justify-content: flex-start;
            }}
            .song-info-box {{
                margin: 15px;
                padding: 10px;
                background-color: #576574;
                border-radius: 10px;
                box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.2);
                width: 100%;
                text-align: center;
                disply:block;
            }}
            
        </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    st.markdown('<div class="song-container">', unsafe_allow_html=True)
    if selected_song:
        if selected_song in song_data.columns:
            recommendation = song_data.nlargest(11, selected_song)["Song Name"]
            st.markdown(
                f"""<h4>Recommended Songs for {selected_song} are:</h4>""", unsafe_allow_html=True)
            for i, song in enumerate(recommendation.values[1:], start=1):
                song_info_html = f"""
                    <div class="song-info-box">
                        <h4>{i}.{song}</h4>
                    </div>
                """

                st.markdown(song_info_html, unsafe_allow_html=True)
        else:
            print("Sorry, there is no song name in our database. Please try another one.")
    st.markdown('</div>', unsafe_allow_html=True)


def movie_recommendations():
    st.title("Movie Recommendations")
    st.write("Enter a movie name, and we'll suggest n (your choice) matching movies!")

    movie_names = [movie for movie in data_dict["Movies"]
                   ["title"]]

    selected_movie = st.selectbox(
        "Select a movie:", [""] + movie_names, key="suggestions")

    cosine_sim = np.load('ndarray_data.npy')

    def get_recommendations(title, cosine_sim=cosine_sim, num_recommend=10):

        idx = movie_indices_data.loc[movie_indices_data['title']
                                     == title].index[0]
        # Get the pairwsie similarity scores of all movies with that movie
        sim_scores = list(enumerate(cosine_sim[idx]))
        # Sort the movies based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        top_similar = sim_scores[1:num_recommend+1]

        # Get the movie indices
        movie_indices = [i[0] for i in top_similar]
        # Return the top 10 most similar movies

        return movie_data['title'].iloc[movie_indices]

    user_input_rec_count = st.number_input(
        "Enter No of movies that you want to get recommended", min_value=0, max_value=100)

    css = f"""
        <style>
        .movie-info-box {{
            margin: 15px;
            padding: 10px;
            background-color: #576574;
            border-radius: 10px;
            box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.2);
            width: 100%;
            text-align: center;
            disply:block;
        }}
        
        </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    if st.button("Submit"):
        if selected_movie != "" or user_input_rec_count != "":
            movies = get_recommendations(
                selected_movie, num_recommend=user_input_rec_count)

            st.markdown(
                f"""<h4>Recommended Movies for {selected_movie} are:</h4>""", unsafe_allow_html=True)
            for i, movie in enumerate(movies, start=1):
                song_info_html = f"""
                    <div class="movie-info-box">
                        <h4>{i}.{movie}</h4>
                    </div>
                """
                st.markdown(song_info_html, unsafe_allow_html=True)


def product_recommendations():
    st.title("Product Recommendations")
    st.write("Enter a product name, and we'll suggest 5 matching products!")

    # product_input = st.text_input("Enter a product name:", "")
    # suggestions = []

    # if product_input:
    #     # Filter products that match the input
    #     suggestions = product_data[product_data["Product Name"].str.contains(
    #         product_input, case=False)]
    #     suggestions = suggestions["Product Name"].sample(5).tolist()

    # if suggestions:
    #     st.subheader("Matching Products:")
    #     for suggestion in suggestions:
    #         st.write(suggestion)


def sidebar():
    st.sidebar.title("Select a Page")
    selected_page = st.sidebar.radio("", ["Songs", "Movies", "Products"])
    return selected_page


selected_page = sidebar()

if selected_page == "Songs":
    css = f"""
    <style>
        body {{
            background-image: linear-gradient(to bottom right, #ffafbd, #ffc3a0);
        }}
    </style>
        """

    st.markdown(css, unsafe_allow_html=True)

    song_recommendations()
elif selected_page == "Movies":
    st.markdown(
        """
        <style>
        body {
            background-image: linear-gradient(to bottom right, #c2e59c, #64b3f4);
        }
        </>
        """,
        unsafe_allow_html=True,
    )
    movie_recommendations()
else:
    st.markdown(
        """
        <style>
        body {
            background-image: linear-gradient(to bottom right, #f6d365, #fda085);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    product_recommendations()
