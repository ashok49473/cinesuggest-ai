import requests
import streamlit as st
import time
from typing import Dict, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


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
        if hasattr(self, 'session'):
            self.session.close()