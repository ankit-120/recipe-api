from django.test import TestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

class UserAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass"
        )
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}'
        )

        self.registration_url = reverse('users:create-user')
        self.login_url = reverse('users:login-user')
        self.logout_url = reverse('users:logout-user')
        self.user_info_url = reverse('users:user-info')
        self.user_profile_url = reverse('users:user-profile')
        self.user_avatar_url = reverse('users:user-avatar')
        self.user_bookmark_url = reverse('users:user-bookmark', kwargs={'pk': self.user.id})
        self.password_change_url = reverse('users:change-password')

    def test_user_registration(self):
        response = self.client.post(self.registration_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])

    def test_user_login(self):
        response = self.client.post(self.login_url, {
            'email': 'testuser@example.com',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])

    def test_user_profile(self):
        response = self.client.get(self.user_info_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_logout(self):
        response = self.client.post(self.logout_url, {
            'refresh': str(self.token)
        })
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_user_bookmarks(self):
        # Test adding a bookmark
        response = self.client.post(self.user_bookmark_url, {
            'id': 1 # Replace with a valid recipe ID
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test removing a bookmark
        response = self.client.delete(self.user_bookmark_url, {
            'id': 1  # Replace with a valid recipe ID
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_change(self):
        # Ensure the client is authenticated
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        
        # Test changing the password with correct old password
        response = self.client.patch(self.password_change_url, {
            'old_password': 'testpass',  # Correct old password
            'new_password': 'newpass123'  # Ensure this meets any password requirements
        })
        
        # Check for a successful response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify that the password has been updated
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass123'))
        
        # Test with incorrect old password
        response = self.client.patch(self.password_change_url, {
            'old_password': 'wrongpass',  # Incorrect old password
            'new_password': 'newpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test with invalid new password (assuming it must be at least 8 characters long)
        response = self.client.patch(self.password_change_url, {
            'old_password': 'testpass',
            'new_password': 'short'  # Example of an invalid password
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Additional check: Verify that the password hasn't been changed to an invalid one
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass123'))
