from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post


def index(request):
    all_posts = Post.objects.all().order_by("-posted")
    return render(
        request, "network/index.html", {"posts": all_posts, "title": "All Posts"}
    )


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
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def post(request):
    if request.method == "POST":
        postBody = request.POST.get("postbody")
        currentUser = request.user

        newPost = Post(description=postBody, poster=currentUser)

        newPost.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/newpost.html")


def followingFunction(user, stalker):
    followers = user.followers.all()
    isFollowing = False
    for follower in followers:
        if stalker == follower:
            isFollowing = True
        else:
            isFollowing = False
    return isFollowing


def profile_view(request, name):
    currentUser = request.user
    user = User.objects.get(username=name)
    followersCount = user.followers.count()
    followingCount = user.following.count()
    userPosts = Post.objects.filter(poster=user)
    userPosts = userPosts.order_by("-posted")

    isFollowing = followingFunction(user, currentUser)

    return render(
        request,
        "network/profile.html",
        {
            "currentUser": currentUser,
            "idName": user,
            "followerCount": followersCount,
            "followingCount": followingCount,
            "isFollowing": isFollowing,
            "userPosts": userPosts,
        },
           )


def follow(request, name):
    userToFollow = User.objects.get(username=name)
    userToFollow.followers.add(request.user)
    requestFollowing = User.objects.get(username = request.user)
    requestFollowing.following.add(userToFollow)
    return HttpResponseRedirect(reverse("profile", args=(name,)))


def unfollow(request, name):
    userToUnfollow = User.objects.get(username=name)
    userToUnfollow.followers.remove(request.user)
    requestUnfollow = User.objects.get(username = request.user)
    requestUnfollow.following.remove(userToUnfollow)
    return HttpResponseRedirect(reverse("profile", args=(name,)))


def following_view(request):
    user = User.objects.get(username = request.user)
    userFollowing = user.following.all()
    followingPosts = Post.objects.filter(poster__in = userFollowing).order_by("-posted")     
    return render(
        request, "network/index.html", {"posts": followingPosts, "title": "Following Peoples"}
    )
