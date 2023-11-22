import os
import requests
import random
from functools import reduce
from operator import or_
from django.shortcuts import render
from django.http import HttpResponse
from typing import Any
from django.db import models
from django.core.cache import cache
from django.db.models.query import QuerySet, Q
from django.http import JsonResponse
from django.template.loader import render_to_string


# Create your views here.
from django.views.generic import ListView, DetailView
from django.views.generic.dates import YearArchiveView
from .models import Movie, Genre


# Import recommendation engine libraries
import pandas as pd
import pickle
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


API_KEY = "5f8c4580f32863abb80e9aa0ca00509e"


def get_movie_details(movie):
    cache_key = f"movie_details_{movie.tmdb_id}"
    cached_details = cache.get(cache_key)

    if cached_details:
        return cached_details
    

    url = f'https://api.themoviedb.org/3/movie/{movie.tmdb_id}?api_key={API_KEY}&language=en-US'
    response = requests.get(url)
    movie_detail = response.json()
    
    # Add details to the list
    details_list = {
        'title': movie.title,
        'poster_url': f"https://image.tmdb.org/t/p/w500/{movie_detail.get('poster_path','')}",
        'genre_names': ', '.join(genre.name for genre in movie.genres.all()),
        'tagline': movie_detail.get('tagline', ''),  # Get the tagline or an empty string if empty
    }

# Cache the details for future use
    cache.set(cache_key, details_list)

    return details_list


def home(request):
    paginate_by = 10
    
    # Fetch a list of movies
    movies = Movie.objects.all()
    
    # Fetch movie details for each movie
    details_list = [get_movie_details(movie) for movie in movies]
    
        
    # Shuffle the details_list to display results at random
    random.shuffle(details_list)
    
    # Include the details_list in the context
    context = {'title': 'tazama-movies', 'details_list': details_list}
    
    return render(request, 'movies/home.html', context)


class MovieList(ListView):
    """A class that lists all the movies available in the database
        fetches poster and tagline data through TMBD_APIs

    Args:
        ListView (_type_): _description_

    Returns:
        _type_: _description_
    """
    model = Movie
    paginate_by = 12
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch the list of all genres
        context['genres'] = Genre.objects.all()
        
        
        # Fetch movie details for each movie in the object_list
        details_list = [get_movie_details(movie) for movie in context['object_list']]
        
        # Shuffle the details_list to display results at random
        random.shuffle(details_list)

        context['details_list'] = details_list
        return context


class MovieDetail(DetailView):
    model = Movie
    
    def get_object(self):
        object = super(MovieDetail, self).get_object()
        object.view_count += 1
        object.save()
        return object
    


class MovieCategory(ListView):
    """It filters movies by categories/ genres

    Args:
        ListView (_type_): _description_

    Returns:
        _type_: _description_
    """
    model = Movie
    paginate_by = 12

    
    def get_queryset(self):
       selected_genre = self.request.GET.get('selected_genre')
       print(f"Selected Genre: {selected_genre}")

       if selected_genre:
            genres = selected_genre.split('-')
            query = reduce(or_, (Q(genres__name=genre) for genre in genres))
            print(f"Generated Query: {query}")
            return Movie.objects.filter(query).distinct()
       else:
          return Movie.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch the list of all genres
        context['genres'] = Genre.objects.all()

      # Fetch movie details for each movie in the object_list
        details_list = [get_movie_details(movie) for movie in context['object_list']]
        
        # Shuffle the details_list to display results at random
        random.shuffle(details_list)

        context['details_list'] = details_list
        return context
    
    

class MovieSearch(ListView):
    model = Movie
    paginate_by = 5
    template_name = 'movie_list.html'
    max_suggestions = 10

    def get_dataframe(self):
        # Load your DataFrame (replace 'your_dataframe.csv' with the actual file path)
        df = pd.read_csv('recommendation_engine/final.csv')
        return df

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            # Filter movies based on the DataFrame column 'title'
            df = self.get_dataframe()
            titles_matching_query = df[df['title'].str.contains(query, case=False)]
            
            # Get Movie objects for the matching titles
            object_list = [
                Movie(title=movie_title) for movie_title in titles_matching_query['title']
            ]
        else:
            object_list = Movie.objects.none()
        return object_list

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        max_set = queryset[:self.max_suggestions]
        suggestions = [{'label': movie.title, 'value': movie.title} for movie in max_set]
        return JsonResponse(suggestions, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()

        # Load your DataFrame
        df = self.get_dataframe()

        # Fetch movie details for each movie in the object_list
        details_list = [get_movie_details(movie) for movie in context['object_list']]
        
        # Shuffle the details_list to display results at random
        random.shuffle(details_list)

        context['details_list'] = details_list
        return context

    

def recommend(request):
    
    model = Movie
    movies = Movie.objects.all()
    
    # Load movies from the dataframe
    movie_list = pd.read_pickle('recommendation_engine/movie_list.pkl',)

    
    # Load the pickled recommendation model
    with open('recommendation_engine/similarity.pkl', 'rb') as model_file:
        recommendation_model = pickle.load(model_file)

    
    # Fetch the title from the request parameters
    movie_title = request.GET.get('query', '')
    
     # Convert the queryset to a list of titles
    movie_titles = list(movies.values_list('title', flat=True))
    
     # Find the index of the movie with the given title in the DataFrame
    try:
        index = movie_list.index[movie_list['title'] == movie_title].tolist()[0]
    except IndexError:
        # Handle the case where the movie title is not found
        index = None

    if index is not None:
        try:
            distances = sorted(list(enumerate(recommendation_model[index])), reverse=True, key=lambda x: x[1])

            recommend_list = []

            for i in distances[1:6]:
                recommended_movie_title = movie_list.iloc[i[0]]['title']
                tmdb_id = movie_list.iloc[i[0]]['tmdb_id'] # Convert to integer

                
                # Fetch data via API
                url = f'https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={API_KEY}&language=en-US'
                response = requests.get(url)
                movie_detail = response.json()

                # Add details to the list
                recommend_list.append({
                    'title': recommended_movie_title,
                    'poster_url': f"https://image.tmdb.org/t/p/w500/{movie_detail.get('poster_path', '')}",
                })


                                    
            # Return the details list to be displayed in the template
            return render(request, 'movies/movie_reco.html', {'details_list': recommend_list})
        except IndexError as e:
            # Log the error for further investigation
            print(f"IndexError: {e}")
            return HttpResponse("Error: Index out of range while processing recommendations.")
    else:
        # Handle the case where the movie title is not found
        return render(request, 'movies/home.html')

    
