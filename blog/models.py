import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import admin
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    genres = models.CharField(blank=True, max_length=20)
    
    
    def __str__(self):
        return f"{self.title} by {self.author} posted on date {self.date_posted.day}, month {self.date_posted.month}"

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    
    @admin.display(
        boolean = True,
        ordering = "date_posted",
        description = "recently posted",
    )
    def was_published_recently(self):
        """Shows if the post was recently added.

        Returns:
            _type_: _description_
        """
        return self.date_posted >= timezone.now() - datetime.timedelta(days=1)
