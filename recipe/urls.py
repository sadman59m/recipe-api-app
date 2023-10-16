"""
URL mappings for recipe
"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from recipe import views




router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
    path('all/', views.AllRecipeView.as_view(), name='all-recipe'),
]
