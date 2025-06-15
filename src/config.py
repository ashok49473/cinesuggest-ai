from dataclasses import dataclass
from typing import List


@dataclass
class APIConfig:
    """Configuration for TMDB API"""
    base_url: str = "https://api.themoviedb.org/3"
    image_base_url: str = "http://image.tmdb.org/t/p/w500"
    timeout: int = 10
    max_retries: int = 3
    retry_backoff_factor: int = 1
    retry_status_codes: List[int] = None
    
    def __post_init__(self):
        if self.retry_status_codes is None:
            self.retry_status_codes = [429, 500, 502, 503, 504]


@dataclass
class AppConfig:
    """Configuration for the application"""
    movie_info_path: str = "movie_info.csv"
    similarity_path: str = "similarity.pkl"
    default_recommendations: int = 10
    grid_columns: int = 5
    poster_width_large: int = 300
    poster_width_small: int = 150
    placeholder_image_large: str = "https://via.placeholder.com/300x450?text=No+Poster+Available"
    placeholder_image_small: str = "https://via.placeholder.com/150x225?text=No+Poster"


# Global configuration instances
api_config = APIConfig()
app_config = AppConfig()
