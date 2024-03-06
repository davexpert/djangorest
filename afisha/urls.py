from django.contrib import admin
from django.urls import path, include
from movie_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/test', views.test),

    path('api/v1/movies', views.movie_list_view),
    path('api/v1/movies/<int:id>', views.movie_detail_view),
    path('api/v1/directors', views.director_list_view),
    path('api/v1/directors/<int:id>', views.director_detail_view),
    path('api/v1/reviews', views.review_list_view),
    path('api/v1/reviews/<int:id>', views.review_detail_view),
    path('api/v1/movies/reviews', views.get_movies_reviews),
    path('api/v1/login/', views.authorization),
    path('api/v1/register/', views.registration),
    path('api/v1/user/reviews/', views.user_reviews),

    # path('accounts/activate/<str:key>/', views.activate_user),
    # path('api/v1/activate/<str:key>', views.activate_user),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
