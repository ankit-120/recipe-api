# user/tests/test_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import CustomUser as User

class UserModelTests(TestCase):
    def setUp(self):
        # self.User = get_user_model()
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpass")
        
        

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertTrue(self.user.check_password('testpass'))

    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser@example.com')
