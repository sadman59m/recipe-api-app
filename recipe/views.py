"""
Views for Recipe APIs
"""

import os
from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Recipe,
    Tag,
    Ingredient,
)
from recipe import serializers



class AllRecipeView(ListAPIView):
    serializer_class = serializers.AllRecipeSerializer
    queryset = Recipe.objects.all()



class RecipeViewSet(viewsets.ModelViewSet):
    """View for managing recipe APIs"""
    """This is a viewset which will have multiple endpoints such as list, details etc"""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retrive Recipes for authenticated User"""
        return self.queryset.filter(user=self.request.user).order_by('-id')
    
    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == 'list':
            return serializers.RecipeSerializer
        
        #custom serializer action
        if self.action == 'upload_image':
            return serializers.RecipeImageSerializer
        
        return self.serializer_class
            
    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)
        
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to Recipe"""
        recipe = self.get_object()
        
        existing_image_path = None
        if recipe.image:
            existing_image_path = recipe.image.path

        serializer = self.get_serializer(recipe, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            if existing_image_path and os.path.exists(existing_image_path):
                os.remove(existing_image_path)
                
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        

        
class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet,
                            ):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset to authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')



class TagViewSet(BaseRecipeAttrViewSet):
    """Manage Tags in Database"""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    
    
    
class IngredientViewSet(BaseRecipeAttrViewSet):
    """Viewset For Ingredient"""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()