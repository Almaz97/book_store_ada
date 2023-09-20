from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class SignupViewTestCase(APITestCase):

    @patch('user_auth.serializers.check_email.delay')
    @patch('user_auth.serializers.save_signup_info.delay')
    def test_signup_with_valid_data(self, check_email_mock, save_signup_info_mock):
        data = {
            'username': 'test_username',
            'email': 'alex123@gmail.com',
            'password': 'super_password2020',
            'password2': 'super_password2020'
        }
        url = reverse('signup')
        response = self.client.post(url, data=data)

        users = User.objects.all()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(users.count(), 1)
        self.assertEqual(users.first().username, data['username'])

        check_email_mock.assert_called_with(user_id=users.first().id)
        save_signup_info_mock.assert_called_with(user_id=users.first().id)

    def test_signup_with_invalid_data(self):
        data = {
            'username': 'test_username',
            'email': 'alex123@gmail.com',
            'password': 'super_password2020',
            'password2': 'not_matching_password'
        }

        url = reverse('signup')
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)


class LoginViewTestCase(APITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.username = 'test_username'
        self.email = 'test_username@gmail.com'
        user = User.objects.create(
            username=self.username,
            email=self.email
        )
        user.set_password('fortest2020')
        user.save()

    def test_login_valid_data(self):
        data = {
            'username': self.username,
            'password': 'fortest2020'
        }

        url = reverse('token_obtain_pair')
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_invalid_data(self):
        pass
