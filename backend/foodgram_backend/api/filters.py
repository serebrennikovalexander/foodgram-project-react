from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from recipes.models import MainTag, Recipe


class IngredientSearchFilter(SearchFilter):
    """
    Фильтр для ингредиентов.
    """
    search_param = 'name'


class RecipeFilterSet(FilterSet):
    """
    Фильтр для рецептов.
    """
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=MainTag.objects.all()
    )
    is_favorited = filters.BooleanFilter(
        method='is_favorited_filter'
    )
    is_in_shopping_cart = filters.BooleanFilter(
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
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def is_in_shopping_cart_filter(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset
