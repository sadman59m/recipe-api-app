"""
Views for Recipe APIs
"""

from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
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
        
        return self.serializer_class
            
    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)
