from __future__ import unicode_literals
import uuid
from backend import settings
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from languages_plus.models import Language


class Company(models.Model):
    name = models.CharField(verbose_name="Название создателя ПО", max_length=240, blank=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class Tag(models.Model):
    name = models.CharField(verbose_name="Название тега", max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class OperatingSystem(models.Model):
    name = models.CharField(verbose_name="Название операционный системы", max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Операционная система'
        verbose_name_plural = 'Операционные системы'


class Product(models.Model):
    class Meta:
        ordering = ["-publish_date"]
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    title = models.CharField(verbose_name="Название ПО", max_length=255, unique=True)
    slug = models.SlugField(verbose_name="Слаг", max_length=255, unique=True)
    description = models.TextField(verbose_name="Описание ПО", blank=True)
    meta_description = models.CharField(verbose_name="Мета-Описание ПО", max_length=150, blank=True)
    price = models.DecimalField(verbose_name="Цена", decimal_places=2, max_digits=6)
    photo = models.ImageField(verbose_name="Фото продукта", blank=True, upload_to=f"product_images/{uuid.uuid4()}")
    languages = models.ManyToManyField(Language, verbose_name="Языки", related_name="products", blank=True)
    date_created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    date_modified = models.DateTimeField(verbose_name="Дата последнего обновления", auto_now=True)
    publish_date = models.DateTimeField(verbose_name="Дата публикации", blank=True, null=True)
    published = models.BooleanField(verbose_name="Опубликован?", default=True)
    operating_systems = models.ManyToManyField(OperatingSystem, verbose_name="Операционные системы", related_name="products", blank=True)
    company = models.ForeignKey(Company, verbose_name="Создатель ПО", on_delete=models.PROTECT, blank=True, null=True)
    tags = models.ManyToManyField(Tag, verbose_name="Теги", related_name="products", blank=True, null=True)

    def __str__(self):
        """ Строковое представление модели (отображается в консоли) """
        return f'{self.title}: {self.price}Р'


class ProductKey(models.Model):
    product = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.PROTECT, related_name="keys")
    product_key = models.UUIDField(verbose_name="Ключ активации продукта", unique=True, default=uuid.uuid4, editable=False)
    is_deleted = models.BooleanField(verbose_name="Использован?", default=False)

    class Meta:
        ordering = ["-product"]
        verbose_name = 'Ключ активации продукта'
        verbose_name_plural = 'Ключи активации продуктов'

    def __str__(self):
        """ Строковое представление модели (отображается в консоли) """
        return f'{self.product}: {self.product_key}'


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Создает и сохраняет пользователя с введенным им email и паролем.
        """
        if not email:
            raise ValueError('email должен быть указан')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email'), unique=True)
    first_name = models.CharField(_('Имя'), max_length=30, blank=True)
    last_name = models.CharField(_('Фамилия'), max_length=30, blank=True)
    bankcard_number = models.CharField(_('Номер банковской карты'), max_length=30, blank=True, null=True)
    date_joined = models.DateTimeField(_('Дата регистрации'), auto_now_add=True)
    is_active = models.BooleanField(_('Активный?'), default=True)
    avatar = models.ImageField(_('Фото'), upload_to='avatars/', null=True, blank=True)
    is_staff = models.BooleanField(_('Сотрудник?'), default=False)

    objects = UserManager()

    # Временная метка создания объекта.
    created_at = models.DateTimeField(_('Время создания'), auto_now_add=True, blank=True, null=True)
    # Временная метка показывающая время последнего обновления объекта.
    updated_at = models.DateTimeField(_('Время обновления'), auto_now=True, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        """ Строковое представление модели (отображается в консоли) """
        return self.email

    def get_full_name(self):
        '''
        Возвращает first_name и last_name с пробелом между ними.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Возвращает сокращенное имя пользователя.
        '''
        return self.first_name

    @staticmethod
    def email_user(subject, message, to_email, from_email=None, **kwargs):
        '''
        Отправляет электронное письмо этому пользователю.
        '''
        send_mail(subject, message, from_email, [to_email], **kwargs)
