# Generated by Django 3.2.8 on 2021-12-25 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20211225_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='images1',
            field=models.FileField(upload_to='products/%Y/%m/%d'),
        ),
    ]