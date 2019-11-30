from random import randint

from django.test import TestCase
from faker import Faker

from books.models import Author, Book, Category, Rating


class BookTestCase(TestCase):

    def setUp(self):
        """Populate test database with random data."""
        self.faker = Faker("pl_PL")
        for _ in range(5):
            Author.objects.create(name=self.faker.first_name(), surname=self.faker.last_name())
        for _ in range(3):
            self._create_fake_book()
        for _ in range(3):
            Category.objects.create(category_name=self.faker.word())

    # def _random_author(self):
    #     """Return a random Author object from db."""
    #     authors = Author.objects.all()
    #     return authors[randint(0, len(authors) - 1)]
    #
    # def _find_author_by_name(self, name):
    #     """Return the first `Author` object that matches `name`."""
    #     return Author.objects.filter(name=name).first()

    def _fake_book_data(self):
        """Generate a dict of book data
        """
        book_data = {
            "title": self.faker.sentence(),
            "isbn": int(self.faker.random_int(min=1000, max=9999, step=1)),
            # "book_author": self._random_author().name,
            # "book_category": self.faker.word(),
            "average_rating": 0,
        }
        return book_data

    def _create_fake_book(self):
        """Generate new fake book and save to database."""
        book_data = self._fake_book_data()
        new_book = Book.objects.create(**book_data)

    def _create_fake_author(self):
        author_data = {
            "name": self.faker.first_name(),
            "surname": self.faker.last_name(),
        }
        new_auhor = Author.objects.create(**author_data)

    def test_add_book(self):
        books_before = Book.objects.count()
        self._create_fake_book()
        self.assertEqual(Book.objects.count(), books_before + 1)

    def test_delete_book(self):
        books_before = Book.objects.count()
        Book.objects.first().delete()
        self.assertEqual(Book.objects.count(), books_before-1)

    def test_add_author(self):
        authors_before = Author.objects.count()
        self._create_fake_author()
        self.assertEqual(Author.objects.count(), authors_before + 1)

    def test_delete_author(self):
        authors_before = Author.objects.count()
        Author.objects.first().delete()
        self.assertEqual(Author.objects.count(), authors_before-1)

    def test_add_category(self):
        categories_before = Category.objects.count()
        Category.objects.create(category_name=self.faker.word())
        self.assertEqual(Category.objects.count(), categories_before+1)

    def test_delete_category(self):
        categories_before = Category.objects.count()
        Category.objects.first().delete()
        self.assertEqual(Category.objects.count(), categories_before-1)

    def test_adding_rating(self):
        book = Book.objects.first()
        current_average_rating = book.average_rating
        book.book_rating.set(5)
        self.assertEqual(book.average_rating, 5)



