from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch, MagicMock
from .services.tmdb import TMDBService
from .views import HomeView

class TMDBServiceTest(TestCase):
    @patch('core.services.tmdb.requests.get')
    def test_get_trending_movies_success(self, mock_get):
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [{"id": 1, "title": "Test Movie"}]
        }
        mock_get.return_value = mock_response

        service = TMDBService()
        movies = service.get_trending_movies()
        
        self.assertEqual(len(movies), 1)
        self.assertEqual(movies[0]['title'], "Test Movie")

    @patch('core.services.tmdb.requests.get')
    def test_get_movie_details_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 1, 
            "title": "Test Movie",
            "videos": {"results": []}
        }
        mock_get.return_value = mock_response

        service = TMDBService()
        movie = service.get_movie_details(1)
        
        self.assertEqual(movie['title'], "Test Movie")

class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')

    @patch('core.views.TMDBService.get_trending_movies')
    def test_home_view_status_code(self, mock_get_trending):
        mock_get_trending.return_value = [{"id": 1, "title": "Test Movie"}]
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')

    @patch('core.views.TMDBService.get_trending_movies')
    def test_home_view_context(self, mock_get_trending):
        mock_get_trending.return_value = [{"id": 1, "title": "Test Movie"}]
        response = self.client.get(reverse('core:home'))
        self.assertIn('movies', response.context)
        self.assertEqual(len(response.context['movies']), 1)
