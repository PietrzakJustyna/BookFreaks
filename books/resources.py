from import_export import resources
from books.models import Book


class BookResource(resources.ModelResource):
    class Meta:
        model = Book
