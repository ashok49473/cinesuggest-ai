import pandas as pd
import pickle
from typing import List, Tuple


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
    
    def get_movie_list(self) -> List[str]:
        return self.movie_info['title'].tolist()
    
    def get_movie_index_by_title(self, title: str) -> int:
        return self.movie_info[self.movie_info['title'] == title].index[0]