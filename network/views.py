import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.core import serializers

from .models import User, Post


def index(request):
    # Oredering posts by date
    posts = Post.objects.all().order_by('-date')

    # Displaying max 10 posts per page
    paginator = Paginator(posts, 10)

    page = request.GET.get('page')
    posts = paginator.get_page(page)

    if request.method == "POST" and "p" in request.POST:
        newpost = request.POST['p']

        p = Post(post=newpost, user=request.user)
        p.save()

        return HttpResponseRedirect(reverse('allposts'))


    return render(request, "network/index.html", {
    "posts": posts,
    })

def allposts(request):

    # Get all posts ordered by date
    posts = Post.objects.all().order_by('-date')

    # Applying pagination
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, "network/allposts.html", {
    "posts": posts,
    })

def profile(request, profile):
    # Accessing the user
    user = User.objects.get(pk=profile)

    # Filtering posts for that user
    posts = Post.objects.filter(user=profile).order_by('-date')

    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    # Save the user followers and following list in a variable

    follow = user.followers.all()


    # If request is POST
    if request.method == "POST" and 'unfollow' in request.POST:


        # Check if the request user is in the user list followers
        if request.user in follow:

            # Try to remove the request user from the user followers list
            user.followers.remove(request.user)
            # Try to remove the user from the request user following list
            request.user.following.remove(user)

            # Redirect to follow's page
            return HttpResponseRedirect(reverse('follow', args=[request.user.id]))

            # If is not in the list
    elif request.method == "POST" and 'follow' in  request.POST:

        # Add them to the list
        user.followers.add(request.user)
        request.user.following.add(user)
        # Redirect to follow's page

        return HttpResponseRedirect(reverse('follow', args=[request.user.id]))


    return render(request, "network/profile.html", {
    "user": user,
    "posts": posts,
    "f": user.following.all(),
    "f2": follow

    })


def follow(request, profile):

    # Accessing user
    profile = User.objects.get(pk=profile)

    # Filtering the posts of the members in request user following list
    posts = Post.objects.filter(user__in=profile.following.all()).order_by('-date')

    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, "network/follow.html", {
    "profile": profile,
    "posts": posts,
    "f": follow

    })

@csrf_exempt
def edit(request, post_id):

    # Get the Post by its ID
    post = Post.objects.get(pk=post_id)

    # Requiring a request POST
    if request.method != "POST":
        return JsonResponse({"error": "Request POST required"}, status=400)

    # Get the Post's Content
    data = json.loads(request.body)
    p = data.get("post", "")

    # Updating and saving the Post
    post.post = p
    post.save()

    return JsonResponse({"message": "Post updated successfully!"}, status=201)





@csrf_exempt
def likes(request, post_id):

    # Get the post
    post = Post.objects.get(pk=post_id)

    # Get the field "like"
    like = post.like.all()

    # Check if request user has liked the post before
    if request.user in like:

        # Then try to remove it from the like list
        post.like.remove(request.user)

    else:

        # Otherwise, add the request user in the like list
        post.like.add(request.user)

    return JsonResponse(post.serialize())




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
