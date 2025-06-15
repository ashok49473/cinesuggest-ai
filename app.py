import streamlit as st
import pandas as pd
import pickle
import requests
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple, Dict, Any
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

@dataclass
class Movie:
    title: str
    movie_id: int
    overview: str
    release_date: str
    rating: float
    genres: List[str]
    poster_url: str


class TMDBMovieDataProvider:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.themoviedb.org/3"
        self.image_base_url = "http://image.tmdb.org/t/p/w500"
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,  # number of retries
            backoff_factor=1,  # wait 1, 2, 4 seconds between retries
            status_forcelist=[429, 500, 502, 503, 504],  # HTTP status codes to retry on
        )
        
        # Create a session with retry strategy
        self.session = requests.Session()
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Add user agent to session headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9'
        })

    def get_movie_data(self, movie_id: int) -> Dict[str, Any]:
        max_retries = 3
        retry_delay = 2  # seconds
        
        for attempt in range(max_retries):
            try:
                url = f"{self.base_url}/movie/{movie_id}?api_key={self.api_key}&language=en-US"
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.ConnectionError as e:
                if attempt < max_retries - 1:
                    st.warning(f"Connection error occurred. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # exponential backoff
                else:
                    st.error("Failed to connect to TMDB API after multiple attempts. Please check your internet connection.")
                    return self._get_default_movie_data()
            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching movie data: {str(e)}")
                return self._get_default_movie_data()
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")
                return self._get_default_movie_data()
    
    def _get_default_movie_data(self) -> Dict[str, Any]:
        """Return default movie data structure when API call fails"""
        return {
            'overview': 'Movie data unavailable',
            'release_date': 'Unknown',
            'vote_average': 0.0,
            'genres': [],
            'poster_path': None
        }

    def __del__(self):
        self.session.close()

class MovieRepository:
    def __init__(self, movie_info_path: str, similarity_path: str):
        self.movie_info = pd.read_csv(movie_info_path)
        with open(similarity_path, 'rb') as f:
            self.similarity = pickle.load(f)

    def get_movie_by_title(self, title: str) -> pd.Series:
        return self.movie_info[self.movie_info['title'] == title].iloc[0]

    def get_similar_movies(self, movie_index: int, num_recommendations: int = 10) -> List[Tuple[int, float]]:
        distances = sorted(list(enumerate(self.similarity[movie_index])), reverse=True, key=lambda x: x[1])
        similar_movies = distances[1:num_recommendations+1]
        return similar_movies

class MovieService:
    def __init__(self, repository: MovieRepository, data_provider: TMDBMovieDataProvider):
        self.repository = repository
        self.data_provider = data_provider

    def get_movie_details(self, title: str) -> Movie:
        movie_data = self.repository.get_movie_by_title(title)
        tmdb_data = self.data_provider.get_movie_data(movie_data.movie_id)
        
        return Movie(
            title=title,
            movie_id=movie_data.movie_id,
            overview=tmdb_data['overview'],
            release_date=tmdb_data['release_date'],
            rating=tmdb_data['vote_average'],
            genres=[genre['name'] for genre in tmdb_data['genres']],
            poster_url=f"http://image.tmdb.org/t/p/w500/{tmdb_data['poster_path']}"
        )

    def get_recommendations(self, title: str, num_recommendations: int = 10) -> List[Movie]:
        movie_index = self.repository.movie_info[self.repository.movie_info['title'] == title].index[0]
        similar_movies = self.repository.get_similar_movies(movie_index, num_recommendations)
        
        recommendations = []
        for idx, _ in similar_movies:
            movie_data = self.repository.movie_info.iloc[idx]
            tmdb_data = self.data_provider.get_movie_data(movie_data.movie_id)
            
            recommendations.append(Movie(
                title=movie_data.title,
                movie_id=movie_data.movie_id,
                overview=tmdb_data['overview'],
                release_date=tmdb_data['release_date'],
                rating=tmdb_data['vote_average'],
                genres=[genre['name'] for genre in tmdb_data['genres']],
                poster_url=f"http://image.tmdb.org/t/p/w500/{tmdb_data['poster_path']}"
            ))
        
        return recommendations

def main():
    st.set_page_config(
        page_title="Movie Recommendation System",
        page_icon="🎬",
        layout="wide"
    )
    
    st.title("🎬 Movie Recommendation System")
    
    # Initialize the components
    try:
        movie_repository = MovieRepository(
            movie_info_path="movie_info.csv",
            similarity_path="similarity.pkl"
        )
        
        # You'll need to replace this with your actual TMDB API key
        tmdb_api_key = st.secrets["tmdb_api_key"] if "tmdb_api_key" in st.secrets else st.text_input("Enter your TMDB API key")
        
        if not tmdb_api_key:
            st.warning("Please enter your TMDB API key to continue")
            return
            
        data_provider = TMDBMovieDataProvider(api_key=tmdb_api_key)
        movie_service = MovieService(repository=movie_repository, data_provider=data_provider)
        
        # Get list of movies for selection
        movie_list = movie_repository.movie_info['title'].tolist()
        selected_movie = st.selectbox("Select a movie", movie_list)
        
        if selected_movie:
            # Display selected movie details
            movie_details = movie_service.get_movie_details(selected_movie)
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                if movie_details.poster_url:
                    st.image(movie_details.poster_url, width=300)
                else:
                    st.image("https://via.placeholder.com/300x450?text=No+Poster+Available", width=300)
            
            with col2:
                st.subheader(movie_details.title)
                st.write(f"**Release Date:** {movie_details.release_date}")
                st.write(f"**Rating:** {movie_details.rating:.1f}/10")
                st.write(f"**Genres:** {', '.join(movie_details.genres)}")
                st.write("**Overview:**")
                st.write(movie_details.overview)
            
            # Add a recommend button
            if st.button("Get Recommendations"):
                # Get and display recommendations
                st.subheader("Recommended Movies")
                recommendations = movie_service.get_recommendations(selected_movie)
                
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
    
    except FileNotFoundError as e:
        st.error(f"Required data files not found: {str(e)}")
        st.info("Please ensure you have the following files in your directory:")
        st.write("- movies.csv (containing movie information)")
        st.write("- similarity.pkl (containing similarity matrix)")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()

