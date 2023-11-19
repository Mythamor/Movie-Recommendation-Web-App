"""
URL configuration for tazama project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from movies import views as movie_views
from blog import views as blog_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', movie_views.home, name='movies-home'),
    path('movies/', movie_views.MovieList.as_view(template_name='movies/movie_list.html'), name='movie_list'),
    path('movies/genres/<str:genres>/', movie_views.MovieCategory.as_view(), name='movie_genres'),
    path('search/', movie_views.MovieSearch.as_view(), name='movie_search'),
    path('disclaimer/', blog_views.disclaimer, name='disclaimer'),
    path('movies/<int:pk>', movie_views.MovieDetail.as_view(template_name='movies/movie_detail.html'), name='movie_detail'),
    path('recommend/', movie_views.recommend, name='movie_recommend'),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', 
        auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), 
        name='password_reset'),
    path('password-reset/done', 
        auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
        name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), 
        name='password_reset_confirm'),
    path('password-reset-complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), 
        name='password_reset_complete'),
    path('', include('blog.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
