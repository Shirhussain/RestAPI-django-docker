from rest_framework import  viewsets, mixins
from rest_framework.authentication import  TokenAuthentication
from rest_framework.permissions import  IsAuthenticated

from core.models import  Tag, Ingredient, Recipe
from . serializers import  (
                        TagSerializer, 
                        IngredientSerializer, 
                        RecipeSerializer, 
                        RecipeDetailSerializer
)


# to avoid code duplication between TagVieSet and IngredientViewSet 
# i gonna define a base class for this two.
class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """Base viewset for user owned recipe attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
    
    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tag in database"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipe in the database"""
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return the recipe for authenticated user"""
        return self.queryset.filter(user=self.request.user)

    # i gonna overwrite the serializer_class because according to Rest framework docs
    # this is that function to call and retrieve the serializer class for 
    # a particular request. by default there is set of action in model viewset which:
    # one of them is 'list, the other action is retrive' in which i gonna retrieve the 
    # detail serializer.

    # also make sure that you are typing the correct bellow spalling otherwise it won't work
    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == "retrieve":
            return RecipeDetailSerializer
        
        return self.serializer_class
        
