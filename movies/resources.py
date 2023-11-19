from import_export import resources

# Register your models here.
from .models import Movie, Genre


class MovieResource(resources.ModelResource):
    class Meta:
        model = Movie