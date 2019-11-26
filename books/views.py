from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import Group, User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, FormView, UpdateView, DeleteView
from books.forms import LoginForm, CreateUserForm, CreateBookForm
from books.models import Book, Author, Category, Rating, FavouriteBook


class LandingPageView(View):
    def get(self, request):
        ten_best_rated_books = Book.objects.all().order_by("average_rating").reverse()[:10]
        return render(request, "landing_page.html", {"ten_best_rated_books": ten_best_rated_books})


class CreateUserView(View):
    def get(self, request):
        logout(request)
        form = CreateUserForm()
        return render(request, "create_user.html", {'form': form})

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                password_repeat = form.cleaned_data['password_repeat']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']

                if password == password_repeat:
                    user = User.objects.create_user(username=username, email=email, password=password,
                                                    first_name=first_name, last_name=last_name)

                    group = Group.objects.get(name='Users')
                    user.groups.add(group)

                    return redirect(reverse("login"))
                else:
                    messages.warning(request, "Passwords given are not the same")
                    return redirect(reverse("register"))
            except IntegrityError:
                messages.warning(request, "User with this username already exists")
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


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")


class BookView(View):
    def get(self, request, book_id):
        try:
            current_rating = Rating.objects.get(book_id=book_id, user_id=request.user.id)
            book = get_object_or_404(Book, pk=book_id)
            return render(request, "book_view.html", {"book": book, "current_rating": current_rating})
        except ObjectDoesNotExist:
            book = get_object_or_404(Book, pk=book_id)
            return render(request, "book_view.html", {"book": book})


class BookListView(View):
    def get(self, request):

        how = self.request.GET.get("how")

        if how == "rating-asc":
            books = Book.objects.all().order_by("average_rating")
        elif how == "alpha-asc":
            books = Book.objects.all().order_by("title")
        elif how == "rating-desc":
            books = Book.objects.all().order_by("average_rating").reverse()
        else:
            books = Book.objects.all().order_by("title").reverse()

        paginator = Paginator(books, 10)
        page = request.GET.get('page')
        books_per_page = paginator.get_page(page)
        return render(request, "books.html", {"books": books_per_page})


class AuthorView(View):
    def get(self, request, author_id):
        author = Author.objects.get(id=author_id)
        books = author.books.all()
        return render(request, "author_view.html", {"author": author, "books": books})


class AuthorListView(View):
    def get(self, request):
        authors = Author.objects.all().order_by("surname")
        paginator = Paginator(authors, 10)
        page = request.GET.get('page')
        authors_per_page = paginator.get_page(page)
        return render(request, "authors.html", {"authors": authors_per_page})


class BooksInCategoryView(View):
    def get(self, request, category_id):

        category = Category.objects.get(id=category_id)
        how = self.request.GET.get("how")

        if how == "rating-asc":
            books = Book.objects.filter(book_category=category).order_by("average_rating")
        elif how == "alpha-asc":
            books = Book.objects.filter(book_category=category).order_by("title")
        elif how == "rating-desc":
            books = Book.objects.filter(book_category=category).order_by("average_rating").reverse()
        else:
            books = Book.objects.filter(book_category=category).order_by("title").reverse()

        return render(request, "books.html", {"books": books, "category": category})


class SearchView(TemplateView):
    template_name = "base.html"


class SearchResultsView(ListView):
    model = Book
    template_name = 'search_result.html'

    def get_queryset(self):
        query = self.request.GET.get('search_input')
        object_list = Book.objects.filter(Q(title__icontains=query) |
                                          Q(book_author__name__icontains=query) |
                                          Q(book_author__surname__icontains=query))
        return object_list


class CreateBookView(PermissionRequiredMixin, FormView):
    permission_required = 'add_book'
    template_name = 'create_book.html'
    success_url = '/books'
    form_class = CreateBookForm

    def form_valid(self, form):
        title = form.cleaned_data['title']
        isbn = form.cleaned_data['isbn']
        authors = form.cleaned_data['authors']
        create_new_author = form.cleaned_data['create_new_author']
        categories = form.cleaned_data['categories']
        author_name = form.cleaned_data['author_name']
        author_surname = form.cleaned_data['author_surname']
        book = Book(title=title, isbn=isbn, average_rating=0)
        book.save()
        if create_new_author is True:
            new_author = Author(name=author_name, surname=author_surname)
            new_author.save()
            book.book_author.add(new_author)
        else:
            author_list = Author.objects.filter(pk__in=authors)
            for author in author_list:
                book.book_author.add(author)
        category_list = Category.objects.filter(pk__in=categories)
        for category in category_list:
            book.book_category.add(category)

        return redirect('books/{}'.format(book.id))


