# Generated by Django 3.2.8 on 2022-01-15 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_auto_20220115_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='items',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.order'),
        ),
    ]
