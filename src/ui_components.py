import streamlit as st
from typing import List
from src.models import Movie


class MovieUIComponents:
    @staticmethod
    def display_movie_details(movie: Movie):
        """Display detailed information about a movie"""
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if movie.poster_url:
                st.image(movie.poster_url, width=300)
            else:
                st.image("https://via.placeholder.com/300x450?text=No+Poster+Available", width=300)
        
        with col2:
            st.subheader(movie.title)
            st.write(f"**Release Date:** {movie.release_date}")
            st.write(f"**Rating:** {movie.rating:.1f}/10")
            st.write(f"**Genres:** {', '.join(movie.genres)}")
            st.write("**Overview:**")
            st.write(movie.overview)
    
    @staticmethod
    def display_movie_recommendations(recommendations: List[Movie]):
        """Display movie recommendations in a grid layout"""
        st.subheader("Recommended Movies")
        
        # Display recommendations in a grid
        cols = st.columns(5)
        for idx, movie in enumerate(recommendations):
            with cols[idx % 5]:
                if movie.poster_url:
                    st.image(movie.poster_url, width=150)
                else:
                    st.image("https://via.placeholder.com/150x225?text=No+Poster", width=150)
                st.write(f"**{movie.title}**")
                st.write(f"Rating: {movie.rating:.1f}/10")
    
    @staticmethod
    def show_error_messages():
        """Display common error messages and setup instructions"""
        st.error("Required data files not found")
        st.info("Please ensure you have the following files in your directory:")
        st.write("- movie_info.csv (containing movie information)")
        st.write("- similarity.pkl (containing similarity matrix)")
    
    @staticmethod
    def get_api_key() -> str:
        """Get TMDB API key from secrets or user input"""
        if "tmdb_api_key" in st.secrets:
            return st.secrets["tmdb_api_key"]
        else:
            api_key = st.text_input("Enter your TMDB API key", type="password")
            if not api_key:
                st.warning("Please enter your TMDB API key to continue")
                st.info("You can get a free API key from https://www.themoviedb.org/settings/api")
            return api_key