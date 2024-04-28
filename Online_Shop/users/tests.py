from django.contrib.auth import authenticate
from django.test import TestCase
from django.contrib.auth import get_user_model
# from django.urls import reverse
# from django.contrib.auth.models import User

# class LoginViewTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Set up test data such as users if needed
#         User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

#     def test_login_view_get(self):
#         # Test GET request to login view
#         response = self.client.get(reverse('login'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'login.html')  # Replace 'your_template.html' with your actual template

#     def test_login_view_post_valid(self):
#         # Test POST request to login view with valid data
#         data = {'username': 'testuser', 'password': 'testpassword'}
#         response = self.client.post(reverse('login'), data)
#         self.assertEqual(response.status_code, 302)  # 302 is the status code for a redirect after successful login
#         self.assertRedirects(response, reverse('profile/login/'))  # Replace 'success_url' with your actual success URL

#     def test_login_view_post_invalid(self):
#         # Test POST request to login view with invalid data
#         data = {'username': 'invaliduser', 'password': 'invalidpassword'}
#         response = self.client.post(reverse('login'), data)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'login.html')  # Replace 'your_template.html' with your actual template
#         self.assertFormError(response, 'form', None, 'Invalid username or password')  # Adjust the form error message as needed

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
