# Generated by Django 2.2.6 on 2019-11-25 15:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0007_remove_author_average_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavouriteBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when_changed', models.DateTimeField(auto_now=True)),
                ('favourite', models.BooleanField(default=False)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fav_book', to='books.Book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fav_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
