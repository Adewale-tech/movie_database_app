from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .services.tmdb import TMDBService
from .models import Watchlist

class HomeView(View):
    def get(self, request):
        tmdb = TMDBService()
        trending_movies = tmdb.get_trending_movies()
        return render(request, 'core/home.html', {'movies': trending_movies})

class MovieDetailView(View):
    def get(self, request, movie_id):
        tmdb = TMDBService()
        movie = tmdb.get_movie_details(movie_id)
        in_watchlist = False
        if request.user.is_authenticated:
            in_watchlist = Watchlist.objects.filter(user=request.user, movie_id=movie_id).exists()
        return render(request, 'core/movie_detail.html', {'movie': movie, 'in_watchlist': in_watchlist})

class SearchView(View):
    def get(self, request):
        query = request.GET.get('q')
        movies = []
        if query:
            tmdb = TMDBService()
            movies = tmdb.search_movies(query)
        return render(request, 'core/search.html', {'movies': movies, 'query': query})

class AddToWatchlistView(LoginRequiredMixin, View):
    def post(self, request, movie_id):
        # We need movie details to save title/poster
        tmdb = TMDBService()
        movie = tmdb.get_movie_details(movie_id)
        
        if movie:
            Watchlist.objects.get_or_create(
                user=request.user,
                movie_id=movie_id,
                defaults={
                    'title': movie.get('title'),
                    'poster_path': movie.get('poster_path')
                }
            )
        return redirect('core:movie_detail', movie_id=movie_id)

class RemoveFromWatchlistView(LoginRequiredMixin, View):
    def post(self, request, movie_id):
        Watchlist.objects.filter(user=request.user, movie_id=movie_id).delete()
        # Redirect to where the user came from, or watchlist
        next_url = request.POST.get('next', 'core:watchlist')
        return redirect(next_url)

class WatchlistView(LoginRequiredMixin, View):
    def get(self, request):
        watchlist = Watchlist.objects.filter(user=request.user)
        return render(request, 'core/watchlist.html', {'watchlist': watchlist})
