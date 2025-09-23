from django import forms

from reviews.models import Book, Review

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'body', 'rating']

