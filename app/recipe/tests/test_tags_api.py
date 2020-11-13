from django.contrib.auth import  get_user_model
from django.urls import  reverse
from django.test import TestCase

from rest_framework import  status
from rest_framework.test import  APIClient

from core.models import  Tag
from recipe.serializers import  TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTest(TestCase):
    """Test the publicly available tags"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateApiTest(TestCase):
    """Test the authorized user tags"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'shir@company.com',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        Tag.objects.create(user=self.user, name="Qaboli")
        Tag.objects.create(user=self.user, name="Mantoo")

        # res means response
        res = self.client.get(TAGS_URL)

        # order by name in alphabetical order in reverse order
        tags = Tag.objects.all().order_by('-name')
        # if it has more than one object so 'many=True' should pass
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for the authenticated user"""
        next_user = get_user_model().objects.create_user(
            'nextuser@gmail.com',
            'testpass'
        )
        Tag.objects.create(user=next_user, name='Chinaki')
        tag = Tag.objects.create(user=self.user, name="Palaw Mahi")

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        # we gonna get the name and then compare to the tag.name
        self.assertEqual(res.data[0]['name'], tag.name)
        
    def test_create_tag_successful(self):
        """Test creating a new tag"""
        payload = {'name': 'Test tag'}
        self.client.post(TAGS_URL, payload)

        # this exist return True or false
        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creating a new tag with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

