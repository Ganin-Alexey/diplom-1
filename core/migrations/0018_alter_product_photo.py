# Generated by Django 4.2.1 on 2023-05-27 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_alter_product_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(blank=True, upload_to='product_images/662d05b0-efe1-44ba-90e6-1094a7527393', verbose_name='Фото продукта'),
        ),
    ]