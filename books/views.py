from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from books.forms import LoginForm, CreateUserForm
from books.models import Book


class BookView(View):
    def get(self, request, book_id):
        book = Book.objects.get(id=book_id)
        category = book.category_set.all()
        author = book.book_author.all()
        return render(request, "book_view.html", {"book": book, "category": category, "author": author})


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


class BooksView(View):
    def get(self, request):
        books = Book.objects.all().order_by("title")
        return render(request, "books.html", {"books": books})
