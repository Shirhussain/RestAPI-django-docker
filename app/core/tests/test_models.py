from django.test import TestCase
from django.contrib.auth import  get_user_model


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
        user  = get_user_model().objects.create_user(email,"test123")

        self.assertEqual(user.email, email.lower())


    def test_new_user_invalid_email(self):
        """Test creating user with no email raise error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test1234')

    
    def test_new_superuser(self):
        """Test create a new superuser"""
        user = get_user_model().objects.create_superuser('danishayrCompany@shir.com','test123')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

