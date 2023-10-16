"""
Serializer for Recipe API's
"""

from rest_framework import serializers

from core.models import Recipe


class AllRecipeSerializer(serializers.ModelSerializer):
    """Serializer for getting all the recipies. No authentication needed"""
    class Meta:
        model = Recipe
        fields = '__all__'



class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes"""
    
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']
        
        
        
class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view"""
    
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']

