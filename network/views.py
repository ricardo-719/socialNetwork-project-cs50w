from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm, Textarea
from datetime import datetime

from .models import User, Post, Profile, Follows


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['chirp']
        """ exclude = ['user', 'likes', 'date'] """
        widgets = {'chirp': Textarea(attrs={
            'class': "form-control px-2 py-1.5 text-gray-700 border border-solid border-gray-300 rounded transition ease-in-out m-1 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none",
            'cols': 16,
            'rows': 8,
            'style': 'width: 35%',
            'autocomplete': "off",
            'placeholder': 'What\'s Happening?', 
            })}

def index(request):
    form = PostForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            chirp = request.POST['chirp']
            f = Post(user=request.user, chirp=chirp, likes=0, date=datetime.now().strftime("%Y-%m-%d"))
            f.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/index.html", {
            "form": PostForm()
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")