from django.contrib import admin

# Register your models here.
from .models import Query, NewsItem, Favourite, User

admin.site.register(NewsItem)
admin.site.register(Query)
admin.site.register(User)
admin.site.register(Favourite)


