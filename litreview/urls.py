"""litreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import users.views
from users.views import ProfileRedirectLoginView
import reviews.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", ProfileRedirectLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", users.views.signup_page, name="signup"),
    path("ajax/username-available/", users.views.username_available, name="username_available"),
    path("ajax/email-available/", users.views.email_available, name="email_available"),
    path("", reviews.views.home, name="home"),
    path("recent-reviews/", reviews.views.recent_reviews, name="recent_reviews"),
    path("search/", reviews.views.search, name="search"),
    path('books/<int:book_id>/', reviews.views.book_detail, name='book_detail'),
    path('books/add/', reviews.views.book_create, name='book_create'),
    path('books/<int:book_id>/reviews/add/', reviews.views.review_create, name='review_create'),
    path('books/<int:book_id>/reviews/<int:review_id>/edit/', reviews.views.review_edit, name='review_edit'),
    path('books/<int:book_id>/reviews/<int:review_id>/delete/', reviews.views.review_delete, name='review_delete'),
    path('users/<str:username>/', users.views.user_profile, name='user_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
