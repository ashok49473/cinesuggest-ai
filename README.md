# CineSuggest AI - Your personal guide to the world of cinema!


![image](https://github.com/user-attachments/assets/7c9fc425-b751-4f18-bbc8-3e47036ceb7e)

A content-based movie recommendation system that uses the Cosine similarity and Nearest Neighbors algorithm to suggest similar movies. It integrates with The Movie Database (TMDB) API to enhance recommendations with detailed movie metadata such as posters, genres, and overviews.


## Project Structure

```
movie-recommendation-system/
├── main.py                 # Main application entry point
├── models.py              # Data models and structures
├── repository.py          # Data access layer
├── data_provider.py       # TMDB API integration
├── service.py             # Business logic layer
├── ui_components.py       # UI components and layouts
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── movie_info.csv        # Movie information dataset
└── similarity.pkl        # Pre-computed similarity matrix
```

## Architecture

The application follows a clean architecture pattern with clear separation of concerns:

- **Models**: Data structures (`Movie` class)
- **Repository**: Data access layer for CSV and pickle files
- **Data Provider**: External API integration (TMDB)
- **Service**: Business logic and orchestration
- **UI Components**: Streamlit interface components
- **Configuration**: Centralized settings management

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Prepare Data Files**
   - Place `movie_info.csv` with columns: title, movie_id
   - Place `similarity.pkl` containing the similarity matrix

3. **Get TMDB API Key**
   - Register at [TMDB](https://www.themoviedb.org/)
   - Get your API key from the API settings
   - Either add it to Streamlit secrets or enter it in the app

4. **Run the Application**
   ```bash
   streamlit run main.py
   ```

## Features

- **Movie Selection**: Choose from a list of available movies
- **Movie Details**: View comprehensive movie information including:
  - Poster image
  - Release date
  - Rating
  - Genres
  - Overview
- **Recommendations**: Get similar movie recommendations
- **Error Handling**: Robust error handling for API failures
- **Retry Logic**: Automatic retry for failed API requests

## Configuration

The application can be configured through `config.py`:

- **APIConfig**: TMDB API settings (timeout, retries, etc.)
- **AppConfig**: Application settings (file paths, UI settings, etc.)

## API Integration

The system integrates with TMDB API to fetch:
- Movie metadata
- Poster images
- Ratings and reviews
- Genre information
