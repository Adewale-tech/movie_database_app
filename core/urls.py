from django.urls import path
from .views import HomeView, MovieDetailView, SearchView, AddToWatchlistView, RemoveFromWatchlistView, WatchlistView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('movie/<int:movie_id>/', MovieDetailView.as_view(), name='movie_detail'),
    path('search/', SearchView.as_view(), name='search'),
    path('watchlist/', WatchlistView.as_view(), name='watchlist'),
    path('watchlist/add/<int:movie_id>/', AddToWatchlistView.as_view(), name='add_to_watchlist'),
    path('watchlist/remove/<int:movie_id>/', RemoveFromWatchlistView.as_view(), name='remove_from_watchlist'),
]
