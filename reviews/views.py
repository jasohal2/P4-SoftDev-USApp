from users.models import User
from django.db.models import Q

def search(request):
    query = request.GET.get('q', '').strip()
    users = books = None
    if query:
        if request.user.is_authenticated:
            users = User.objects.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(username__icontains=query)
            ).exclude(pk=request.user.pk)
        books = Book.objects.filter(title__icontains=query)
    context = {'users': users, 'books': books}
    return render(request, 'reviews/search.html', context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from reviews.forms import BookForm, ReviewForm
from .models import Book, Review

def home(request):
    feed = request.GET.get('feed', 'following')
    context = {}
    if request.user.is_authenticated:
        following_users = request.user.following.all()
        following_reviews = Review.objects.filter(Q(user__in=following_users)).order_by('-created')
        trending_reviews = Review.objects.order_by('-rating', '-created')[:10]
        context['feed'] = feed
        context['following_reviews'] = following_reviews
        context['trending_reviews'] = trending_reviews
    else:
        trending_reviews = Review.objects.order_by('-rating', '-created')[:10]
        context['feed'] = 'trending'
        context['trending_reviews'] = trending_reviews
    return render(request, "reviews/home.html", context)

@login_required
def recent_reviews(request):
    # Show top-rated reviews for logged-in users
    reviews = Review.objects.order_by('-rating', '-created')[:10]
    return render(request, "reviews/recent_reviews.html", {"reviews": reviews})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = book.review_set.all()
    return render(request, "reviews/book.html", context = {"book": book, "reviews": reviews})

@login_required
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            return redirect("book_detail", book_id=book.id)
    else:
        form = BookForm()
    return render(request, "reviews/book_create.html", {"form": form})

@login_required
def review_create(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect("book_detail", book_id=book.id)
    else:
        form = ReviewForm()
    return render(request, "reviews/review_create.html", {"form": form, "book": book})