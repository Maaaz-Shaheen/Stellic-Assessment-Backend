from django.urls import path
from assessment import views

urlpatterns = [
    path('', views.getRoutes),
    path('news/', views.getNews),
    path('news/favourite/', views.getFavourites),
]