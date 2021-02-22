from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        '''Test creating a new user with an email is successful'''
        email = 'greenkelechi@gmail.com'
        password = "bracelet"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_normalized(self):
        """Test the email for a new user is normalised"""
        email = 'test@GMAIL.COM'
        user = get_user_model().objects.create_user(email, 'bracelet')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating usert with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'bracelet')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test"gmail.com',
            'bracelet'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
