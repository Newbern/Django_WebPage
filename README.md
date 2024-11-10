# INCOMPLETE PROJECT


# Django Webpage

## Frameworks

* Django


# Basic Setup
```bash
pip install Django

python -m django-admin startproject mysite
```
# Running server in command line
There is a couple ways to create a django applications including through Windows Command Prompt.
to run the server, type the following command. Dont forget to add your port you can use `8000`, `5050` and etc
```bash
python manage.py runserver localhost:8000
```

Next create a place to hold the website
```bash
cd mysite
python manage.py startapp main
```
# Mysite setup
## Urls Setup
Once you create your `mysite` setup you then want to place your urls 
```bash
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls'))
]
```
this is like the building blocks for other urls you can easily connect to others
## Settings Setup
Under the INSTALLED_APPS you want to place this code
```bash
'main.apps.MainConfig',
```
This here will create the app and make everything work the way its expose to.
And while we are here you can add more ports for other to reach your site right here under
```bash
ALLOWED_HOSTS = ['192.168.1.136', 'localhost']
```
# Main Setup
## Urls Setup
Next you want to create urls.py, so you can have more urls Inside your urls, so they have a way of connecting to one another
```bash
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('page1/', views.page1, name='page1')
]
```
## Views Setup
next you want to set up your views that way you can run code to your HTML page
```bash
from django.shortcuts import render, redirect
from .models import Account, ImageSlide, Part
from django.http import HttpResponse

def home(request):
     # This is a quick way to get a response from the page 
     return HttpResponse("<h1>Hello, World!</h1>")
    
def page1(request):
    # This is how we can get html files and redirect to other ones
    if request.method == "POST":
        name = request.POST.get['name']
        
        if name != "Me":
            # This is how we can go to other pages from our views or reload this page
            return redirect("page1")
            
    elif request.method == "GET":
        # This is how we can get data from the database useing by using or models
        name = Account.objects.filter(user=username)[0].name
        
    # This is how we load in our dynamic html files
    return render(request, 'main/home.html', {'name': name})
```

## Models Setup
Create migrations
```bash
python manage.py makemigrations mysite
```
Here we can create a model which stores data in the database a specific way.
```bash
from django.db import models

# Create a class
class Account(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
```

Next, you want to migrate this and actually put this model to use
```bash
python manage.py makemigrations
```
Next, you want to confirm this creation or update
```bash
python manage.py migrate
```

## Admin Setup
under admin, you want to be able to access this when you search `localhost:8000/admin` so make sure you activate it.
```bash
from django.contrib import admin
from .models import Account

# Register your models here.
admin.site.register(Account)
```

## Templates Set Up
Next you want to have a folder called `templates` where you can store you html files you need to create another file 
under this with the same name as this is under so like this under main `templates/main`.
there you will create a html file called `base.html`. here you can start dynamically programming.
```bash
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
    <h1>Hello, World</h1>
    <!-- Here you can add code from other html file, this is like the basic setup of every page -->
    {% block content %}{% endblock %}
</body>
</html>
```

So, after you create you `base.html` file you will create other called `Home.html`. what we are going to do is pretty
much copy this and then place code from other files that way we can basically save time from writing and reuse this file.

```bash
<!-- This all we have to place to pretty much copy the file-->
{% extend 'main/base.html' %}

<!-- New page will run just like the base.html but now with this code to -->
{% block content %}
    <a href='/'>Home</a>
{% endblock %}
```