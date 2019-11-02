from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=124)


class Author(models.Model):
    name = models.CharField(max_length=124)
    surname = models.CharField(max_length=124)
    books = models.ManyToManyField(Book)


class Category(models.Model):
    category_name = models.CharField(max_length=124)
    books = models.ManyToManyField(Book)


class Rating(models.Model):
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    book = models.ManyToManyField(Book)
    when_rated = models.DateTimeField(auto_now=True)
    user = models.ManyToManyField(User)

