from import_export import resources
from books.models import Book, Category, Author
from import_export.fields import Field
from import_export.widgets import ManyToManyWidget


class BookResource(resources.ModelResource):
    book_category = Field(attribute='book_category', widget=ManyToManyWidget(Category, field='category_name'),
                          column_name='Category')
    book_author = Field(attribute='book_author', widget=ManyToManyWidget(Author), column_name='Author')
    isbn = Field(attribute='isbn', column_name='ISBN')
    title = Field(attribute='title', column_name='Title')
    average_rating = Field(attribute='average_rating', column_name='Average rating')

    class Meta:
        model = Book
        fields = ('isbn', 'title', 'book_author', 'book_category', 'average_rating')
        export_order = fields

    def dehydrate_book_author(self, book):
        authors = ['{} {}'.format(author.name, author.surname) for author in book.book_author.all()]
        return ','.join(authors)
