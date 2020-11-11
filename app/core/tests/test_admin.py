from django.test import TestCase, Client
from django.contrib.auth import  get_user_model
from django.urls import  reverse


class AdminSiteTest(TestCase):

    def setUp(self):
        self.client = Client() 
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'shihussain@company.com',
            password = 'password134'
        )
        # force_login --> it is use the client helper function that allow you to login user in 
        # with django authentication and it's make our test a lot easier to write.
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email = "shirtest@comapny.com",
            password = "Password134",
            name = "Test you full name"
        )

    def test_users_listed(self):
        """ Test users are listed in user page"""
        # This url in defined in django documentations 
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code,200)
        