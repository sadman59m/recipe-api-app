"""
Tests for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model



class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new user"""
        sample_emails = [
            ['Test1@Example.com', 'Test1@example.com'],
            ['TEST1@EXAMPLE.com', 'TEST1@example.com'],
            ['test@example.COM', 'test@example.com']
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'pass123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raise_error(self):
        """Test creating a user without email raises valueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_super_user(self):
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)