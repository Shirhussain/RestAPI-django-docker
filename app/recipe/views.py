from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import  viewsets, mixins, status
from rest_framework.authentication import  TokenAuthentication
from rest_framework.permissions import  IsAuthenticated

from core.models import  Tag, Ingredient, Recipe
from . serializers import  (
                        TagSerializer, 
                        IngredientSerializer, 
                        RecipeSerializer, 
                        RecipeDetailSerializer,
                        RecipeImageSerializer
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
        elif self.action == "upload_image":
            return RecipeImageSerializer
        
        return self.serializer_class
        
    def perform_create(self, serializer):
        """Create a new Recipe"""
        serializer.save(user=self.request.user)

    # define custom action 
    # detail=True means that it's actually for the detail and it's for specific  recipe
    # you are gonna only be to upload images that already exists and you will use the detail url
    # which has the id of the recipe in the url and know that which one to upload to 
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to recipe"""
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe, 
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        
        # if it's not valid an don't return we can do the standard way which is like follows
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
