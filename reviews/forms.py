from django import forms

from reviews.models import Book, Review

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'