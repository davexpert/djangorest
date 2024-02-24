from rest_framework import serializers
from . import models

class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Director
        fields = ' id name movies_count'.split()

    def get_movies_count(self, director):
        return director.movie_set.count()


class ReviewSerializer(serializers.ModelSerializer):
    stars = serializers.IntegerField(min_value=1, max_value=5)
    class Meta:
        model = models.Review
        fields = ' id text author stars '.split()


class MovieSerializer(serializers.ModelSerializer):
    #director = DirectorSerializer()
    director = serializers.SerializerMethodField()
    #reviews = ReviewSerializer(many=True)
    reviews = serializers.SerializerMethodField()
    class Meta:
        model = models.Movie
        fields = "id title duration director reviews ".split()
        # fields = "__all__"

    def get_director(self, movie):
        try:
            return movie.director.name
        except:
            return "No director found"

    def get_reviews(self, movie):
        #serializer = ReviewSerializer(movie.reviews.all(), many=True)
        serializer = ReviewSerializer(models.Review.objects.filter(author__isnull=False,
                                                                   movie=movie), many=True)
        return serializer.data
