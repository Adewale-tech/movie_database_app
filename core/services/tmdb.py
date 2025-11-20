import requests
import os
from django.conf import settings

class TMDBService:
    BASE_URL = "https://api.themoviedb.org/3"
    
    def __init__(self):
        self.api_key = os.getenv("TMDB_API_KEY")
        if not self.api_key:
            # Fallback or warning
            print("Warning: TMDB_API_KEY not found in environment variables.")

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json;charset=utf-8"
        }
    
    def _get_params(self):
        # For v3 API key query param usage (alternative to Bearer)
        return {"api_key": self.api_key}

    def get_trending_movies(self, time_window="week"):
        """Fetch trending movies."""
        url = f"{self.BASE_URL}/trending/movie/{time_window}"
        response = requests.get(url, params=self._get_params())
        if response.status_code == 200:
            return response.json().get("results", [])
        return []

    def get_movie_details(self, movie_id):
        """Fetch movie details including credits and reviews."""
        url = f"{self.BASE_URL}/movie/{movie_id}"
        params = self._get_params()
        params['append_to_response'] = 'credits,reviews'
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return None

    def search_movies(self, query):
        """Search for movies."""
        url = f"{self.BASE_URL}/search/movie"
        params = self._get_params()
        params['query'] = query
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get("results", [])
        return []
