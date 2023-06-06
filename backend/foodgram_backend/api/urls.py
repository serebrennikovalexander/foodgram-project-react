from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CustomUserViewSet, MainIngredientViewSet, MainTagViewSet,
                    RecipeViewSet)

app_name = 'api'

router = DefaultRouter()

router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'tags', MainTagViewSet, basename='tags')
router.register(r'ingredients', MainIngredientViewSet, basename='ingredients')
router.register(r'users', CustomUserViewSet, basename='users')

urlpatterns = [
    # path('', include('djoser.urls')),
    path('', include(router.urls)),
    path(r'auth/', include('djoser.urls.authtoken')),
]
