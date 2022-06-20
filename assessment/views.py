from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timezone
import requests

from assessment.models import Query, NewsItem, User, Favourite


# ---------------------- PART 1 & 2 ----------------------

def getNews(request):
    # get parameters of query if any
    filterBy = request.GET.get("query", "")

    # check if query exists
    queryExists = Query.objects.filter(query=filterBy)

    if len(queryExists) > 0:
        timePassed = datetime.now(timezone.utc) - queryExists[len(queryExists) - 1].getCreatedTime()

        # check expiry of query of 1 min
        if timePassed.seconds < 60:

            # get news items from DB and make response list
            newsItemsFromDb = NewsItem.objects.filter(query=queryExists.last())

            # return results from db
            return JsonResponse(list(newsItemsFromDb.values("headline", "link", "source", "id")), safe=False)

    # if query does not exist, save it
    q = Query(query=filterBy)
    q.save()


    # fetch news api results with parameters if any
    news = requests.get(
        'https://newsapi.org/v2/top-headlines?q=' + filterBy + '&category=general&language=en&apiKey=bfd5ba809197400ea7bf617aa4c30c71')

    newsJson = news.json()

    # for each news item, save in db and add to aggregatedNews as well
    for nNews in newsJson["articles"]:
        # n = NewsItem(title=nNews["title"], link=nNews["url"], source="newsapi")
        n, created = NewsItem.objects.get_or_create(
            headline=nNews["title"], link=nNews["url"], source="newsapi",
        )

        n.query.add(q)


        # --------- Reddit news data ----------

    # run different query depending on presence of parameters
    redditQuery = ""

    if filterBy == "":
        redditQuery = 'https://www.reddit.com/r/news.json?limit=100'
    else:
        redditQuery = 'https://www.reddit.com/r/news/search.json?q=' + filterBy

    # run fetch with header to ensure reddit does not reject query
    reddit = requests.get(redditQuery, headers={'User-agent': 'newsaggregator:v1 (by Maaaz)'})
    redditJson = reddit.json()

    # for each news item, save in db and add to aggregatedNews as well
    for rNews in redditJson["data"]["children"]:
        n = NewsItem(headline=rNews["data"]["title"], link=rNews["data"]["url"], source="reddit")
        n.save()
        n.query.add(q)

        # return the aggregatedNews results
    return JsonResponse(list(NewsItem.objects.filter(query=q).values("headline", "link", "source", "id")), safe=False)


# ---------------------- PART 3 ----------------------

# view to handle single favourite and get all favourites
def getFavourites(request):
    # extract parameters from query
    userName = request.GET.get("user", None)
    articleId = request.GET.get("id", None)

    # error handling for no username in query
    if not userName:
        return JsonResponse({"error": "Error! Please provide username to get favourite articles"})

    # get user data from db
    user = User.objects.filter(name=userName)

    # error handling for non existing user
    if not user:
        return JsonResponse({"error": "Error! No such user"})

    # if no article ID is provided, all of user's favourite articles are returned
    if not articleId:
        favouriteArticles = Favourite.objects.filter(user=user[0].id)
        responseList = []

        for fArticle in favouriteArticles:
            fav_dic = {
                "user": fArticle.user.name,
                "id": fArticle.article.id,
                "headline": fArticle.article.headline,
                "link": fArticle.article.link,
                "source": fArticle.article.source,
            }

            responseList.append(fav_dic)

        return JsonResponse(responseList, safe=False)

        # attempted a oneliner
        # return JsonResponse(
        #     list(favouriteArticles.values(
        #         username=F("user__name"), article_id_=F("article__id"), headline=F("article__headline"),
        #         link=F("article__link"), source=F("article__source"))
        #     ), safe=False
        # )


    # if at this point, article id must have been provided too so run checks for that
    article = NewsItem.objects.filter(id=articleId)
    if not article:
        return JsonResponse({"error": "Error! No article with this ID found"})

    # check if article is favourited
    fav = Favourite.objects.filter(user=user[0].id, article=article[0].id)

    # empty dict to store response
    fav_dic = dict()

    # if article is favourited, delete entry to unfavourite and set fav_dic with the proper response
    if fav:
        fav_dic = {
            "user": fav[0].user.name,
            "id": fav[0].article.id,
            "headline": fav[0].article.headline,
            "link": fav[0].article.link,
            "source": fav[0].article.source,
            "favourite": False
        }

        fav.delete()

    # if article is not favourited, add it to the favourites table and set fav_dic with proper response
    else:
        newFav = Favourite(user=user[0], article=article[0])
        newFav.save()

        fav_dic = {
            "user": newFav.user.name,
            "id": newFav.article.id,
            "headline": newFav.article.headline,
            "link": newFav.article.link,
            "source": newFav.article.source,
            "favourite": True
        }

    # return response whether favourited or not
    return JsonResponse([fav_dic], safe=False)


# view that handles default url
def getRoutes(request):
    routes = [
        'GET /news',
        'GET /news/favourite'
    ]
    return JsonResponse(routes, safe=False)