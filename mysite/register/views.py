from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User
from main.models import Account
from .forms import RegisterForm, LoginForm


# Create your views here.


# Sign in
def register(request):
    if request.method == "POST":
        # Getting  New User Data
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        confirm_password = request.POST['password2']

        # Confirming Password
        if password != confirm_password:
            messages.error(request, 'Passwords must match')
            return redirect('register')

        # Creating User
        else:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username, email, password)
                user.save()

                auth.login(request, user)

                new_user = Account.objects.create(user=user)


                return redirect('home')
            else:
                messages.error(request, 'Account already exists')
                return redirect('register')
    else:
        form = RegisterForm()


    return render(request, "register/SignUp.html", {"form": form})

# Login
def login(request):
    if request.method == "POST":
        # Getting User Login Data
        username = request.POST['username']
        password = request.POST['password']

        # Setting up User authentication
        user = auth.authenticate(username=username, password=password)

        # Checking to see if user exist
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            form = LoginForm()

    else:
        form = LoginForm()

    return render(request, "register/Login.html", {"form": form})


def logout(request):
    auth.logout(request)
    return render(request, "register/Logout.html", {})