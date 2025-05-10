"""
Test for the Django admin modifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """Tests for the Django admin."""

    def setUp(self):
        """Set up the test case."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='password123',
            name='Test User'
        )

    def test_users_list(self):
        """Test that the users are listed on page."""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        # Check that the response is 200 OK
        self.assertEqual(res.status_code, 200)

        # Check that the user is in the response
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test that the edit user page works."""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        # Check that the response is 200 OK
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works."""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        # Check that the response is 200 OK
        self.assertEqual(res.status_code, 200)
