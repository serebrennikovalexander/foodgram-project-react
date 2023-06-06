import django_filters
from django_filters import rest_framework
from rest_framework.filters import SearchFilter

from recipes.models import MainTag, Recipe


class IngredientSearchFilter(SearchFilter):
    """
    Фильтр для ингредиентов.
    """
    search_param = 'name'


class RecipeFilterSet(rest_framework.FilterSet):
    """
    Фильтр для рецептов.
    """
    author = rest_framework.NumberFilter(field_name='author__id')
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=MainTag.objects.all()
    )
    is_favorited = django_filters.NumberFilter(
        method='is_favorited_filter'
    )
    is_in_shopping_cart = django_filters.NumberFilter(
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
        if value == 1:
            return queryset.filter(favorites__user=self.request.user)
        # if value and self.request.user.is_authenticated:
            # return queryset.filter(favorites__user=self.request.user)
        # return queryset

    def is_in_shopping_cart_filter(self, queryset, name, value):
        if value == 1:
            return queryset.filter(shopping_cart__user=self.request.user)
        # if value and self.request.user.is_authenticated:
            # return queryset.filter(shopping_cart__user=self.request.user)
        # return queryset
