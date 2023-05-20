from django.contrib import admin

# Register your models here.
from core.models import Tag, Product, OperatingSystem, Company


# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     model = Profile


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    model = Company


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag


@admin.register(OperatingSystem)
class TagAdmin(admin.ModelAdmin):
    model = OperatingSystem


@admin.register(Product)
class PostAdmin(admin.ModelAdmin):
    model = Product

    list_display = (
        "id",
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
        "title",
        "slug",
        "price",
        "publish_date",
        "published",
    )
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
