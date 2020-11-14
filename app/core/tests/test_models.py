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
        
