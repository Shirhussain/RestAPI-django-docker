from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import  get_user_model

from core import  models


def sample_user(email = 'shirTest@gmail.com', password='testpassword'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    
    def test_create_user_with_email_successfull(self):
        """Test creating a new user with an email successfull""" 
        email = "sh.dansihyar@gmail.com" 
        password = "Testkon123"
        user = get_user_model().objects.create_user(email = email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


    def test_new_user_email_normalized(self):
        """Test the email for the user is normalized"""
        email = 'sh.danishyar@GMAIL.com'
        user  = get_user_model().objects.create_user(email, "test123")

        self.assertEqual(user.email, email.lower())


    def test_new_user_invalid_email(self):
        """Test creating user with no email raise error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test1234')

    
    def test_new_superuser(self):
        """Test create a new superuser"""
        user = get_user_model().objects.create_superuser('danishayrCompany@shir.com', 'test123')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user = sample_user(),
            name = 'ShirTag'
        )
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test The ingredient string representations"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name="Cucumber"
        )

        self.assertEqual(str(ingredient), ingredient.name)
        
    def test_recipe_str(self):
        """Test the recipe string representations"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Qboli palaw or ozbaki palaw',
            time_minutes=30,
            price=150.00
        )

        self.assertEqual(str(recipe), recipe.title)

    # i gonna mock the uuid function from the default uuid library that comes with python
    # then i gonna change the value it return and gonna call our function and make sure that the 
    # string that is created for the path matches what we expected with sample uuid.
    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that images is saved in the correct location"""
        uuid = 'test-uuid'
        # the following line means that whenever we call funcation that is triggered form 
        # whiten our test it will change the value and overwrite the default behavior 
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myImage.jpg')
        
        expected_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, expected_path)


