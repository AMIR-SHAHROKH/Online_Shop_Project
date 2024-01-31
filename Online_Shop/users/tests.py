from django.contrib.auth import authenticate
from django.test import TestCase
from django.contrib.auth import get_user_model

class UserModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a sample user
        cls.User = get_user_model()
        cls.user = cls.User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_user_creation(self):
        user = self.User.objects.get(username='testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpassword'))

    def test_user_str_representation(self):
        user = self.User.objects.get(username='testuser')
        self.assertEqual(str(user), 'testuser')

    def test_user_authentication(self):
        authenticated_user = authenticate(username='testuser', password='testpassword')
        self.assertEqual(self.user, authenticated_user)

    def test_user_invalid_authentication(self):
        authenticated_user = authenticate(username='testuser', password='invalidpassword')
        self.assertIsNone(authenticated_user)
