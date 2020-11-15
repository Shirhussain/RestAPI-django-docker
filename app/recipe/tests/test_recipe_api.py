from django.contrib.auth import  get_user_model
from django.urls import  reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import  APIClient

from core.models import  Recipe 

from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')


def sample_recipe(user, **params):
    """Create and return a sample recipe"""
    # i gonna interduce you to a new consept of creating helper functions when we need 
    # repeated object in our test.
    # we know that we are gonna create a lot of recipes for this test.
    # you know that recipe has three or four require prammiters, 
    # what i gonna do is that i have to setup a funcitions that allow us to create a recipe 
    # that allow as with a set of default values. this make a lot easier to test.
    defaults = {
        # her we have use but in our function we have we don't need to repeat.
        'title': 'Sample Recipe',
        'time_minutes': 30,
        'price': 50.00
    }
    # what this 'update' does ? it's accept dictionary object and it will take which ever 
    # keys are in the dictionary and it will update them or they don't exists it will create them. 
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTest(TestCase):
    """Test unauthorized recipe API access"""
    
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication required"""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """Test unauthenticated recipe API access"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'sampleUser@gmail.com',
            'testPasswordhere'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_users(self):
        """Test retrieving recipies for user"""
        user2 = get_user_model().objects.create_user(
            'next_user@gmail.com',
            'nextPassword'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
