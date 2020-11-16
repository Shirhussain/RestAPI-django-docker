from rest_framework import serializers

from core.models import  Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""


    class Meta:
        model = Tag
        fields = ('id','name')
        read_only_fields = ('id',)
        

class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for INgredient objects"""

    class Meta:
        model = Ingredient
        fields = ('id','name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe object"""
    # because 'ingredients and tags' are not actually the par of the serializer
    # so i need to do the following style.
    # what it's dose?  it's list the objects or ingredients with 'id'
    # because we don't wanna to list the full list of this values of this objects
    # if we wanna access to other fields of this object we can do that with 'detail API'
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset = Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset = Tag.objects.all()
    )

    class Meta:
        model = Recipe 
        fields = (
            'id', 'title', 'ingredients','tags', 'time_minutes',
            'price', 'link'
        )
        # we put read_only here to make sure that user can't change the id
        read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    """Serialize a recipe detail"""
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    