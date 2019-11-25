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
    LandingPageView, SearchResultsView, LogoutView, CreateBookView, BooksInCategoryView, CreateAuthorView, \
    CreateCategoryView, ModifyAuthorView, ModifyCategoryView, DeleteBookView, DeleteAuthorView, RateBookView, \
    ModifyBookView, DeleteCategoryView, FavouriteBookView, RatedByUserView, LikedByUserView

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
    path('books_in_category/<int:category_id>', BooksInCategoryView.as_view(), name='books_in_category'),
    path('create_author', CreateAuthorView.as_view(), name='create_author'),
    path('create_category', CreateCategoryView.as_view(), name='create_category'),
    path('modify_author/<int:pk>', ModifyAuthorView.as_view(), name='modify_author'),
    path('modify_category/<int:pk>', ModifyCategoryView.as_view(), name='modify_category'),
    path('modify_book/<int:pk>', ModifyBookView.as_view(), name='modify_book'),
    path('delete_book/<int:pk>', DeleteBookView.as_view(), name='delete_book'),
    path('delete_author/<int:pk>', DeleteAuthorView.as_view(), name='delete_author'),
    path('delete_category/<int:pk>', DeleteCategoryView.as_view(), name='delete_category'),
    path('book_rate/<int:book_id>/<int:rating>', RateBookView.as_view(), name='rate_book'),
    path('book_fav/<int:book_id>/<int:fav>', FavouriteBookView.as_view(), name='fav_book'),
    path('books/rated_by_you', RatedByUserView.as_view(), name='rated_by_user'),
    path('books/liked_by_you', LikedByUserView.as_view(), name='liked_by_user'),
]
