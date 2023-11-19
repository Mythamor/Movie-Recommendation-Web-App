from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author","date_posted", "was_published_recently"]
    
    # filter by date_posted
    list_filter = ["date_posted"]
    
admin.site.register(Post, PostAdmin)