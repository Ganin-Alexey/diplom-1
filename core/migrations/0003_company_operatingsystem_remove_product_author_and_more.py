# Generated by Django 4.2.1 on 2023-05-09 17:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('languages_plus', '0004_auto_20171214_0004'),
        ('core', '0002_user_is_staff'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=240, unique=True, verbose_name='Название создателя ПО')),
            ],
        ),
        migrations.CreateModel(
            name='OperatingSystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Название операционный системы')),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='author',
        ),
        migrations.AddField(
            model_name='product',
            name='languages',
            field=models.ManyToManyField(blank=True, related_name='products', to='languages_plus.language', verbose_name='Языки'),
        ),
        migrations.AlterField(
            model_name='product',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='product',
            name='date_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание ПО'),
        ),
        migrations.AlterField(
            model_name='product',
            name='meta_description',
            field=models.CharField(blank=True, max_length=150, verbose_name='Мета-Описание ПО'),
        ),
        migrations.AlterField(
            model_name='product',
            name='publish_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='product',
            name='published',
            field=models.BooleanField(default=True, verbose_name='Опубликован?'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='Слаг'),
        ),
        migrations.AlterField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, related_name='products', to='core.tag', verbose_name='Теги'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=255, unique=True, verbose_name='Название ПО'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, max_length=240, verbose_name='ФИО'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='website',
            field=models.URLField(blank=True, verbose_name='Сайт URL'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Название тега'),
        ),
        migrations.AddField(
            model_name='product',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.company', verbose_name='Создатель ПО'),
        ),
        migrations.AddField(
            model_name='product',
            name='operating_systems',
            field=models.ManyToManyField(blank=True, related_name='products', to='core.operatingsystem', verbose_name='Операционные системы'),
        ),
    ]
