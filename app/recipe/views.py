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
        # next we are gonna add a feature to our API so we can filter tags and ingredients 
        # that are assigned to recipe only, we might wanna use this filter if we creating 
        # a front-end application that has drop-down list that we can user to filter 
        # recipe by tags and ingredients, in that dropdown you might only want to see the 
        # list of tags and ingredients that are actually assigned to recipe already 
        # and you might want to exclude any tags and ingredients that are not assigned to 
        # any recipe 
        assigned_only = bool(
            # the reason that i have passed as integer first 'int' because the assigned value 
            # gonna be '0 or 1' and with they query_prams there is no consept of type 
            # so wee need to first convert to an ingeger and then convert to a boolean
            # otherwise if you do boolean with string with '0' in it then that convert to true
            # which means that assigned only will be True if we pass assigned_only =0  

            # if assigned_only isn't passed at all it means None, so you have to pass a default value = 0
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()
    
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

    # in python we don't have convention for (public, private) function 
    # all we have is public but if you intended to have private so do it just by underscore (_)
    def _params_to_ints(self, qs):
        """Convert a list of strings to a list of integers"""
        # our_string ='1,2,3'
        # our_string_list = ['1','2','3','4']
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Return the recipe for authenticated user"""
        # for filtering 'tags', and 'ingredients' in recipe 
        # i gonna start by retrieving the comma saprated string of id's for our tags and ingredint
        # query_params() is a dictionary pram which contain all of dictionary that are provided 
        # in the request. in 'get' if we provided 'tags' in will assigned to tags otherwise it return None
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            Ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=Ingredient_ids)
        return queryset.filter(user=self.request.user)

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