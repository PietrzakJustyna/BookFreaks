from django.contrib.auth.models import User, Permission, Group
from django.test import TestCase
from faker import Faker

from books.models import Author, Book, Category, Rating, FavouriteBook


class BookTestCase(TestCase):

    def setUp(self):
        """Populate test database with random data."""
        self.faker = Faker("pl_PL")
        for _ in range(3):
            Author.objects.create(name=self.faker.first_name(), surname=self.faker.last_name())
        for _ in range(3):
            self._create_fake_book()
        for _ in range(3):
            Category.objects.create(category_name=self.faker.word())
        for _ in range(3):
            self._create_fake_user()

        Group.objects.create(name="Users")

    def _create_fake_user(self):
        new_user = User.objects.create_user(self.faker.word(), self.faker.email(), '12345678')

    def _fake_book_data(self):
        """Generate a dict of book data
        """
        book_data = {
            "title": self.faker.sentence(),
            "isbn": int(self.faker.random_int(min=1000, max=9999, step=1)),
            "average_rating": 0.0,
        }
        return book_data

    def _create_fake_book(self):
        """Generate new fake book and save to database."""
        book_data = self._fake_book_data()
        new_book = Book.objects.create(**book_data)

    def test_add_book_user_has_permissions(self):
        books_before = Book.objects.count()

        user = User.objects.first()
        permission_needed = Permission.objects.get(name="Can add book")
        user.user_permissions.add(permission_needed)
        self.client.login(username=user.username, password="12345678")

        response = self.client.post("/create_book", {"title": self.faker.word(),
                                                     "isbn": self.faker.random_int(min=1000, max=9999, step=1),
                                                     "create_new_author": False,
                                                     "authors": Author.objects.first().pk,
                                                     "categories": Category.objects.first().pk,
                                                     "average_rating": 0.0})

        self.assertEqual(Book.objects.count(), books_before + 1)

    def test_add_book_no_permission(self):
        books_before = Book.objects.count()

        user = User.objects.first()
        self.client.login(username=user.username, password="12345678")

        response = self.client.post("/create_book", {"title": self.faker.word(),
                                                     "isbn": self.faker.random_int(min=1000, max=9999, step=1),
                                                     "create_new_author": False,
                                                     "authors": Author.objects.first().pk,
                                                     "categories": Category.objects.first().pk,
                                                     "average_rating": 0.0})

        self.assertEqual(Book.objects.count(), books_before)

    def test_delete_book(self):
        books_before = Book.objects.count()
        book = Book.objects.first()
        user = User.objects.first()
        permission_needed = Permission.objects.get(name="Can delete book")
        user.user_permissions.add(permission_needed)
        self.client.login(username=user.username, password="12345678")
        response = self.client.post("/delete_book/{}".format(book.pk))
        self.assertEqual(Book.objects.count(), books_before - 1)

    def test_add_author(self):
        authors_before = Author.objects.count()

        user = User.objects.first()
        permission_needed = Permission.objects.get(name="Can add author")
        user.user_permissions.add(permission_needed)
        self.client.login(username=user.username, password="12345678")

        author_data = {
            "name": self.faker.first_name(),
            "surname": self.faker.last_name(),
        }
        response = self.client.post("/create_author", author_data)

        self.assertEqual(Author.objects.count(), authors_before + 1)

    def test_delete_author(self):
        authors_before = Author.objects.count()
        author = Author.objects.first()
        user = User.objects.first()
        permission_needed = Permission.objects.get(name="Can delete author")
        user.user_permissions.add(permission_needed)
        self.client.login(username=user.username, password="12345678")
        response = self.client.post("/delete_author/{}".format(author.pk))
        self.assertEqual(Author.objects.count(), authors_before - 1)

    def test_add_category(self):
        categories_before = Category.objects.count()

        user = User.objects.first()
        permission_needed = Permission.objects.get(name="Can add category")
        user.user_permissions.add(permission_needed)
        self.client.login(username=user.username, password="12345678")

        response = self.client.post("/create_category", {"category_name": self.faker.word()})
        self.assertEqual(Category.objects.count(), categories_before + 1)

    def test_delete_category(self):
        categories_before = Category.objects.count()
        category = Category.objects.first()

        user = User.objects.first()
        permission_needed = Permission.objects.get(name="Can delete category")
        user.user_permissions.add(permission_needed)
        self.client.login(username=user.username, password="12345678")

        response = self.client.post("/delete_category/{}".format(category.pk))
        self.assertEqual(Category.objects.count(), categories_before - 1)

    def test_add_new_user(self):
        users_before = User.objects.count()
        response = self.client.post("/register", {"username": self.faker.word(),
                                                  "password": "olaola",
                                                  "password_repeat": "olaola",
                                                  "first_name": self.faker.first_name(),
                                                  "last_name": self.faker.last_name(),
                                                  "email": self.faker.email()})
        self.assertEqual(User.objects.count(), users_before + 1)

    def test_login_user(self):
        user = User.objects.first()
        response = self.client.post("/login", {"user": user.username, "password": "12345678"})
        self.assertEqual(response.status_code, 302)

    def test_average_rating(self):
        book = Book.objects.first()
        user = User.objects.first()
        rating, new_rating = Rating.objects.get_or_create(book_id=book.pk, user_id=user.pk)
        rating.rating = 5
        rating.save()
        book.refresh_from_db()
        self.assertEqual(book.average_rating, 5)

    def test_favourite(self):
        book = Book.objects.last()

        user = User.objects.first()
        permission_needed = Permission.objects.get(name="Can add favourite book")
        user.user_permissions.add(permission_needed)
        self.client.login(username=user.username, password="12345678")

        response = self.client.post("/book_fav/{}/{}".format(book.pk, 1))

        books = Book.objects.filter(fav_book__user=user)
        self.assertEqual(len(books), 1)

    def test_modify_category(self):
        category = Category.objects.last()

        user = User.objects.first()
        permission_needed = Permission.objects.get(name="Can change category")
        user.user_permissions.add(permission_needed)
        self.client.login(username=user.username, password="12345678")

        response = self.client.post("/modify_category/{}".format(category.pk), {"category_name": "nowa nazwa"})
        category.refresh_from_db()
        self.assertEqual(category.category_name, "nowa nazwa")
