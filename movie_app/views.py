from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import serializer, models
from django.db.models import Avg
from .models import Movie, Review
from .serializer import MovieSerializer


@api_view(['GET'])
def movie_list_view(request):
    movie = models.Movie.objects.all()
    data = serializer.MovieSerializer(movie, many=True).data
    return Response(data=data)


@api_view(['GET'])
def movie_detail_view(request, id):
    try:
        movie_id = models.Movie.objects.get(id=id)
    except models.Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Movie not found'})

    data = serializer.MovieSerializer(movie_id).data
    return Response(data=data)


@api_view(['GET'])
def director_list_view(request):
    director = models.Director.objects.all()
    data = serializer.DirectorSerializer(director, many=True).data
    return Response(data=data)


@api_view(['GET'])
def director_detail_view(request, id):
    try:
        director_id = models.Director.objects.get(id=id)
    except models.Director.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Director not found'})

    data = serializer.DirectorSerializer(director_id).data
    return Response(data=data)

@api_view(['GET'])
def review_list_view(request):
    movie = models.Review.objects.all()
    data = serializer.ReviewSerializer(movie, many=True).data
    return Response(data=data)

@api_view(['GET'])
def review_detail_view(request, id):
    try:
        review_id = models.Review.objects.get(id=id)
    except models.Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Review not found'})

    data = serializer.ReviewSerializer(review_id).data
    return Response(data=data)

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