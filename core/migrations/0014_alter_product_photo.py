# Generated by Django 4.2.1 on 2023-05-25 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_company_options_alter_operatingsystem_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(blank=True, upload_to='product_images/76020d28-4459-4917-9c67-e05f56b83dd6', verbose_name='Фото продукта'),
        ),
    ]
