"""
Tests for the models in the app.
"""
import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class UserModelTests(TestCase):
    """Test the User model."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = "test@example.com"
        password = "testpassword123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.role, 'reader')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email=email, password='sample123'
            )
            self.assertEqual(user.email, expected)
            self.assertEqual(user.role, 'reader')

    def test_new_user_without_email_raises_error(self):
        """Test creating user without an email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='', password='test123'
            )

    def test_create_editor_user(self):
        """Test creating an editor user"""
        email = 'editortest@example.com'
        user = get_user_model().objects.create_editor_user(
            email=email,
            password='test123'
        )
        self.assertEqual(user.email, email)
        self.assertEqual(user.role, 'editor')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_with_bad_role(self):
        """Test creating a user with an invalid role raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='test@example.com',
                password='test123',
                role='invalid_role'
            )

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.role, 'reader')

    def test_check_if_user_editor(self):
        """Test if user is editor"""
        user = get_user_model().objects.create_editor_user(
            email='test@example.com',
            password='test123'
        )
        self.assertTrue(user.is_editor())

    def test_check_if_user_reader(self):
        """Test if user is reader"""
        user = get_user_model().objects.create_user(
            email='test@example.com',
            password='test123'
        )
        self.assertTrue(user.is_reader())

    def test_create_book(self):
        """Test creating a book"""
        book = models.Book.objects.create(
            uuid=uuid.uuid4(),
            title='Test Book',
            author='Test Author',
            created_at='2023-01-01',
            updated_at='2023-01-01',
        )

        self.assertEqual(str(book), book.title)

    def test_creeate_page(self):
        """Test creating a page"""
        book = models.Book.objects.create(
            uuid=uuid.uuid4(),
            title='Test Book',
            author='Test Author',
            created_at='2023-01-01',
            updated_at='2023-01-01',
        )
        page = models.Page.objects.create(
            uuid=uuid.uuid4(),
            book=book,
            number=1,
            content='This is a test page.',
        )

        self.assertEqual(str(page), f'Page {page.number} of {page.book.title}')
