# Tazama - Movie Recommendation Web App
![Screenshot from 2023-11-15 17-39-46](https://github.com/Mythamor/Tazama-A-Movie-Recommendation-Web-App/assets/113252977/1121486d-2c65-423f-859a-5a39d735b649)


## Project Inspiration:
> For the reel story behind the tazama, visit my blog post.   
[Tazama: A Movie Recommendation web app](https://medium.com/@MithamoBeth/tazama-a-django-movie-recommendation-web-app-062a62a08228)

## Introduction
Tazama is not just a movie recommendation app; it's a cinematic masterpiece! 🚀 Built with Django, HTML, CSS, Bootstrap, JS, and a dash of jQuery, it gives users personalized movie suggestions and also features a mini-blog with a social twist. Lights, camera, interaction! 🍿 It incorporates a powerful recommendation engine that utilizes content-based filtering with Natural Language Processing (NLP) and cosine similarity.

## Why Django?
1. The Object-Relational Mapping (ORM) system provided a smooth interaction with the database, simplifying data operations. 
2. Leveraging the Django REST Framework, I built a robust API, ensuring seamless communication between the front end and backend. 
3. Django's built-in authentication system secured user data, and the admin interface facilitated easy management of the movie dataset. 
4. The template engine, middleware support, and Django signals enhanced the app's functionality, while scalability features ensured efficient handling of a growing user base. 
5. The focus on security, extensive community support, and well-documented resources made Django the ideal framework for crafting Tazama's efficient and secure architecture.

### Key Features:
> 🎥 Personalized movie recommendations based on similar movies.
> 🌐 Mobile responsive web app with playful UI.
> ✨ A mini-blog for a social touch. Users can register, login, create profiles, and, update and delete blogs. Social features will be added to v2 of the app.


## Recommendation Engine
The movie recommender system is powered by a robust dataset containing over 9000 movies and one million tags. Leveraging the capabilities of Natural Language Processing (NLP) and employing cosine similarity, this engine provides users with personalized movie recommendations. By analyzing genres and tags, the system suggests movies that align with the user's taste, creating a tailored and enjoyable viewing experience.


## Installation

### 1. Create Virtual Environment
``` bash
python -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
``` bash
    pip install -r requirements.txt
```
## Usage

### 1. Run Migrations
``` bash
    python manage.py migrate
```

### 2. Start the Party
``` bash
    python manage.py runserver
```

## Deployment: 
> [tazama](tazama.tech)

## Author:
> Mithamo Beth




