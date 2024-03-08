from rest_framework.generics import (ListAPIView,
                                     ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.pagination import PageNumberPagination
from movie_app.models import Review, Movie, Director
from movie_app.serializer import (ReviewSerializer,
                                  MovieSerializer,
                                  DirectorSerializer,
                                  ReviewCreateUpdateSerializer)
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from . serializers import UserCreateSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class AuthorizationAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            Token.objects.filter(user=user).delete()

            token = Token.objects.create(user=user)
            return Response(data={'key': token.key},
                            status=status.HTTP_200_OK)

        return Response(data={'error': "User not found"},
                        status=status.HTTP_404_NOT_FOUND)


class RegisterApiView(APIView):
    serializer_class = UserCreateSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        User.objects.create_user(**serializer.validated_data)
        return Response(data={'message': "User created successfully"},
                        status=status.HTTP_201_CREATED)

class ReviewListApiView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewUpdateDeleteApiView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'

class MovieListApiView(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = PageNumberPagination
    filterset_fields = ['director', 'title']


class MovieUpdateDeleteApiView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'id'

class DirectorListApiView(ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

class DirectorUpdateDeleteApiView(RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    lookup_field = 'id'


class UserReviewListApiView(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer