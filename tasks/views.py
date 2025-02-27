from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db import IntegrityError

# Create your views here.


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]: #verificacion de si ambas claves son iguales
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save() #se guarda el usuario en la base de datos
                login(request,user)
                return redirect('tasks')
            except IntegrityError: #IntegrityError captura excepciones solamente de la base de datos
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "errorUser": "User already exists"},
                )
        else:
            return render(
                request,
                "signup.html",
                {"form": UserCreationForm, "errorPasswords": "Passwords not match"},
            )


def tasks(request):
    if request.method == "GET":
        return render(request,'tasks.html')