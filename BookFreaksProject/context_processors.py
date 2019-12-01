from django.utils import timezone
from books.models import Category, Book


def book_categories_processor(request):
    categories = Category.objects.all().order_by("category_name")
    return {"categories": categories}


def date_processor(request):
    today = timezone.now().date()
    return {"today": today}
