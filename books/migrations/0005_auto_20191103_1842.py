# Generated by Django 2.2.6 on 2019-11-03 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_auto_20191103_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]