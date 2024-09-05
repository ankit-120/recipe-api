from django.test import TestCase
from users.models import CustomUser, Profile
from users.serializers import CustomUserSerializer, UserRegisterationSerializer, ProfileSerializer

class CustomUserSerializerTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", email="testuser@example.com", password="testpass")
        Profile.objects.filter(user=self.user).delete()  # Ensure no profile exists
        self.profile = Profile.objects.create(user=self.user, bio='Test Bio')
        self.serializer = CustomUserSerializer(instance=self.user)

    def test_serialization(self):
        data = self.serializer.data
        self.assertEqual(data['email'], 'testuser@example.com')
        self.assertEqual(data['username'], 'testuser')

class UserRegistrationSerializerTests(TestCase):
    def test_create_user(self):
        data = {
            'email': 'newuser@example.com',
            'password': 'password123',
            'username': 'newuser'
        }
        serializer = UserRegisterationSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            self.assertEqual(user.email, 'newuser@example.com')
            self.assertTrue(user.check_password('password123'))
        else:
            self.fail('Serializer validation failed')

class ProfileSerializerTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='password123',
            username='testuser'
        )
        Profile.objects.filter(user=self.user).delete()  # Ensure no profile exists
        self.profile = Profile.objects.create(user=self.user, bio='Test Bio')
        self.serializer = ProfileSerializer(instance=self.profile)

    def test_serialization(self):
        data = self.serializer.data
        self.assertEqual(data['bio'], 'Test Bio')
