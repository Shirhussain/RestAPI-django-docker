from django.contrib.auth import  get_user_model
from django.urls import  reverse
from django.test import TestCase

from rest_framework import  status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import  IngredientSerializer


INGREDIENT_URL = reverse('recipe:ingredient-list')


class PublicIngredientApiTest(TestCase):
    """Test the public ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the ingredient"""
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTest(TestCase):
    """Test the private ingredients API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'shir@compnay.com',
            'testpassword'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients_test(self):
        """Retrieving a list of ingredients"""
        Ingredient.objects.create(user=self.user, name='soup')
        Ingredient.objects.create(user=self.user, name='salt')

        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that ingredients for the authenticated user are required"""
        user2 = get_user_model().objects.create_user(
            'next@user.com',
            'user2pass'
        )
        Ingredient.objects.create(user=user2, name='Oil')
        ingredient = Ingredient.objects.create(user=self.user, name='onion')

        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

        
