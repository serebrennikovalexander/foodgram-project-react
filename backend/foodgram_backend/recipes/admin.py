from django.contrib import admin

from .models import (Favorite, IngridientInRecipe, MainIngredient, MainTag,
                     Recipe, ShoppingCart)


@admin.register(MainIngredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(IngridientInRecipe)
class IngridientInRecipeAdmin(admin.ModelAdmin):
    fields = ('ingredient', 'recipe', 'amount')
    search_fields = ('ingredient', 'recipe')


class IngridientInRecipeInline(admin.TabularInline):
    model = IngridientInRecipe
    min_num = 1
    extra = 0


@admin.register(MainTag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'text', 'pub_date')
    search_fields = ('name', 'author')
    filter_horizontal = ('tags', )
    list_filter = ('tags', 'author', 'name')
    inlines = (IngridientInRecipeInline, )

    def count_favorites(self, obj):
        return obj.favorites.count()


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
