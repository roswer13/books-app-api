"""
Test the book APIs.
"""
import uuid
import time

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Book, Page

from book.serializers import (
    BookSerializer,
    PageSerializer,
    PageDetailSerializer
)


BOOKS_URL = reverse("book:book-list")
PAGES_URL = reverse("book:page-list")


def detail_url(book_uuid: str):
    """Return book detail URL."""
    return reverse("book:book-detail", args=[book_uuid])


def detail_page_url(page_uuid: str):
    """Return page detail URL."""
    return reverse("book:page-detail", args=[page_uuid])


def create_user(**params):
    """Create and return a user."""
    return get_user_model().objects.create_user(**params)


def create_editor_user(**params):
    """Create and return an editor user."""
    return get_user_model().objects.create_editor_user(**params)


def create_book_and_page(**params):
    """Create and return a book and page."""
    default_params = {
        "title": "Test Book",
        "author": "Test Author",
    }
    default_params.update(params)
    book = Book.objects.create(**default_params)

    for i in range(1, 3):
        Page.objects.create(
            book=book,
            number=i,
            content=f"Test Content {i}",
        )

    return book


class PublicBookAPITests(TestCase):
    """Test the publicly available book API."""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """Test that authentication is required for book API."""
        res = self.client.get(BOOKS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBookAPIUserReaderTests(TestCase):
    """Test the authorized user book API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='testpass')
        self.client.force_authenticate(self.user)

    # Book API tests for a user with reader role.

    def test_create_book(self):
        """Test creating a book does not access."""
        payload = {
            "title": "Test Book",
            "author": "Test Author",
        }
        res = self.client.post(BOOKS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book(self):
        """Test updating a book does not access."""
        book = create_book_and_page()
        payload = {
            "title": "Updated Book",
            "author": "Updated Author",
        }

        url = detail_url(book.uuid)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book(self):
        """Test deleting a book does not access."""
        book = create_book_and_page()

        url = detail_url(book.uuid)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_book(self):
        """Test retrieving a book."""
        book = create_book_and_page()

        url = detail_url(book.uuid)
        res = self.client.get(url)
        serializer = BookSerializer(book)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_book_list(self):
        """Test retrieving a list of books."""
        create_book_and_page(title="Book 1")
        create_book_and_page(title="Book 2")

        res = self.client.get(BOOKS_URL)
        books = Book.objects.all().order_by("-created_at")
        serializer = BookSerializer(books, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_retrieve_book_list_page(self):
        """Test retrieving a paginated list of books."""
        for i in range(1, 21):
            create_book_and_page(title=f"Book {i}")

        res = self.client.get(BOOKS_URL, {"page": 2})
        books = Book.objects.all().order_by("-created_at")[10:20]
        serializer = BookSerializer(books, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    # Page API tests for a user with reader role.

    def test_create_page(self):
        """Test creating a page does not access."""
        book = create_book_and_page()
        payload = {
            "book": book.uuid,
            "number": 1,
            "content": "Test Content",
        }
        res = self.client.post(PAGES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_page(self):
        """Test updating a page does not access."""
        book = create_book_and_page()
        page = book.pages.first()
        payload = {
            "book": book.uuid,
            "number": 1,
            "content": "Updated Content",
        }

        url = detail_page_url(page.uuid)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_page(self):
        """Test deleting a page does not access."""
        book = create_book_and_page()
        page = book.pages.first()

        url = detail_page_url(page.uuid)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_page_list(self):
        """Test retrieving a list of pages."""
        book = create_book_and_page()

        res = self.client.get(PAGES_URL, {"book_uuid": book.uuid})
        pages = Page.objects.filter(book=book).order_by("number")
        serializer = PageSerializer(pages, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_restrive_page_list_pagination(self):
        """Test retrieving a paginated list of pages."""
        book = create_book_and_page()
        for i in range(3, 30):
            Page.objects.create(
                book=book,
                number=i,
                content=f"Test Content {i}",
            )

        res = self.client.get(PAGES_URL, {"book_uuid": book.uuid, "page": 2})
        pages = Page.objects.filter(book=book).order_by("number")[15:30]
        serializer = PageSerializer(pages, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_retrieve_page_list_invalid_book_uuid(self):
        """Test retrieving a list of pages with invalid book UUID."""
        create_book_and_page()

        res = self.client.get(PAGES_URL, {"book_uuid": str(uuid.uuid4())})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], [])

    def test_retrieve_page(self):
        """Test retrieving a page."""
        book = create_book_and_page()
        page = book.pages.first()

        url = detail_page_url(page.uuid)
        res = self.client.get(url)
        serializer = PageDetailSerializer(page)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class PrivateBookAPITests(TestCase):
    """Test the authorized user book API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_editor_user(
            email='user@example.com', password='testpass'
        )
        self.client.force_authenticate(self.user)

    # Book API tests for a user with editor role.
    def test_create_book(self):
        """Test creating a book."""
        payload = {
            "title": "Test Book",
            "author": "Test Author",
        }
        res = self.client.post(BOOKS_URL, payload)
        book = Book.objects.get(uuid=res.data["uuid"])
        serializer = BookSerializer(book)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(book.title, payload["title"])
        self.assertEqual(book.author, payload["author"])
        self.assertEqual(
            book.created_at.replace(microsecond=0),
            book.updated_at.replace(microsecond=0)
        )

    def test_update_book(self):
        """Test updating a book."""
        book = create_book_and_page()
        time.sleep(1)  # Ensure the updated_at timestamp changes

        payload = {
            "title": "Updated Book",
            "author": "Updated Author",
        }

        url = detail_url(book.uuid)
        res = self.client.patch(url, payload)
        book.refresh_from_db()

        serializer = BookSerializer(book)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(book.title, payload["title"])
        self.assertEqual(book.author, payload["author"])
        self.assertNotEqual(book.created_at, book.updated_at)

    def test_delete_book(self):
        """Test deleting a book."""
        book = create_book_and_page()

        url = detail_url(book.uuid)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(uuid=book.uuid).exists())

    def test_retrieve_book(self):
        """Test retrieving a book."""
        book = create_book_and_page()

        url = detail_url(book.uuid)
        res = self.client.get(url)
        serializer = BookSerializer(book)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_book_list(self):
        """Test retrieving a list of books."""
        create_book_and_page(title="Book 1")
        create_book_and_page(title="Book 2")

        res = self.client.get(BOOKS_URL)
        books = Book.objects.all().order_by("-created_at")
        serializer = BookSerializer(books, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_retrieve_book_list_pagination(self):
        """Test retrieving a paginated list of books."""
        for i in range(1, 21):
            create_book_and_page(title=f"Book {i}")

        res = self.client.get(BOOKS_URL, {"page": 2})
        books = Book.objects.all().order_by("-created_at")[10:20]
        serializer = BookSerializer(books, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    # Page API tests for a user with editor role.

    def test_create_page(self):
        """Test creating a page."""
        book = create_book_and_page()
        payload = {
            "book": book.uuid,
            "number": 6,
            "content": "Test Content",
        }
        res = self.client.post(PAGES_URL, payload)
        page = Page.objects.get(uuid=res.data["uuid"])
        serializer = PageSerializer(page)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(page.book, book)
        self.assertEqual(page.number, payload["number"])
        self.assertEqual(page.content, payload["content"])

    def test_create_page_and_validate_book_update_at(self):
        """Test creating a page and validating book updated_at."""
        book = create_book_and_page()
        before_created_at = book.updated_at
        before_updated_at = book.updated_at

        time.sleep(1)  # Ensure the updated_at timestamp changes

        payload = {
            "book": book.uuid,
            "number": 6,
            "content": "Test Content",
        }
        res = self.client.post(PAGES_URL, payload)
        book.refresh_from_db()

        page = Page.objects.get(uuid=res.data["uuid"])
        serializer = PageSerializer(page)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(
            book.created_at.replace(microsecond=0),
            before_created_at.replace(microsecond=0)
        )
        self.assertNotEqual(book.updated_at, before_updated_at)

    def test_create_page_number_already_exists(self):
        """Test creating a page with an existing number."""
        book = create_book_and_page()
        payload = {
            "book": book.uuid,
            "number": 1,
            "content": "Test Content",
        }
        res = self.client.post(PAGES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_page(self):
        """Test updating a page."""
        book = create_book_and_page()
        page = book.pages.first()
        payload = {
            "book": book.uuid,
            "number": 1,
            "content": "Updated Content",
        }

        url = detail_page_url(page.uuid)
        res = self.client.patch(url, payload)
        page.refresh_from_db()
        book.refresh_from_db()
        serializer = PageDetailSerializer(page)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(page.book, book)
        self.assertEqual(page.number, payload["number"])
        self.assertEqual(page.content, payload["content"])

    def test_update_page_number_already_exists(self):
        """Test updating a page with an existing number."""
        book = create_book_and_page()
        page = book.pages.first()
        payload = {
            "number": 2,
            "content": "Updated Content",
        }

        url = detail_page_url(page.uuid)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_page(self):
        """Test deleting a page."""
        book = create_book_and_page()
        page = book.pages.first()

        url = detail_page_url(page.uuid)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Page.objects.filter(uuid=page.uuid).exists())

    def test_retrieve_page(self):
        """Test retrieving a page."""
        book = create_book_and_page()
        page = book.pages.first()

        url = detail_page_url(page.uuid)
        res = self.client.get(url)
        serializer = PageDetailSerializer(page)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_page_list(self):
        """Test retrieving a list of pages."""
        book = create_book_and_page()

        res = self.client.get(PAGES_URL, {"book_uuid": book.uuid})
        pages = Page.objects.filter(book=book).order_by("number")
        serializer = PageSerializer(pages, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_retrieve_page_list_invalid_book_uuid(self):
        """Test retrieving a list of pages with invalid book UUID."""
        create_book_and_page()

        res = self.client.get(PAGES_URL, {"book_uuid": str(uuid.uuid4())})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], [])

    def test_retrieve_page_list_pagination(self):
        """Test retrieving a paginated list of pages."""
        book = create_book_and_page()
        for i in range(3, 30):
            Page.objects.create(
                book=book,
                number=i,
                content=f"Test Content {i}",
            )

        res = self.client.get(PAGES_URL, {"book_uuid": book.uuid, "page": 2})
        pages = Page.objects.filter(book=book).order_by("number")[15:30]
        serializer = PageSerializer(pages, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)
