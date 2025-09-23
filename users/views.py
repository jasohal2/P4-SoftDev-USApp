from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from users.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect

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