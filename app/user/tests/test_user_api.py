from django.test import TestCase
from django.contrib.auth import get_user_model #This helps us use our models
from django.urls import reverse #This imports api urls

from rest_framework.test import APIClient#
from rest_framework import status#this module contains some status code that a in basic readable form


CREATE_USER_URL = reverse('user:create')#This a user create url
TOKEN_URL = reverse('user:token')

def create_user(**param):
    return get_user_model().objects.create_user(**param)

class PublicUserApiTests(TestCase):
    """Test the user API (public)"""

    def setup(self):
        self.client = APIClient()#This is a user

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload ={
            'email': 'greenkelechi@gmail.com',
            'password': 'testpass',
            'name': 'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)#this is a user entering the above name,email,set_password
        #which is the payload. and it being posted

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)#This is getting the payload in form of a dictionary
        self.assertTrue(user.check_password(payload['password']))#This asserts that the password is true
        self.assertNotIn('password', res.data)#Checking to ensure that the password is not part of the dictionary for secutiy reasons

    def test_user_exists(self):
        """Test creating user that already exists fails"""
        payload = {'email': 'greenkelechi@gmail.com', 'password': 'testpass'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)#This should return a 400 bad request

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {'email': 'greenkelechi@gmail.com', 'password': 'pw'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)#this ensures that if the password is to short, it return a HTTP 400 bad request
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()#This checks if any user with a short password exists
        self.assertFalse(user_exists)


    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {'email': 'greenkeelchi@gmail.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)


        self.assertIn('token', res.data)#this tests that there is a token in res.data
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """test that token is not created if invalid credentials are given"""
        create_user(email='greenkelechi@gmail.com', password='testpass')#This is the correc password
        payload = {'email': 'greenkelechi@gmail.com', 'password': 'wrong'}#this is the wrong password
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesnt exist"""
        payload = {'email': 'greenkelechi@gmail.com', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_fields(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})#if email or password is empty the test should fail

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
