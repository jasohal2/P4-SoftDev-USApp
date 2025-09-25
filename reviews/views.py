"""Views for search, home feeds, and CRUD in the reviews app.
"""

from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from users.models import User
from reviews.forms import BookForm, ReviewForm
from .models import Book, Review

def search(request):
    """Search users and books by query string.

    - Users: excludes current user when authenticated, annotated with
      review/follow counts.
    - Books: annotated with average rating and review count.
    """
    query = request.GET.get('q', '').strip()
    users = books = None
    if query:
        if request.user.is_authenticated:
            users = (
                User.objects.filter(
                    Q(first_name__icontains=query) |
                    Q(last_name__icontains=query) |
                    Q(username__icontains=query)
                )
                .exclude(pk=request.user.pk)
                .annotate(
                    review_count=Count('review', distinct=True),
                    followers_count=Count('followers', distinct=True),
                    following_count=Count('following', distinct=True),
                )  # aggregated counts
                .order_by('username')
            )
        books = (
            Book.objects.filter(title__icontains=query)
            .annotate(
                avg_rating=Avg('review__rating'),
                review_count=Count('review', distinct=True),
            )
            .order_by('title')
        )
    context = {'users': users, 'books': books, 'query': query}
    return render(request, 'reviews/search.html', context)

def home(request):
    """Render the home feed.

    feed can be 'following' or 'recent'; default to following for
    signed-in users, recent for guests.
    """
    feed = request.GET.get('feed')
    context = {}
    if request.user.is_authenticated:
        if feed not in ('following', 'recent'):
            feed = 'following'
        following_users = request.user.following.all()
        following_reviews = (
            Review.objects.filter(Q(user__in=following_users))
            .select_related('book', 'user')
            .order_by('-created')
        )
        recent_reviews = (
            Review.objects.select_related('book', 'user').order_by('-created')[:10]
        )
        context['feed'] = feed
        context['following_reviews'] = following_reviews
        context['recent_reviews'] = recent_reviews
    else:
        # guests always see recent reviews
        recent_reviews = Review.objects.select_related('book', 'user').order_by('-created')[:10]
        context['feed'] = 'recent'
        context['recent_reviews'] = recent_reviews
    return render(request, "reviews/home.html", context)

@login_required
def recent_reviews(request):
    """Show top-rated reviews for logged-in users (legacy page)."""
    reviews = Review.objects.select_related('book', 'user').order_by('-rating', '-created')[:10]
    return render(request, "reviews/recent_reviews.html", {"reviews": reviews})

def book_detail(request, book_id):
    """Display book detail and its reviews."""
    book = get_object_or_404(Book, id=book_id)
    reviews = book.review_set.select_related('user').all()
    return render(request, "reviews/book.html", context={"book": book, "reviews": reviews})

@login_required
def book_create(request):
    """Create a new book (title, cover, description)."""
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
    """Create a review for a given book."""
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

@login_required
def review_edit(request, book_id, review_id):
    """Edit an existing review owned by the user."""
    book = get_object_or_404(Book, id=book_id)
    review = get_object_or_404(Review, id=review_id, user=request.user, book=book)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("book_detail", book_id=book.id)
    else:
        form = ReviewForm(instance=review)
    return render(request, "reviews/review_edit.html", {"form": form, "book": book})

@login_required
def review_delete(request, book_id, review_id):
    """Delete a review (POST only), scoped to the owner and book.

    GET returns a fallback confirmation template.
    """
    book = get_object_or_404(Book, id=book_id)
    review = get_object_or_404(Review, id=review_id, user=request.user, book=book)
    if request.method == "POST":
        review.delete()
        return redirect("book_detail", book_id=book.id)
    else:
        form = ReviewForm(instance=review)
        return render(request, "reviews/review_delete.html", {"form": form, "book": book})