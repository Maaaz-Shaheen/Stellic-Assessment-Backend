from tkinter import CASCADE
from django.db import models


# Create your models here.


# model to store query text and
class Query(models.Model):
    query = models.CharField(max_length=200)
    run_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query

    def getCreatedTime(self):
        return self.run_at


# model to store every news item returned from a query
class NewsItem(models.Model):
    headline = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    source = models.CharField(max_length=200)
    # query = models.ForeignKey(Query, on_delete=models.CASCADE)
    query = models.ManyToManyField(Query)

    def __str__(self):
        return str([self.headline, self.link, self.source])


# model to store users
# assumption is made that username will always be unique
class User(models.Model):
    name = models.CharField(max_length=200, unique=True)
    favourite_articles = models.ManyToManyField(NewsItem, through="Favourite")

    def __str__(self):
        return self.name


# model to store favourites of each user
class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(NewsItem, on_delete=models.CASCADE)

    def __str__(self):
        return str([self.user, self.article])
