"""BookFreeks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from books.views import BookView, LoginView, CreateUserView, BookListView, AuthorListView, AuthorView, \
    LandingPageView, SearchResultsView, LogoutView, CreateBookView, BooksInCategoryView

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing_page'),
    path('admin/', admin.site.urls),
    path('books/<int:book_id>', BookView.as_view(), name='book'),
    path('login', LoginView.as_view(), name='login'),
    path('register', CreateUserView.as_view(), name='register'),
    path('books', BookListView.as_view(), name='books'),
    path('authors', AuthorListView.as_view(), name='authors'),
    path('authors/<int:author_id>', AuthorView.as_view(), name='author'),
    path('search_result', SearchResultsView.as_view(), name='search_result'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('create_book', CreateBookView.as_view(), name='create_book'),
    path('books_in_category/<int:category_id>', BooksInCategoryView.as_view(), name='books_in_category')
]
