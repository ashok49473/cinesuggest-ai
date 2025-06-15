import streamlit as st
from src.repository import MovieRepository
from src.data_provider import TMDBMovieDataProvider
from src.service import MovieService
from src.ui_components import MovieUIComponents
<<<<<<< HEAD

=======
from src.config import app_config
>>>>>>> b46c11e (modularize code)

def main():
    st.set_page_config(
        page_title="Movie Recommendation System",
        page_icon="🎬",
        layout="wide"
    )
    
    st.title("🎬 Movie Recommendation System")
    
    # Initialize UI components
    ui = MovieUIComponents()
    
    # Get API key
    tmdb_api_key = ui.get_api_key()
    
    if not tmdb_api_key:
        return
    
    # Initialize the components
    try:
        movie_repository = MovieRepository(

            movie_info_path=app_config.movie_info_path,
            similarity_path=app_config.similarity_path
        )
        
        data_provider = TMDBMovieDataProvider(api_key=tmdb_api_key)
        movie_service = MovieService(repository=movie_repository, data_provider=data_provider)
        
        # Get list of movies for selection
        movie_list = movie_service.get_movie_list()
        selected_movie = st.selectbox("Select a movie", movie_list)
        
        if selected_movie:
            # Display selected movie details
            movie_details = movie_service.get_movie_details(selected_movie)
            ui.display_movie_details(movie_details)
            
            # Add a recommend button
            if st.button("Get Recommendations"):
                # Get and display recommendations
                recommendations = movie_service.get_recommendations(selected_movie)
                ui.display_movie_recommendations(recommendations)
    
    except FileNotFoundError:
        ui.show_error_messages()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()