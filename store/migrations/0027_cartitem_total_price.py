# Generated by Django 3.2.8 on 2022-01-15 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0026_order_braintree_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
    ]
