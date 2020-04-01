from import_export import resources
from books.models import Book, Category, Author
from import_export.fields import Field
from import_export.widgets import ManyToManyWidget


class BookResource(resources.ModelResource):
    book_category = Field(attribute='book_category', widget=ManyToManyWidget(Category, field='category_name'))
    book_author = Field(attribute='book_author', widget=ManyToManyWidget(Author))

    class Meta:
        model = Book
        fields = ('isbn', 'title', 'book_author', 'book_category', 'average_rating')
        export_order = fields

    def dehydrate_book_author(self, book):
        authors = ['{} {}'.format(author.name, author.surname) for author in book.book_author.all()]
        return ','.join(authors)
