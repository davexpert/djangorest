from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import serializer, models
from django.db.models import Avg
from .models import Movie, Review
from .serializer import MovieSerializer


@api_view(['GET', 'POST'])
def movie_list_view(request):
    if request.method == 'GET':
        movie = models.Movie.objects.all()
        data = serializer.MovieSerializer(movie, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializers = serializer.MovieCreateUpdateSerializer(data=request.data)
        if not serializers.is_valid():
            return Response(data={'errors': serializers.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
        print(request.data)
        title = request.data.get('title')
        description = request.data.get('description')
        duration = request.data.get('duration')
        director_id = request.data.get('director_id')
        # movie = models.Movie.objects.create(**request.data)
        movie = models.Movie.objects.create(title=title, description=description, duration=duration,
                                                director_id=director_id)

        for i in request.data.get("reviews", []):
            models.Review.objects.create(stars=i['stars'], text=i['text'], movie=movie)


        return Response(data=serializer.MovieSerializer(movie).data,
                        status=status.HTTP_201_CREATED)
        # return Response(data={'message': 'Данные отправлены'})


@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_view(request, id):
    try:
        movie_id = models.Movie.objects.get(id=id)
    except models.Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Movie not found'})

    if request.method == 'GET':
        data = serializer.MovieSerializer(movie_id).data
        return Response(data=data)

    elif request.method == 'DELETE':
        movie_id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={'message': 'Movie deleted'})

    elif request.method == 'PUT':
        movie_id.title = request.data.get('title')
        movie_id.description = request.data.get('description')
        movie_id.duration = request.data.get('duration')
        movie_id.director = request.data.get('director')
        movie_id.save()
        return Response(data=serializer.MovieSerializer(movie_id).data)



@api_view(['GET', 'POST'])
def director_list_view(request):
    if request.method == 'GET':
        director = models.Director.objects.all()
        data = serializer.DirectorSerializer(director, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializers = serializer.DirectorCreateSerializer(data=request.data)
        if not serializers.is_valid():
            return Response(data={'errors': serializers.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
        director = models.Director.objects.create(**request.data)
        return Response(status=status.HTTP_201_CREATED,
                        data=serializer.DirectorSerializer(director).data)

@api_view(['GET', 'PUT', 'DELETE'])
def director_detail_view(request, id):
    try:
        director_id = models.Director.objects.get(id=id)
    except models.Director.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Director not found'})

    if request.method == 'GET':
        data = serializer.DirectorSerializer(director_id).data
        return Response(data=data)
    elif request.method == 'DELETE':
        director_id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, data={'message': 'Director has been deleted'})
    elif request.method == 'PUT':
        director_id.name = request.data.get('name')
        director_id.save()
        return Response(data=serializer.DirectorSerializer(director_id).data)

@api_view(['GET', 'POST'])
def review_list_view(request):
    if request.method == 'GET':
        movie = models.Review.objects.all()
        data = serializer.ReviewSerializer(movie, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializers = serializer.ReviewCreateUpdateSerializer(data=request.data)
        if not serializers.is_valid():
            return Response(data={'errors': serializers.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
        review = models.Review.objects.create(**request.data)
        return Response(data=serializer.ReviewSerializer(review).data,
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_view(request, id):
    try:
        review_id = models.Review.objects.get(id=id)
    except models.Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Review not found'})
    if request.method == 'GET':
        data = serializer.ReviewSerializer(review_id).data
        return Response(data=data)
    elif request.method == 'DELETE':
        review_id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={'message': 'Review has been deleted'})
    elif request.method == 'PUT':
        review_id.movie_id = request.data.get('movie_id')
        review_id.text = request.data.get('text')
        review_id.stars = request.data.get('stars')
        review_id.save()
        return Response(data=serializer.ReviewSerializer(review_id).data)

@api_view(['GET'])
def test(request):
    context = {
        'integer': 100,
        'string': 'hello world',
        'boolean': True,
        'list': [
            1,2,3
        ]
    }
    return Response(data=context)

@api_view(['GET'])
def get_movies_reviews(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    avg_rating = Review.objects.aggregate(Avg('stars'))['stars__avg']

    response_data = {
        'movies': serializer.data,
        'avg_rating': avg_rating
    }

    return Response(response_data)