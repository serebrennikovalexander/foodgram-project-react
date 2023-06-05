import django_filters
from rest_framework import filters

from recipes.models import MainTag, Recipe


class IngredientSearchFilter(filters.SearchFilter):
    """
    Фильтр для ингредиентов.
    """
    search_param = 'name'


class RecipeFilterSet(django_filters.FilterSet):
    """
    Фильтр для рецептов.
    """
    tags = django_filters.ModelChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=MainTag.objects.all()
    )
    is_favorited = django_filters.BooleanFilter(
        method='is_favorited_filter'
    )
    is_in_shopping_cart = django_filters.BooleanFilter(
        method='is_in_shopping_cart_filter'
    )

    class Meta:
        model = Recipe
        fields = (
            'author',
            'tags',
            'is_favorited',
            'is_in_shopping_cart'
        )

    def is_favorited_filter(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def is_in_shopping_cart_filter(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset
