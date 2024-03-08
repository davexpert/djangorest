from django.urls import path
from . import views

urlpatterns = [
    path('reviews/', views.ReviewListApiView.as_view()),
    path('reviews/<int:id>/', views.ReviewUpdateDeleteApiView.as_view()),
    path('movies/', views.MovieListApiView.as_view()),
    path('movies/<int:id>/', views.MovieUpdateDeleteApiView.as_view()),
    path('directors/', views.DirectorListApiView.as_view()),
    path('directors/<int:id>/', views.DirectorUpdateDeleteApiView.as_view()),
    path('register/', views.RegisterApiView.as_view()),
    path('login/', views.AuthorizationAPIView.as_view()),
    path('user/reviews/', views.UserReviewListApiView.as_view()),


]