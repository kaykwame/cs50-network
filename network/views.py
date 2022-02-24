import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import RedirectView
from .models import User, Posts, Followers, Likes
from django.shortcuts import get_object_or_404
from .forms import post_creation_form
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url="login")
def index(request):
    form = post_creation_form(request.POST or None)
    user = request.user
    return render(request, "network/index.html", {
    "form": form,
    "user": user,
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


@login_required
def newpost(request):
    #Make new post with 'POST' request.
    if request.method == "POST":
        form = post_creation_form(request.POST or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.Poster = request.user
            post.Poster_username = request.user.username
            post.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/index.html", {"form": form})
    else:
        form = listing_creation_form()
        return render(request, "network/index.html", {"form": post_creation_form})


@login_required(login_url="login")
def allposts(request):

    #Get all posts made and arrange them in reverse chronological order.
    posts_list = Posts.objects.all().order_by('-Date_posted')

    #Create pagination for pages with more than 10 posts.
    page = request.GET.get('page', 1)
    paginator = Paginator(posts_list, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    user = request.user
    form = post_creation_form()

    #Get the number of likes for each post in order to be rendered or html page.
    liked_post = [i for i in posts if Likes.objects.filter(user = request.user, post=i)]
    return render(request, "network/allposts.html", {
        "posts": posts,
        "user": user,
        "form": form,
        "liked_post": liked_post,
    })

@login_required(login_url="login")
def following(request):
    form = post_creation_form()

    #Get posts from users that the current user follows and arrange them in reverse chronological order.
    posts_list = Posts.objects.filter(Poster__following__follower=request.user).order_by('-Date_posted')

    #Create pagination for pages with more than 10 posts.
    page = request.GET.get('page', 1)
    paginator = Paginator(posts_list, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    #Get the number of likes for each post in order to be rendered or html page.
    liked_post = [i for i in posts if Likes.objects.filter(user=request.user, post=i)]
    return render(request, "network/following.html", {
    "posts": posts,
    "form": form,
    "liked_post": liked_post,
    })


@login_required(login_url="login")
def like(request):

    #Get id of liked post from ajax request
    post_id = request.GET.get("id", "")

    user = request.user
    post = Posts.objects.get(pk=post_id)
    liked= False

    #Get like for current user on the post
    like = Likes.objects.filter(user=user, post=post)

    #If like exists ie. user has already liked the post, delete like (or 'unlike' the post).
    if like:
        like.delete()


    #If like doesn't exist ie. user has not already liked the post, create like object (or 'like' the post).
    else:
        Likes.objects.create(user=user, post=post)
    return HttpResponse(status=204)


@csrf_exempt
@login_required(login_url="login")
def profilepage(request, poster):
    form = post_creation_form()
    otheruser = User.objects.get(username=poster)
    currentuser = request.user
    userid = otheruser.id

    #Get posts from users that the current user follows and arrange them in reverse chronological order.
    posts_list = Posts.objects.filter(Poster=userid).order_by('-Date_posted')

    #Create pagination for pages with more than 10 posts.
    page = request.GET.get('page', 1)
    paginator = Paginator(posts_list, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    #Get number of followers of user.
    followers = Followers.objects.filter(followee=userid).count()

    #Get number of people user is following.
    followees = Followers.objects.filter(follower=userid).count()

    #Get the number of likes for each post in order to be rendered or html page.
    liked_post = [i for i in posts if Likes.objects.filter(user=request.user, post=i)]

    if Followers.objects.filter(followee=otheruser, follower=request.user).exists():
        follow_status = "True"
        return render(request, "network/profilepage.html", {
        "otheruser": otheruser,
        "currentuser": currentuser,
        "follow_status": follow_status,
        "posts": posts,
        "poster": poster,
        "form": form,
        "liked_post": liked_post,
        "followers": followers,
        "followees": followees
        })
    else:
        follow_status = "False"
        return render(request, "network/profilepage.html", {
        "follow_status": follow_status,
        "otheruser": otheruser,
        "currentuser": currentuser,
        "posts": posts,
        "poster": poster,
        "form": form,
        "liked_post": liked_post,
        "followers": followers,
        "followees": followees
        })


@login_required(login_url="login")
def follow(request, userid):
    otheruser = User.objects.get(id=userid)

    #Insert new follower in 'Followers' model.
    Followers(followee=otheruser, follower=request.user).save()
    poster = User.objects.get(pk=userid).username
    return HttpResponseRedirect(reverse("profilepage", args=(poster, )))


@login_required(login_url="login")
def unfollow(request, userid):
    otheruser = User.objects.get(id=userid)

    #Delete follower from 'Followers' model.
    Followers.objects.get(followee=otheruser, follower=request.user).delete()
    poster = User.objects.get(pk=userid).username
    return HttpResponseRedirect(reverse("profilepage", args=(poster, )))


#API view to get or update post data.
@csrf_exempt
@login_required(login_url="login")
def post(request, post_id):

    # Query for requested post
    try:
        post = Posts.objects.get(pk=post_id)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update post with new contents
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("Post_content") is not None:
            post.Post_content = data["Post_content"]
            post.save()
            return HttpResponse(status=204)

    #Request must be via GET or PUT
    else:
        return JsonResponse({
        "error": "GET or PUT request required."
    }, status=400)
