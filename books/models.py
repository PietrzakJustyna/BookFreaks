from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models

# Create your models here.
from django.db.models import Avg
from django.db.models.signals import post_save


class Book(models.Model):
    title = models.CharField(max_length=124)
    isbn = models.CharField(max_length=13, unique=True, null=True)
    average_rating = models.FloatField()

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=124)
    surname = models.CharField(max_length=124)
    books = models.ManyToManyField(Book, related_name="book_author")

    def __str__(self):
        return "{} {}".format(self.name, self.surname)


class Category(models.Model):
    category_name = models.CharField(max_length=124)
    books = models.ManyToManyField(Book, related_name="book_category")

    def __str__(self):
        return self.category_name


class Rating(models.Model):
    rating = models.IntegerField(validators=[MaxValueValidator(5)], default=0)
    book = models.ForeignKey(Book, related_name="book_rating", on_delete=models.CASCADE)
    when_rated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)

    @classmethod
    def rate(cls, who, what_book, how_much):
        obj, created = cls.objects.get_or_create(user=who, book=what_book)
        obj.rating = how_much
        obj.save()
        return obj.book.average_rating


def book_rating_saved(instance, **kwargs):
    book = instance.book
    book.average_rating = round(book.book_rating.all().aggregate(Avg('rating'))['rating__avg'], 1)
    book.save()


post_save.connect(book_rating_saved, sender=Rating)


class FavouriteBook(models.Model):
    when_changed = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="fav_user", on_delete=models.CASCADE)
    favourite = models.BooleanField(default=False)
    book = models.ForeignKey(Book, related_name="fav_book", on_delete=models.CASCADE)

    @classmethod
    def add_to_favourite(cls, who, what_book, fav):
        obj, created = cls.objects.get_or_create(user=who, book=what_book)
        obj.favourite = fav
        obj.save()
