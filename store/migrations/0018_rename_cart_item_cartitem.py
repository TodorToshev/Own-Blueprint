# Generated by Django 3.2.8 on 2022-01-07 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_cart_item'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Cart_Item',
            new_name='CartItem',
        ),
    ]
