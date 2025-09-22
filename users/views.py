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