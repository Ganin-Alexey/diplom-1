# Generated by Django 4.2.1 on 2023-05-12 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_company_operatingsystem_remove_product_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='photo',
            field=models.ImageField(blank=True, height_field=220, upload_to='', verbose_name='Фото продукта', width_field=370),
        ),
    ]
