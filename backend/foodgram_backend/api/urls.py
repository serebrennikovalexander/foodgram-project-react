from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CustomUserViewSet, MainIngredientViewSet, MainTagViewSet,
                    RecipeViewSet)

app_name = 'api'

router = DefaultRouter()

router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', MainTagViewSet, basename='tags')
router.register('ingredients', MainIngredientViewSet, basename='ingredients')
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
