from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from .resources import MovieResource

# Register your models here.
from .models import Movie, Genre


"""class MovieAdmin(admin.ModelAdmin):
    list_display = ["title", "release_date"]
    
    # filter by release_date
    list_filter = ["release_date"]"""

# Unregister model if registered to avoid errors on rerun
#admin.site.unregister(Movie)  

class MovieAdmin(ImportExportActionModelAdmin):
    resource_class = MovieResource
    
    list_display = ["title",  "tmdb_id"]
    
    
    
admin.site.register(Movie, MovieAdmin)

admin.site.register(Genre)