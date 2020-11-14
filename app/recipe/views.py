from rest_framework import  viewsets, mixins
from rest_framework.authentication import  TokenAuthentication
from rest_framework.permissions import  IsAuthenticated

from core.models import  Tag, Ingredient
from . serializers import  TagSerializer, IngredientSerializer


class TagViewSet(viewsets.GenericViewSet, 
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """Manage tag in database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_queryset(self):
        """Return the object of current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new tag"""
        serializer.save(user=self.request.user)


class IngredientViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage ingredient in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_queryset(self):
        """Return object for the current authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
        