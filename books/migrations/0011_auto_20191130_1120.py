# Generated by Django 2.2.6 on 2019-11-30 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0010_auto_20191130_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_author',
            field=models.ManyToManyField(related_name='book_author', to='books.Author'),
        ),
        migrations.AlterField(
            model_name='book',
            name='book_category',
            field=models.ManyToManyField(related_name='book_category', to='books.Category'),
        ),
    ]
