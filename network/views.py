from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm, Textarea
from datetime import datetime
from django.core.paginator import Paginator

from .models import User, Post, Profile, Follows


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['chirp']
        widgets = {'chirp': Textarea(attrs={
            'class': "form-control px-2 py-1.5 text-gray-700 rounded transition ease-in-out m-1",
            'id': "chirperForm",
            'cols': "60",
            'rows': "5",
            'autocomplete': "off",
            'placeholder': 'What\'s Happening?', 
            })}


def index(request):
    form = PostForm(request.POST)
    chirps = Post.objects.all().order_by("-id")
    # Apply Paginator
    paginator = Paginator(chirps, 10)
    pageNumber = request.GET.get('page')
    pageObj = paginator.get_page(pageNumber)
    profile = Profile.objects.all()
    if request.method == "POST":
        if request.user.is_authenticated:
            if form.is_valid():
                chirp = request.POST['chirp']
                f = Post(user=request.user, chirp=chirp, likes=0, date=datetime.now().strftime("%Y-%m-%d"), time=datetime.now().strftime("%H:%M"))
                f.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html")
    else:
        return render(request, "network/index.html", {
            "form": PostForm(),
            "profile": profile,
            "pageObj": pageObj
        })
    

def following_view(request):
    form = PostForm(request.POST)
    currentUser = str(request.user)
    followingAccounts = Follows.objects.filter(follower=currentUser)
    chirps = Post.objects.all().order_by("-id")
    # Apply filtering of posts for Following accounts
    dispFollowing = {}
    count = 0
    for chirp in chirps:
        for account in followingAccounts:
            strChirpUser = str(chirp.user)
            if strChirpUser == account.followed:
                dispFollowing[count] = chirp
                count += 1
    #Apply Paginator
    paginator = Paginator(list(dispFollowing.values()), 10)
    pageNumber = request.GET.get('page')
    pageObj = paginator.get_page(pageNumber)
    profile = Profile.objects.all()
    if request.method == "POST":
        if request.user.is_authenticated:
            if form.is_valid():
                chirp = request.POST['chirp']
                f = Post(user=request.user, chirp=chirp, likes=0, date=datetime.now().strftime("%Y-%m-%d"), time=datetime.now().strftime("%H:%M"))
                f.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html")
    else:
        return render(request, "network/index.html", {
            "form": PostForm(),
            "profile": profile,
            "followingAccounts": followingAccounts,
            "pageObj": pageObj
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
        # Generate profile for new user
        f = Profile(user=request.user, username=request.user)
        f.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile_view(request, name):

    # Access Profile and Post data for rendering
    userProfile = Profile.objects.filter(username=name)
    userProfileId = 0
    for data in userProfile:
        userProfileId = data.id
    chirps = Post.objects.filter(user=userProfileId)

    # Access Follow data for sorting
    currentUser = str(request.user)
    followData = Follows.objects.all()

    # If profile exist, render
    if userProfile:
        return render(request, "network/profilePage.html", {
            "profile": userProfile,
            "chirps": chirps,
            "followData": followData,
            "currentUser": currentUser
            })
    return render(request, "network/login.html")


def handleFollow(request):
    if request.method == "POST":
        if request.user.is_authenticated:

            # Variables for updating both classes (Profile & Follows)
            followedUser = request.POST["profileUsername"]
            followedUserDb = Profile.objects.get(username=followedUser)
            followingUser = request.user
            followingUserDb = Profile.objects.get(username=followingUser)

            # Toggle Follow or Unfollow accordingly
            if Follows.objects.filter(follower=followingUser) and Follows.objects.filter(followed=followedUser):
                unfollowQuery = Follows.objects.get(follower=followingUser, followed=followedUser)
                unfollowQuery.delete()
                # Update number of Followers/Following
                followedUserDb.numFollower -= 1
                followingUserDb.numFollowing -= 1
                followedUserDb.save()
                followingUserDb.save()
                return HttpResponseRedirect(followedUser)
            else:
                f = Follows(followed=followedUser, follower=followingUser)
                f.save()
                # Update number of Followers/Following
                followedUserDb.numFollower += 1
                followingUserDb.numFollowing += 1
                followedUserDb.save()
                followingUserDb.save()
                return HttpResponseRedirect(followedUser)
            
    return render(request, "network/login.html")