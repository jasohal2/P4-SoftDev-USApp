from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from users.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import JsonResponse

from . import forms
from reviews.models import Review

def signup_page(request):
    form = forms.SignUpForm()
    if request.method == "POST":
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    return render(request, "authentication/signup.html", {"form": form})

def username_available(request):
    """AJAX endpoint to check if a username is available.
    Query param: ?username=foo
    Returns JSON: {"available": true/false}
    Always returns 200 to simplify client logic.
    """
    username = request.GET.get("username", "").strip()
    available = bool(username) and not User.objects.filter(username__iexact=username).exists()
    return JsonResponse({"available": available, "username": username})

def email_available(request):
    """AJAX endpoint to check if an email is available.
    Query param: ?email=foo@example.com
    Returns JSON: {"available": true/false}
    Always 200.
    Empty email returns available=false to prompt entry.
    """
    email = request.GET.get("email", "").strip()
    if not email:
        return JsonResponse({"available": False, "email": email})
    available = not User.objects.filter(email__iexact=email).exists()
    return JsonResponse({"available": available, "email": email})

@login_required
def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    is_following = request.user.following.filter(pk=profile_user.pk).exists()
    user_search_results = []
    search_query = ''
    # Handle user search when viewing own profile (GET request with user_query)
    if request.user == profile_user and request.method == 'GET':
        search_query = request.GET.get('user_query', '').strip()
        if search_query:
            # Basic case-insensitive contains search on username or full name parts
            from django.db.models import Q
            qs = User.objects.filter(
                Q(username__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            ).exclude(pk=request.user.pk).order_by('username')[:25]
            user_search_results = list(qs)
    if request.method == "POST":
        # Per-user unfollow from own profile (list of people you follow)
        unfollow_username = request.POST.get('unfollow_username')
        follow_username = request.POST.get('follow_username')
        if unfollow_username and request.user == profile_user:
            target = User.objects.filter(username=unfollow_username).first()
            if target and request.user.following.filter(pk=target.pk).exists():
                request.user.following.remove(target)
            return redirect('user_profile', username=profile_user.username)
        if follow_username and request.user == profile_user:
            target = User.objects.filter(username=follow_username).first()
            if target and target != request.user and not request.user.following.filter(pk=target.pk).exists():
                request.user.following.add(target)
            return redirect('user_profile', username=profile_user.username)

        # Follow/unfollow the profile user (when viewing someone else's profile)
        if request.user != profile_user:
            if is_following:
                request.user.following.remove(profile_user)
            else:
                request.user.following.add(profile_user)
            return redirect('user_profile', username=profile_user.username)
    reviews = Review.objects.filter(user=profile_user).select_related('book').order_by('-created')
    following_ids = set(request.user.following.values_list('id', flat=True)) if request.user.is_authenticated else set()
    return render(request, "users/profile.html", {"profile_user": profile_user, "is_following": is_following, "reviews": reviews, "following_ids": following_ids, "user_search_results": user_search_results, "user_search_query": search_query})