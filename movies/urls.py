from django.urls import path
from .views import home, MovieList, MovieDetail, MovieCategory, MovieSearch, disclaimer, recommend

urlpatterns = [
    path("", home, name="movies-home"),
    path('movies/', MovieList.as_view(), name="movie_list"),
    path("movies/<int:pk>/", MovieDetail.as_view(), name="movie_detail"),
    path('movies/genres/<str:genres>/', MovieCategory.as_view(), name='movie_genres'),
    path('search/', MovieSearch.as_view(), name='movie_search'),
    path('recommend/', recommend, name='movie_recommend'),
]
