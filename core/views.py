from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .services.tmdb import TMDBService
from .models import Watchlist

class HomeView(View):
    def get(self, request):
        tmdb = TMDBService()
        trending_movies = tmdb.get_trending_movies()
        
        watchlist_movie_ids = []
        if request.user.is_authenticated:
            watchlist_movie_ids = list(Watchlist.objects.filter(user=request.user).values_list('movie_id', flat=True))
            
        return render(request, 'core/home.html', {
            'movies': trending_movies,
            'watchlist_movie_ids': watchlist_movie_ids
        })

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

class FeedbackView(View):
    def get(self, request):
        return render(request, 'core/feedback.html')

    def post(self, request):
        # In a real app, we would save this or send an email
        # For now, just redirect home with a success message (if messages were set up)
        return redirect('core:home')

class RateMovieView(LoginRequiredMixin, View):
    def post(self, request, movie_id):
        rating = request.POST.get('rating')
        if rating:
            # Save rating logic here (using Review model or similar)
            # For this demo, we'll just assume it's saved
            pass
        return redirect('core:movie_detail', movie_id=movie_id)

class DebugDBView(View):
    def get(self, request):
        import os
        import dj_database_url
        import psycopg2
        from django.http import HttpResponse

        output = ["<h1>Database Diagnostic</h1>"]
        
        # 1. Check Environment Variable
        db_url = os.getenv('DATABASE_URL')
        if not db_url:
            output.append("<p style='color:red'>❌ DATABASE_URL is NOT set in environment variables.</p>")
        else:
            output.append("<p style='color:green'>✅ DATABASE_URL is set.</p>")
            safe_url = db_url.split('@')[-1] if '@' in db_url else '***'
            output.append(f"<p>Value (masked): ...{safe_url}</p>")

            # 2. Check Parsing
            try:
                config = dj_database_url.parse(db_url, conn_max_age=600, ssl_require=True)
                output.append("<p style='color:green'>✅ dj_database_url parsed the URL successfully.</p>")
                output.append(f"<ul><li>Engine: {config.get('ENGINE')}</li><li>Name: {config.get('NAME')}</li><li>Host: {config.get('HOST')}</li></ul>")
                
                # 3. Check Connection
                try:
                    conn = psycopg2.connect(
                        dbname=config['NAME'],
                        user=config['USER'],
                        password=config['PASSWORD'],
                        host=config['HOST'],
                        port=config['PORT'],
                        sslmode='require'
                    )
                    output.append("<p style='color:green'>✅ Successfully connected to PostgreSQL!</p>")
                    conn.close()
                except Exception as e:
                    output.append(f"<p style='color:red'>❌ Failed to connect to PostgreSQL: {e}</p>")
            except Exception as e:
                output.append(f"<p style='color:red'>❌ dj_database_url failed to parse URL: {e}</p>")

        return HttpResponse("".join(output))
