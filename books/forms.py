from django import forms
from books.models import Author, Category


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
    authors_options = []
    for author in authors:
        authors_options.append([author.pk, author.name + " " + author.surname])
    authors_options.append([None, "Add new author"])
    title = forms.CharField(max_length=124)
    isbn = forms.CharField(max_length=13)
    authors = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=tuple(authors_options))
    categories = forms.ModelMultipleChoiceField(Category.objects.all())
    author_name = forms.CharField(max_length=124, required=False)
    author_surname = forms.CharField(max_length=124, required=False)

