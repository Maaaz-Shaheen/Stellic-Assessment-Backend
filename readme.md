## Assessment Submission

### Setup
To run the code, please make sure python is 
installed along with the following libraries

```
pip install requests
pip install django
```

 Now, open the terminal, change directory 
 to the folder with manage.py and run the following command to start the application.

```
python manage.py runserver
```

Navigate to 127.0.0.1:8000 on your browser. The page will open with a JSON 
response of the urls you can navigate to.

### Links

To get all news:
```
http://127.0.0.1:8000/news
```


To get all news with a query:
```
http://127.0.0.1:8088/news?query=bitcoin
```

To get all favourites of a user:
```
http://127.0.0.1:8088/news/favourite/?user=maaaz
```

To favourite/unfavourite an article
```
http://127.0.0.1:8088/news/favourite/?user=maaaz&id=2
```


### F.A.Q

*How do I make a new user?*

A new user can be set in the admin panel at 
http://127.0.0.1:8088/admin using the login details as below:

```
Username: admin
Password: admin
```