# Tazama - Django Movie Recommendation Web App 
![Screenshot from 2023-11-15 17-39-46](https://github.com/Mythamor/Tazama-A-Movie-Recommendation-Web-App/assets/113252977/1121486d-2c65-423f-859a-5a39d735b649)

## [Project Inspiration Blog. The Reel Story Behind Tazama](https://medium.com/@MithamoBeth/tazama-a-django-movie-recommendation-web-app-062a62a08228)
> >   ![android-chrome-192x192](https://github.com/Mythamor/Tazama-A-Movie-Recommendation-Web-App/assets/113252977/6330f758-e433-4bc1-abc8-f96d2fddac84)
> What's the reel story behind the tazama? Visit my blog post.
[Tazama: A Movie Recommendation web app](https://medium.com/@MithamoBeth/tazama-a-django-movie-recommendation-web-app-062a62a08228)

## [How tazama works?] Watch the Trailer (https://www.youtube.com/watch?v=spNG2BryASg)
[![Watch the video](https://img.youtube.com/vi/spNG2BryASg/hqdefault.jpg)](https://www.youtube.com/watch?v=spNG2BryASg)

Tazama is not just a movie recommendation app; it's a cinematic masterpiece! 🚀 Built with Django, HTML, CSS, Bootstrap, JS, and a dash of jQuery, it gives users personalized movie suggestions and also features a mini-blog with a social twist. Lights, camera, interaction! 🍿 It incorporates a powerful recommendation engine that utilizes content-based filtering with Natural Language Processing (NLP) and cosine similarity.

## Why Django?
1. The Object-Relational Mapping (ORM) system provided a smooth interaction with the database, simplifying data operations. 
2. Leveraging the Django REST Framework, I built a robust API, ensuring seamless communication between the front end and backend. 
3. Django's built-in authentication system secured user data, and the admin interface facilitated easy management of the movie dataset. 
4. The template engine, middleware support, and Django signals enhanced the app's functionality, while scalability features ensured efficient handling of a growing user base. 
5. The focus on security, extensive community support, and well-documented resources made Django the ideal framework for crafting Tazama's efficient and secure architecture.

### Key Tazama Features:
> 1. 🎥 Personalized movie recommendations based on similar movies.
> 2. 🌐 Mobile responsive web app with playful UI.
> 3. ✨ A mini-blog for a social touch. Users can register, login, create profiles, and, update and delete blogs. Social features including likes, comments, shares will be added to v2 of the app.


## NLP Recommendation Engine
The movie recommender system is powered by a robust dataset containing over 9000 movies and one million tags. Leveraging the capabilities of Natural Language Processing (NLP) and employing cosine similarity, this engine provides users with personalized movie recommendations. By analyzing genres and tags, the system suggests movies that align with the user's taste, creating a tailored and enjoyable viewing experience.
[Recommendation Notebook](https://github.com/Mythamor/Tazama-A-Movie-Recommendation-Web-App/blob/main/recommendation_engine/Movie_Recommendation_System.ipynb)

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
> What's your next watch during Nextfilx and Chill? Visit [tazama](tazama.tech) for a recommendation.

>> Tazama is deployed on a custom-configured Linux server on Digital Ocean

## Author:
> Mithamo Beth




