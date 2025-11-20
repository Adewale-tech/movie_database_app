from django.db import models
from django.contrib.auth.models import User

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    movie_id = models.IntegerField()
    title = models.CharField(max_length=255)
    poster_path = models.CharField(max_length=255, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie_id')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    movie_id = models.IntegerField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie_id} ({self.rating})"
