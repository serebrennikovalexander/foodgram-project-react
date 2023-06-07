from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import exceptions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.filters import IngredientSearchFilter  # RecipeFilterSet
from api.pagination import CustomPageNumberPagination
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (CreateRecipeSerializer, FollowSerializer,
                             MainIngredientSerializer, MainTagSerializer,
                             ReadRecipeSerializer, ShortResipeSerializer)
from recipes.models import (Favorite, IngridientInRecipe, MainIngredient,
                            MainTag, Recipe, ShoppingCart)
from users.models import Follow

User = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для работы с рецептами.
    """
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    # pagination_class = CustomPageNumberPagination
    pagination_class = None
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('tags',)
    # filterset_class = RecipeFilterSet

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'DELETE'):
            return CreateRecipeSerializer
        return ReadRecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['POST', 'DELETE'])
    def favorite(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)

        if self.request.method == 'POST':
            if Favorite.objects.filter(
                user=user,
                recipe=recipe
            ).exists():
                raise exceptions.ValidationError(
                    'Рецепт уже в списке избранного.'
                )
            Favorite.objects.create(user=user, recipe=recipe)
            serializer = ShortResipeSerializer(
                recipe,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if not Favorite.objects.filter(
                user=user,
                recipe=recipe
        ).exists():
            raise exceptions.ValidationError(
                'Рецепта нет в списке избранного.'
            )
        favorite = get_object_or_404(Favorite, user=user, recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST', 'DELETE'])
    def shopping_cart(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)

        if self.request.method == 'POST':
            if ShoppingCart.objects.filter(
                user=user,
                recipe=recipe
            ).exists():
                raise exceptions.ValidationError(
                    'Рецепт уже в списке покупок.'
                )
            ShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = ShortResipeSerializer(
                recipe,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if not ShoppingCart.objects.filter(
                user=user,
                recipe=recipe
        ).exists():
            raise exceptions.ValidationError(
                'Рецепта нет в списке покупок.'
            )
        shopping_cart = get_object_or_404(
            ShoppingCart,
            user=user,
            recipe=recipe
        )
        shopping_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated, ))
    def download_shopping_cart(self, request):
        user = request.user
        filename = 'foodgram_shopping_list.txt'
        shopping_list = ['Список покупок:']
        ingredients = IngridientInRecipe.objects.filter(
            recipe__shopping_cart__user=user
        )
        calculation_ingredient = ingredients.values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))

        for ingredient in calculation_ingredient:
            shopping_list.append(
                '\n'
                f"{ingredient['ingredient__name']}: "
                f"({ingredient['amount']}) - "
                f"{ingredient['ingredient__measurement_unit']}"
            )

        response = HttpResponse(
            shopping_list,
            content_type='text/plain',
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


class MainTagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет для работы с тегами.
    """
    queryset = MainTag.objects.all()
    serializer_class = MainTagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class MainIngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет для работы с ингредиентами.
    """
    queryset = MainIngredient.objects.all()
    serializer_class = MainIngredientSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class CustomUserViewSet(UserViewSet):
    """
    Вьюсет для работы с пользователями.
    """
    # queryset = User.objects.all()
    pagination_class = CustomPageNumberPagination

    @action(
        detail=False,
        methods=['GET'],
        serializer_class=FollowSerializer,
    )
    def subscriptions(self, request):
        user = get_object_or_404(User, id=request.user.id)
        queryset = self.filter_queryset(
            User.objects.filter(following__user=user)
        )
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        serializer_class=FollowSerializer
    )
    def subscribe(self, request, id=None):
        user = self.request.user
        author = get_object_or_404(User, pk=id)

        if self.request.method == 'POST':
            if user == author:
                raise exceptions.ValidationError(
                    'Подписка на самого себя запрещена.'
                )
            if Follow.objects.filter(
                user=user,
                author=author
            ).exists():
                raise exceptions.ValidationError('Подписка уже оформлена.')
            Follow.objects.create(user=user, author=author)
            serializer = self.get_serializer(author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if not Follow.objects.filter(
            user=user,
            author=author
        ).exists():
            raise exceptions.ValidationError(
                'Подписки не было.'
            )
        subscription = get_object_or_404(
            Follow,
            user=user,
            author=author
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
