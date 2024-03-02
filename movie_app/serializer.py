from rest_framework import serializers
from . import models
from rest_framework.exceptions import ValidationError


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
            return f'{movie.director.id}-{movie.director.name}'
        except:
            return "No director found"

    def get_reviews(self, movie):
        #serializer = ReviewSerializer(movie.reviews.all(), many=True)
        serializer = ReviewSerializer(models.Review.objects.filter(author__isnull=False,
                                                                   movie=movie), many=True)
        return serializer.data


class DirectorCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=40)


class ReviewCreateUpdateSerializer(serializers.Serializer):
        stars = serializers.IntegerField(min_value=1, max_value=5)
        text = serializers.CharField(max_length=60)

        def validate_movie_id(self, movie_id):
            if models.Movie.objects.filter(id=movie_id).count() == 0:
                raise ValidationError(f"Movie with id {movie_id} does not exist")


class MovieCreateUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=3, max_length=10)
    description = serializers.CharField()
    duration = serializers.FloatField()
    director_id = serializers.IntegerField()
    reviews = serializers.ListField(child=ReviewCreateUpdateSerializer())

    def validate_director_id(self, director_id):
        if models.Director.objects.filter(id=director_id).count() == 0:
            raise ValidationError(f"Category with id {director_id} does not exist")


    # def validate(self, attrs):
    #     id = attrs['director_id']
    #     try:
    #         models.Director.objects.get(id=id)
    #     except:
    #         raise ValidationError(f"Category with id {id} does not exist")
    #     return attrs


