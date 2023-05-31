from backend import settings
from django.db.models import Count
from graphene_django import DjangoObjectType
from core import models
from django.db.models import F, Q, QuerySet
import graphene
from graphql_jwt.decorators import login_required
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity


class UserType(DjangoObjectType):
    class Meta:
        model = models.User


class CompanyType(DjangoObjectType):
    class Meta:
        model = models.Company


class ProductType(DjangoObjectType):
    class Meta:
        model = models.Product


class TagType(DjangoObjectType):
    name_tag = graphene.String()
    count_products = graphene.Int()

    class Meta:
        model = models.Tag

    def resolve_name_tag(self, info):
        # Returns last message only if the object was annotated
        return getattr(self, 'name_tag', None)

    def resolve_count_products(self, info):
        # Returns last message only if the object was annotated
        return getattr(self, 'count_products', None)


class OperatingSystemType(DjangoObjectType):
    name_system = graphene.String()
    count_products = graphene.Int()

    class Meta:
        model = models.OperatingSystem

    def resolve_name_system(self, info):
        # Returns last message only if the object was annotated
        return getattr(self, 'name_system', None)

    def resolve_count_products(self, info):
        # Returns last message only if the object was annotated
        return getattr(self, 'count_products', None)


class LanguageType(DjangoObjectType):
    class Meta:
        model = models.Language


class Query(graphene.ObjectType):
    all_products = graphene.List(ProductType, tag=graphene.ID())
    company_by_id = graphene.Field(CompanyType, id=graphene.ID())
    product_by_slug = graphene.Field(ProductType, slug=graphene.String())
    products_by_author = graphene.List(ProductType, id=graphene.ID())
    products_by_tag = graphene.List(ProductType, tag=graphene.String())
    tags_with_count_of_products = graphene.List(TagType)
    operating_systems_with_count_of_products = graphene.List(OperatingSystemType)
    viewer = graphene.Field(UserType, token=graphene.String(required=True))
    products_search = graphene.List(ProductType, query=graphene.String())
    order_payment = graphene.String(email=graphene.String(), ids=graphene.List(graphene.ID))

    @login_required
    def resolve_viewer(self, info, **kwargs):
        return info.context.user

        subject = 'Globus-IT: Ваша покупка совершена успешно!'
        message = 'Ваши ключи: \n'
        for product in products_in_order:
            key = product.keys.first()
            message += f'{product.title} - {key.product_key}\n'
            key.is_deleted = True
            key.save()
        models.User.email_user(subject=subject, to_email=email, message=message)
        return 'Complete'

    def resolve_tags_with_count_of_products(self, info):
        return (
            models.Tag.objects.annotate(name_tag=F('name'), count_products=Count('products')).order_by('name_tag')
        )

    def resolve_products_search(self, info, query=''):
        products = models.Product.objects.prefetch_related("tags", "operating_systems", "languages").select_related("company")

        query_filter = Q()
        for word in query.split(' '):
            query_filter |= Q(title__icontains=word)
            query_filter |= Q(description__icontains=word)
            query_filter |= Q(price__icontains=word)
        return products.filter(query_filter)

    def resolve_operating_systems_with_count_of_products(self, info):
        return (
            models.OperatingSystem.objects.annotate(name_system=F('name'), count_products=Count('products'))
        )

    def resolve_all_products(self, info, tag=None):
        products = models.Product.objects.prefetch_related("tags", "operating_systems", "languages").select_related("company")
        if tag:
           return (products.filter(tags=tag))
        return (products.all())

    def resolve_company_by_id(self, info, id):
        return models.Profile.objects.get(
            id=id
        )

    def resolve_product_by_slug(self, info, slug):
        return (
            models.Product.objects.prefetch_related("tags")
                .select_related("author")
                .get(slug=slug)
        )

    def resolve_products_by_company(self, info, id):
        return (
            models.Product.objects.prefetch_related("tags")
                .select_related("company")
                .filter(company__id=id)
        )

    def resolve_products_by_tag(self, info, tag):
        return (
            models.Product.objects.prefetch_related("tags")
                .select_related("author")
                .filter(tags__name__iexact=tag)
        )

import graphql_jwt


class UserMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        email = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        password = graphene.String(required=True)

    # The class attributes define the response of the mutation
    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, email, first_name, last_name, password):
        user = models.User.objects.create(email=email, first_name=first_name, last_name=last_name, password=password)
        user.save()
        # Notice we return an instance of this mutation
        return UserMutation(user=user)


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()
    delete_token_cookie = graphql_jwt.DeleteJSONWebTokenCookie.Field()
    # Long running refresh tokens
    delete_refresh_token_cookie = graphql_jwt.DeleteRefreshTokenCookie.Field()
    register_user = UserMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
