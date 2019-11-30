from django import forms
from books.models import Author, Category, Book


class LoginForm(forms.Form):
    user = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CreateUserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_repeat = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()


class SearchForm(forms.Form):
    search_input = forms.CharField(required=False)


class CreateBookForm(forms.Form):
    authors = Author.objects.all()
    create_new_author = forms.BooleanField(required=False)
    author_name = forms.CharField(max_length=124, required=False)
    author_surname = forms.CharField(max_length=124, required=False)
    title = forms.CharField(max_length=124)
    isbn = forms.CharField(max_length=13)
    authors = forms.ModelMultipleChoiceField(authors, required=False)
    categories = forms.ModelMultipleChoiceField(Category.objects.all())


class UpdateBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields ="__all__"
