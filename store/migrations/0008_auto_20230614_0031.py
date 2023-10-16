# Generated by Django 3.2.18 on 2023-06-13 19:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20230614_0005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlistitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='wishlistitem',
            name='whishlist_quantity',
        ),
        migrations.AddField(
            model_name='wishlistitem',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]