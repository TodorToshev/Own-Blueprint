# Generated by Django 3.2.8 on 2021-12-27 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20211227_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sizes',
            field=models.ManyToManyField(to='store.Size'),
        ),
    ]
