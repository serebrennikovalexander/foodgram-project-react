from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.fields import Base64ImageField
from recipes.models import (Favorite, IngridientInRecipe, MainIngredient,
                            MainTag, Recipe, ShoppingCart)
from users.models import Follow

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользователя.
    """
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return (
            not user.is_anonymous
            and Follow.objects.filter(user=user, author=obj).exists()
        )


class MainTagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для работы с тегами.
    """
    class Meta:
        model = MainTag
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class MainIngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для работы с ингредиентами.
    """
    class Meta:
        model = MainIngredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )


class IngridientInRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для ингридиентов в рецепте.
    """
    id = serializers.PrimaryKeyRelatedField(
        queryset=MainIngredient.objects.all()
    )
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngridientInRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class ReadRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения рецепта.
    """
    author = CustomUserSerializer(read_only=True, many=False)
    ingredients = IngridientInRecipeSerializer(
        many=True,
        source='ingredientinrecipe'
    )
    tags = MainTagSerializer(read_only=False, many=True)
    image = Base64ImageField(max_length=None)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_ingredients(self, obj):
        ingredients = IngridientInRecipe.objects.filter(recipe=obj)
        return IngridientInRecipeSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        return (
            not user.is_anonymous
            and Favorite.objects.filter(
                user=user.id,
                recipe=obj.id
            ).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        return (
            not user.is_anonymous
            and Recipe.objects.filter(
                shopping_cart__user=user,
                id=obj.id
            ).exists()
        )


class CreateRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания рецепта.
    """
    ingredients = IngridientInRecipeSerializer(
        many=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=MainTag.objects.all()
    )
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def validate_tags(self, tags):
        for tag in tags:
            if not MainTag.objects.filter(id=tag.id).exists():
                raise serializers.ValidationError(
                    'Указанного тега не существует')
        return tags

    def validate_cooking_time(self, cooking_time):
        if cooking_time < 1:
            raise serializers.ValidationError(
                'Время готовки должно быть не меньше одной минуты')
        return cooking_time

    @staticmethod
    def create_ingredients(recipe, ingredients):
        ingredient_list = []
        for ingredient_data in ingredients:
            ingredient_list.append(
                IngridientInRecipe(
                    ingredient=ingredient_data.pop('id'),
                    amount=ingredient_data.pop('amount'),
                    recipe=recipe,
                )
            )
        IngridientInRecipe.objects.bulk_create(ingredient_list)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(
            recipe,
            ingredients
        )
        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        IngridientInRecipe.objects.filter(recipe=instance).delete()
        instance.tags.set(validated_data.pop('tags'))
        ingredients = validated_data.pop('ingredients')
        self.create_ingredients(instance, ingredients)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return ReadRecipeSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data


class ShortResipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор рецептов для короткого отображения.
    """

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
        read_only_fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class FavoriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для избранных рецептов.
    """

    class Meta:
        model = Favorite
        fields = (
            'user',
            'recipe'
        )


class ShoppingCartSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка покупок.
    """

    class Meta:
        model = ShoppingCart
        fields = (
            'user',
            'recipe'
        )


class FollowSerializer(CustomUserSerializer):
    """
    Сериализатор для подписок на автора.
    """
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj)

        if limit:
            queryset = Recipe.objects.filter(
                author=obj
            )[:int(limit)]
        queryset = Recipe.objects.filter(author=obj)

        return ShortResipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
