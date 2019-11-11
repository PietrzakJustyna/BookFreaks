from books.models import Category, Book


def book_categories_processor(request):
    categories = Category.objects.all()
    return {"categories": categories}
