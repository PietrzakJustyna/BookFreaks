# Generated by Django 2.2.6 on 2019-11-16 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20191116_1809'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='is_favourite',
        ),
        migrations.RemoveField(
            model_name='book',
            name='is_favourite',
        ),
    ]
