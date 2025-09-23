from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from users.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import JsonResponse

from . import forms

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
    if request.method == "POST" and request.user != profile_user:
        if is_following:
            request.user.following.remove(profile_user)
        else:
            request.user.following.add(profile_user)
        return redirect('user_profile', username=profile_user.username)
    return render(request, "users/profile.html", {"profile_user": profile_user, "is_following": is_following})