class CreateAuthorView(PermissionRequiredMixin, CreateView):
    permission_required = 'add_author'
    raise_exception = True
    permission_denied_message = 'You have to be an administrator to add new authors'
    model = Author
    template_name = 'create_author.html'
    fields = ['name', 'surname']
    success_url = 'authors'


class CreateCategoryView(PermissionRequiredMixin, CreateView):
    permission_required = 'add_category'
    raise_exception = True
    permission_denied_message = 'You have to be an administrator to add new categories'
    model = Category
    template_name = 'create_category.html'
    fields = ['category_name']
    success_url = 'books'


class ModifyAuthorView(PermissionRequiredMixin, UpdateView):
    permission_required = 'change_author'
    raise_exception = True
    permission_denied_message = 'You have to be an administrator to modify authors'
    model = Author
    template_name = 'create_author.html'
    fields = ['name', 'surname']
    success_url = reverse_lazy('authors')


class ModifyCategoryView(PermissionRequiredMixin, UpdateView):
    permission_required = 'change_category'
    raise_exception = True
    permission_denied_message = 'You have to be an administrator to modify categories'
    model = Category
    template_name = 'create_category.html'
    fields = ['category_name']
    success_url = reverse_lazy('books')


class ModifyBookView(PermissionRequiredMixin, UpdateView):
    permission_required = 'change_book'
    raise_exception = True
    permission_denied_message = 'You have to be an administrator to modify books'
    model = Book
    template_name = 'create_book.html'
    fields = ['title', 'isbn']
    success_url = reverse_lazy('books')


class DeleteBookView(PermissionRequiredMixin, DeleteView):
    permission_required = 'delete_book'
    raise_exception = True
    permission_denied_message = 'You have to be an administrator to delete books'
    model = Book
    success_url = reverse_lazy('books')
    template_name = 'confirm_delete.html'


class DeleteAuthorView(PermissionRequiredMixin, DeleteView):
    permission_required = 'delete_author'
    raise_exception = True
    permission_denied_message = 'You have to be an administrator to delete authors'
    model = Author
    success_url = reverse_lazy('authors')
    template_name = 'confirm_delete.html'


class DeleteCategoryView(PermissionRequiredMixin, DeleteView):
    permission_required = 'delete_category'
    raise_exception = True
    permission_denied_message = 'You have to be an administrator to delete categories'
    model = Category
    success_url = reverse_lazy('books')
    template_name = 'confirm_delete.html'


class RateBookView(LoginRequiredMixin, View):
    raise_exception = True

    def post(self, request, book_id, rating):
        book = get_object_or_404(Book, pk=book_id)
        rating_avg = Rating.rate(request.user, book, rating)
        return JsonResponse({"rating_avg": rating_avg})


class FavouriteBookView(LoginRequiredMixin, View):
    raise_exception = True

    def post(self, request, book_id, fav):
        book = get_object_or_404(Book, pk=book_id)
        add_to_fav = FavouriteBook.add_to_favourite(request.user, book, fav)
        return HttpResponse(status=204)


class RatedByUserView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    def get(self, request):

        user = request.user
        how = self.request.GET.get("how")

        if how == "rating-asc":
            books = Book.objects.filter(book_rating__user=user).order_by("average_rating")
        elif how == "alpha-asc":
            books = Book.objects.filter(book_rating__user=user).order_by("title")
        elif how == "rating-desc":
            books = Book.objects.filter(book_rating__user=user).order_by("average_rating").reverse()
        else:
            books = Book.objects.filter(book_rating__user=user).order_by("title").reverse()

        return render(request, "books.html", {"books": books})


class LikedByUserView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    def get(self, request):
        user = request.user

        how = self.request.GET.get("how")

        if how == "rating-asc":
            books = Book.objects.filter(fav_book__user=user).order_by("average_rating")
        elif how == "alpha-asc":
            books = Book.objects.filter(fav_book__user=user).order_by("title")
        elif how == "rating-desc":
            books = Book.objects.filter(fav_book__user=user).order_by("average_rating").reverse()
        else:
            books = Book.objects.filter(fav_book__user=user).order_by("title").reverse()

        return render(request, "books.html", {"books": books})


