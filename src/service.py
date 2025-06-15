from typing import List
from src.models import Movie
from src.repository import MovieRepository
from src.data_provider import TMDBMovieDataProvider


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
            poster_url=f"http://image.tmdb.org/t/p/w500/{tmdb_data['poster_path']}" if tmdb_data['poster_path'] else None
        )

    def get_recommendations(self, title: str, num_recommendations: int = 10) -> List[Movie]:
        movie_index = self.repository.get_movie_index_by_title(title)
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
                poster_url=f"http://image.tmdb.org/t/p/w500/{tmdb_data['poster_path']}" if tmdb_data['poster_path'] else None
            ))
        
        return recommendations
    
    def get_movie_list(self) -> List[str]:
        return self.repository.get_movie_list()