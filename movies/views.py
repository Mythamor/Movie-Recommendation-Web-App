import os
import requests
import random
from functools import reduce
from operator import or_
from django.shortcuts import render
from django.http import HttpResponse
from typing import Any
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
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



def home(request):
    API_KEY = os.environ.get('API_KEY')
    paginate_by = 10
    # Fetch a list of movies
    movies = Movie.objects.all()
    
    # Fetch movie details for each movie
    details_list = []
    for movie in movies:
        url = f'https://api.themoviedb.org/3/movie/{movie.tmdb_id}?api_key={API_KEY}&language=en-US'
        response = requests.get(url)
        movie_detail = response.json()
        
        # Add details to the list
        details_list.append({
            'title': movie.title,
            'poster_url': f"https://image.tmdb.org/t/p/w500/{movie_detail.get('poster_path','')}",
            'genre_names': ', '.join(genre.name for genre in movie.genres.all()),
            'tagline': movie_detail.get('tagline', ''),  # Get the tagline or an empty string if empty
        })
        
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
    #context_object_name = ''
    #template_name = ".html"
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch the list of all genres
        context['genres'] = Genre.objects.all()
        
        
        # Adding a list of genre names for each movie in the context
        
        API_KEY = os.environ.get('API_KEY')
        
        details_list = []
        
        for movie in context['object_list']:
            url =  f'https://api.themoviedb.org/3/movie/{movie.tmdb_id}?api_key={API_KEY}&language=en-US'
            response = requests.get(url)
            movie_detail = response.json()
            
            
            #Add details to the list
            details_list.append({
                'title': movie.title,
                'poster_url': f"https://image.tmdb.org/t/p/w500/{movie_detail.get('poster_path','')}",
                'genre_names': ', '.join(genre.name for genre in movie.genres.all()),
                'tagline': movie_detail.get('tagline', ''),# Get the tagline or an empty string if empty
            })
            
            
            # Shuffle the details_list to display results at random
            random.shuffle(details_list)
        
            context['details_list'] = details_list
        return context
    

class MovieDetail(DetailView):
    model = Movie
    #template_name = ".html"
    
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
    paginate_by = 5

    
    def get_queryset(self):
        genres  = self.kwargs['genres'].split('-')
         # Use Q objects to filter movies that belong to any of the specified genres
         # Use reduce and or_ to dynamically build Q objects for filtering
        query = reduce(or_, (Q(genres__name=genre) for genre in genres))
            
        return Movie.objects.filter(query).distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch the list of all genres
        context['genres'] = Genre.objects.all()

        # Adding a list of genre names for each movie in the context
        API_KEY = os.environ.get('API_KEY')
        details_list = []

        for movie in context['object_list']:
            url = f'https://api.themoviedb.org/3/movie/{movie.tmdb_id}?api_key={API_KEY}&language=en-US'
            response = requests.get(url)
            movie_detail = response.json()

            # Add details to the list
            details_list.append({
                'title': movie.title,
                'poster_url': f"https://image.tmdb.org/t/p/w500/{movie_detail.get('poster_path','')}",
                'genre_names': ', '.join(genre.name for genre in movie.genres.all()),
                'tagline': movie_detail.get('tagline', ''),  # Get the tagline or an empty string if empty
            })

        # Update the context outside the loop
        context['details_list'] = details_list
        return context
    
    
""" def get_context_data(self, **kwargs):
        context = super(MovieCategory, self).get_context_data(**kwargs)
        context['movie_genres'] = self.kwargs['genres'].replace('-', ', ')
        return context"""
    

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

        # Adding a list of genre names for each movie in the context
        API_KEY = os.environ.get('API_KEY')
        details_list = []
        
        # Extract movie title from the query parameter
        movie_title = self.request.GET.get('query', '')

        for movie_title in context['object_list']:
            # Use the DataFrame to get additional details
            movie_details = df[df['title'] == movie_title].iloc[0]

            details_list.append({
                'title': movie_title,
                'poster_url': f"https://image.tmdb.org/t/p/w500/{movie_details.get('poster_path', '')}",
                'genre_names': ', '.join(genre.name for genre in Movie.objects.get(title=movie_title).genres.all()),
                'tagline': movie_details.get('tagline', ''),
            })

        context['details_list'] = details_list
        context['movie_title'] = movie_title  # Pass movie_title to the template
        return context





 
