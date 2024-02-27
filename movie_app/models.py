from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

class Director(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.FloatField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    @property
    def rating(self):
        return Review.objects.filter(movie=self).aggregate(Avg('stars'))
    #     sum = 0
    #     for i in reviews:
    #         sum_ += i.stars
    #     try:
    #         return sum_ / reviews.count()
    #     except:
    #         return 0

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                               blank=True)
    stars = models.IntegerField(default=5, null=True)

    def __str__(self):
        return self.text