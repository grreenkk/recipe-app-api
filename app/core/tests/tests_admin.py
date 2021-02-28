from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client() #This is a test client from django framework
        self.admin_user = get_user_model().objects.create_superuser(
            email='greenkelechi"gmail.com',
            password = 'bracelet'
        )
        self.client.force_login(self.admin_user) #This is the admin logged into the client
        self.user = get_user_model().objects.create_user(#This is used to test users listing
            email = 'greenkelechi@gmail.com',
            password = 'bracelet',
            name = 'Test user full name'

        )

    def test_users_listed(self):
        """test that users are listed on user page"""
        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)


    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])# /admin/score.user/id(id of the user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_create_user_page(self):# This adds new users
        """test that the create user page works"""
        url = reverse('admin:core_user_add')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
