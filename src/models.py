from dataclasses import dataclass
from typing import List

@dataclass
class Movie:
    title: str
    movie_id: int
    overview: str
    release_date: str
    rating: float
    genres: List[str]
    poster_url: str
