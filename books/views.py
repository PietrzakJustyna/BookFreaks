from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView

from books.forms import LoginForm, CreateUserForm, SearchForm
from books.models import Book, Author, Category


class LandingPageView(View):
    def get(self, request):
        ctx = None
        return render(request, "landing_page.html", {"ctx": ctx})


class CreateUserView(View):
    def get(self, request):
        form = CreateUserForm()
        return render(request, "create_user.html", {'form': form})

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password_repeat = form.cleaned_data['password_repeat']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            if password == password_repeat:
                User.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                         last_name=last_name)
                return redirect(reverse("login"))
            else:
                return redirect(reverse("register"))


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect(reverse('books'))
            form.add_error(None, "Zły login lub hasło")
        return render(request, "login.html", {'form': form})


class BookView(View):
    def get(self, request, book_id):
        book = Book.objects.get(id=book_id)
        category = book.category_set.all()
        author = book.book_author.all()
        return render(request, "book_view.html", {"book": book, "category": category, "author": author})


class BookListView(View):
    def get(self, request):
        books = Book.objects.all().order_by("title")
        return render(request, "books.html", {"books": books})


class AuthorView(View):
    def get(self, request, author_id):
        author = Author.objects.get(id=author_id)
        books = author.books.all()
        return render(request, "author_view.html", {"author": author, "books": books})


class AuthorListView(View):
    def get(self, request):
        authors = Author.objects.all().order_by("surname")
        return render(request, "authors.html", {"authors": authors})


class SearchView(TemplateView):
    template_name = "base.html"


class SearchResultsView(ListView):
    model = Book
    template_name = 'search_result.html'

    def get_queryset(self):
        query = self.request.GET.get('search_input')
        object_list = Book.objects.filter(Q(title__icontains=query) |
                                          Q(book_author__name__icontains=query) |
                                          Q(book_author__surname__icontains=query) |
                                          Q(category__category_name__icontains=query))
        return object_list

