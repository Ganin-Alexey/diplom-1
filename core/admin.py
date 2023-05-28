from django.contrib import admin
from django import forms
# Register your models here.
from core.models import Tag, Product, OperatingSystem, Company, User, ProductKey
from languages_plus.models import Language, CultureCode
from countries_plus.models import Country
from django.contrib.admin.sites import site
from django.contrib.admin.widgets import ForeignKeyRawIdWidget

admin.site.unregister(Language)
admin.site.unregister(CultureCode)
admin.site.unregister(Country)


class ProductKeyAdminForm(forms.ModelForm):
    """Изменяем виджет для ForeignKey"""

    class Meta:
        model = ProductKey
        widgets = {
            'keys': ForeignKeyRawIdWidget(ProductKey._meta.get_field('product').remote_field, site),
        }
        fields = '__all__'


@admin.register(ProductKey)
class ProductKeyAdmin(admin.ModelAdmin):
    model = ProductKey
    form = ProductKeyAdminForm


class ProductKeyInLine(admin.StackedInline):
    model = ProductKey


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    model = Company


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag


@admin.register(OperatingSystem)
class TagAdmin(admin.ModelAdmin):
    model = OperatingSystem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    inlines = [ProductKeyInLine, ]
    list_display = (
        "title",
        "slug",
        "price",
        "publish_date",
        "published",
    )
    list_filter = (
        "published",
        "publish_date",
    )
    list_editable = (
        "slug",
        "price",
        "publish_date",
        "published",
    )
    list_display_links = ("title",)
    search_fields = (
        "title",
        "price",
        "slug",
        "body",
    )
    prepopulated_fields = {
        "slug": (
            "title",
            "price",
        )
    }

    date_hierarchy = "publish_date"
    save_on_top = True
