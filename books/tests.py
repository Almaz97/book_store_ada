from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from .models import Book, Publisher, BookComment, Genre
from model_mommy import mommy


class BookViewSetTestCase(APITestCase):

    def setUp(self):
        # Создаем пользователя и клиента для авторизации
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.books = mommy.make('books.Book')
        self.book = Book.objects.create(title='Test Book',
                                        author='Test Author',
                                        amount_of_pages=500,
                                        is_deleted=False)
        self.genre = Genre.objects.create(title='Drama')

    def test_get_books_unauthenticated(self):
        url = reverse('books-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_create_book_unauthenticated(self):
        data = {'title': 'New Book', 'author': 'New Author'}
        url = reverse('books-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 401)  # Unauthorized

    def test_create_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "Harry Potter",
            "description": "Harry Potter",
            "genre": [self.genre.id],
            "amount_of_pages": 600,
            "author": "Name of Author"
        }
        url = reverse('books-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(
            response.data['genre'][0],
            {'id': self.genre.id, 'title': self.genre.title}
        )

    def test_soft_delete_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('books-detail', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertTrue(Book.objects.get(id=self.book.id).is_deleted)










# class BookCommentViewSetTestCase(APITestCase):
#
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='testpass')
#         self.client = APIClient()
#         self.book = Book.objects.create(title='Test Book', author='Test Author', is_deleted=False)
#         self.comment = BookComment.objects.create(book=self.book, text="Test Comment")
#
#     def test_get_comments_unauthenticated(self):
#         url = reverse('books-comments-detail', args=[self.book.pk])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#
#
# class PublisherViewSetTestCase(APITestCase):
#
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='testpass')
#         self.client = APIClient()
#         self.publisher = Publisher.objects.create(name='Test Publisher')
#
#     def test_get_publishers_unauthenticated(self):
#         url = reverse('publishers-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