""""
class MovieSearch(ListView):
    model = Movie
    paginate_by = 5
    template_name = 'movie_list.html'
    max_suggestions = 10
    
   
    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            object_list = self.model.objects.filter(title__icontains=query)
            print(query)
            print(object_list)
        else:
            object_list = self.model.objects.none()
        return object_list
    
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        max_set = queryset[:self.max_suggestions]
        suggestions = [{'label': movie.title, 'value': movie.title} for movie in max_set]
        return JsonResponse(suggestions, safe=False)
    
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch the list of all genres
        context['genres'] = Genre.objects.all()

        # Adding a list of genre names for each movie in the context
        API_KEY = os.environ.get('API_KEY')
        details_list = []

        for movie in context['object_list']:
            url = f'https://api.themoviedb.org/3/movie/{movie.tmdb_id}?api_key={API_KEY}&language=en-US'
            response = requests.get(url)
            movie_detail = response.json()

            # Add details to the list
            details_list.append({
                'title': movie.title,
                'poster_url': f"https://image.tmdb.org/t/p/w500/{movie_detail.get('poster_path','')}",
                'genre_names': ', '.join(genre.name for genre in movie.genres.all()),
                'tagline': movie_detail.get('tagline', ''),  # Get the tagline or an empty string if empty
            })

        # Update the context outside the loop
        context['details_list'] = details_list
        return context 
"""

"""
def recommend(request):
    
    # Load movies from the dataframe
    final_df = pd.read_csv('recommendation_engine/final.csv',)

    # Instantiate the stemmer
    ps = PorterStemmer()

    # Create the function
    def stems(text):
        l = []
        for i in text.split():
            l.append(ps.stem(i))
            
        return " ".join(l)
    
    # apply stems
    final_df["tags"] = final_df["tags"].apply(stems)
    
    # Instantiate the count vectorizer
    cv = CountVectorizer(max_features=5000, stop_words="english")
    vector = cv.fit_transform(final_df["tags"]).toarray()
    
    # Pass in the similarity vector
    similarity = cosine_similarity(vector)

    # Function for new recommendation
    def get_recommendations(movie):
        index = final_df[final_df["title"] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommendations = [final_df.iloc[i[0]]['title'] for i in distances[1:6]]
        return recommendations

    # Fetch data and create details list
    movie_title = request.GET.get('query', '')
    recommendations = get_recommendations(movie_title)

    details_list = []
    for recommended_movie_title in recommendations:
        tmdb_id = final_df[final_df['title'] == recommended_movie_title]['tmdb_id'].values[0]

        # Fetch data via API
        API_KEY = os.environ.get('API_KEY')  # Set your API key
        url = f'https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={API_KEY}&language=en-US'
        response = requests.get(url)
        movie_detail = response.json()

        # Add details to the list
        details_list.append({
            'title': recommended_movie_title,
            'poster_url': f"https://image.tmdb.org/t/p/w500/{movie_detail.get('poster_path', '')}",
        })

    # Return the details list to be displayed in the template
    return render(request, 'movies/movie_reco.html', {'details_list': details_list})"""
    

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

            details_list = []

            for i in distances[1:6]:
                recommended_movie_title = movie_list.iloc[i[0]]['title']
                tmdb_id = movie_list.iloc[i[0]]['tmdb_id']

                # Fetch data via API
                API_KEY = os.environ.get('API_KEY')  # Set your API key
                url = f'https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={API_KEY}&language=en-US'
                response = requests.get(url)
                movie_detail = response.json()

                # Add details to the list
                details_list.append({
                    'title': recommended_movie_title,
                    'poster_url': f"https://image.tmdb.org/t/p/w500/{movie_detail.get('poster_path', '')}",
                })

            # Return the details list to be displayed in the template
            return render(request, 'movies/movie_reco.html', {'details_list': details_list})
        except IndexError as e:
            # Log the error for further investigation
            print(f"IndexError: {e}")
            return HttpResponse("Error: Index out of range while processing recommendations.")
    else:
        # Handle the case where the movie title is not found
        return render(request, 'movies/home.html')

    
    
"""
def recommend(request):
    model = Movie
    movies = Movie.objects.all()
    
    movie_list = pandas.read_csv('recommendation_engine/tmdb.csv',)

    # Load the pickled recommendation model
    with open('recommendation_engine/similarity.pkl', 'rb') as model_file:
        recommendation_model = pickle.load(model_file)

    # Fetch the title from the request parameters
    movie_title = request.GET.get('query', '')

   # Find the index of the movie with the given title in the DataFrame
    try:
        index = movie_list.index[movie_list['title'] == movie_title].tolist()[0]
    except IndexError:
        # Handle the case where the movie title is not found
        index = None

    if index is not None:
        try:
            distances = sorted(list(enumerate(recommendation_model[index])), reverse=True, key=lambda x: x[1])

            recommendation_string = f"Recommended movies for '{movie_title}':\n"

            for i in distances[1:5]:
                recommended_movie_title = movie_list.iloc[i[0]]['title']
                recommendation_string += f"- {recommended_movie_title}\n"

            # Return the recommendation string
            return HttpResponse(recommendation_string)
        except IndexError as e:
            # Log the error for further investigation
            print(f"IndexError: {e}")
            return HttpResponse("Error: Index out of range while processing recommendations.")
"""
    