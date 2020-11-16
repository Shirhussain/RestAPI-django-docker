from django.contrib.auth import  get_user_model
from django.urls import  reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import  APIClient

from core.models import  Recipe, Tag, Ingredient

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer


RECIPES_URL = reverse('recipe:recipe-list')

# for the URL it should look like this:
# api/recipe/recipes 
# for detail one the line bellow 
# api/recipe/recipes/<id>/
# because 'Id' here is dynamic so we need to use a function
def detail_url(recipe_id):
    """Return Recipe Detail url"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_tag(user, name="Main course"):
    """Create and return sample tag"""
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name="Cimanac"):
    """Create and return a sample ingredient """
    return Ingredient.objects.create(user=user, name=name)

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

    def test_view_recipe_detail(self):
        """Test viewing a recipe Detail"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))
        
        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_recipe(self):
        """Test creating recipe """
        payload = {
            'title': 'Qoroti Afghani',
            'time_minutes': 40,
            'price': 80.00
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        # next i gonna look trough each one of payload keys and then gonna check 
        # that is correct values assigned to our model.
        for key in payload.keys():
            # unfortunatly you can't just do recipe.key  because then it will try to retrieve the key named key
            # from our recipe which is above this for loop.
            # instead i use 'getattr'. is a function that allow you to retrieve an attribute from an object 
            # by passing in a variable. 'getatt(recipe, key)--> which is like recipe.title or recipe.time_minute
            self.assertEqual(payload[key], getattr(recipe, key))

        def test_create_recipe_with_tags(self):
            """Test create a recipe with tags"""
            tag1 = sample_tag(user=self.user, name='Dogh')
            tag2 = sample_tag(user=self.user, name='Oil')
            payload = {
                'title': 'Chinaki with dogh',
                'tags': [tag1.id, tag2.id],
                'time_minutes': 50,
                'price': 400.00
            }
            res = self.client.post(RECIPES_URL, payload)

            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
            recipe = Recipe.objects.get(id=res.data['id'])
            tags = recipe.tags.all()
            # next we should assert that the count of tags are 2 because 2 are assigned
            self.assertEqual(tags.count(), 2)
            self.assertIn(tag1, tags)
            self.assertIn(tag2, tags)

        def test_create_recipe_with_ingredients(self):
            """Test create recipe with ingredients"""
            ingredient1 = sample_ingredient(user=self.user, name='salt')
            ingredient2 = sample_ingredient(user=self.user, name='rice')
            payload = {
                'title': 'Qaboli uzbaki',
                'ingredients': [ingredient1.id, ingredient2.id],
                'time_minutes': 80,
                'price': 150.00
            }
            res = self.client.post(RECIPES_URL, payload)

            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
            recipe = Recipe.objects.get(id=res.data['id'])
            ingredients = recipe.ingredients.all()
            self.assertEqual(ingredients.count(), 2)
            self.assertIn(ingredient1, ingredients)
            self.assertIn(ingredient2, ingredients)
            
