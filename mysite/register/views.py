from django.shortcuts import render
from django.http import HttpResponse
from main.views import image
from .forms import RegisterForm
# Create your views here.

def register(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = RegisterForm(request.POST)
        else:
            form = RegisterForm()
    else:
        form = RegisterForm(request.POST)


    return render(request, "register/SignUp.html", {"Profile_Image": image(request), "form": form})
