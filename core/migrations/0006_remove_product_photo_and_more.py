# Generated by Django 4.2.1 on 2023-05-12 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_product_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='photo',
        ),
        migrations.AddField(
            model_name='product',
            name='a7b720d6-28bc-40e7-9764-3a5f7d0ba4be',
            field=models.ImageField(blank=True, upload_to='product_images', verbose_name='Фото продукта'),
        ),
    ]
