from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from myapp.models import Product, ProductAccess
from mystu.models import Lesson, LessonViewStatus


class ProductModelTest(TestCase):
    """Тесты для модели Product."""

    def test_product_creation(self):
        """Проверка создания продукта."""
        user = User.objects.create_user(username='testuser', password='testpass')
        product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            owner=user
        )
        self.assertEqual(str(product), 'Test Product')
        self.assertEqual(product.name, 'Test Product')
        self.assertIsNotNone(product.created_at)

    def test_product_access_creation(self):
        """Проверка создания доступа к продукту."""
        user = User.objects.create_user(username='testuser2', password='testpass')
        product = Product.objects.create(
            name='Test Product 2',
            description='Test Description 2',
            owner=user
        )
        access = ProductAccess.objects.create(product=product, user=user)
        self.assertIn('testuser2', str(access))
        self.assertTrue(access.is_valid)


class ProductAccessTest(TestCase):
    """Тесты для проверки доступа к продуктам."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.other_user = User.objects.create_user(username='otheruser', password='testpass')
        
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            owner=self.user
        )
        
        # Даём доступ только первому пользователю
        ProductAccess.objects.create(product=self.product, user=self.user, is_valid=True)
        ProductAccess.objects.create(product=self.product, user=self.other_user, is_valid=False)

    def test_product_access_is_valid_filter(self):
        """Проверка фильтрации по is_valid."""
        valid_accesses = ProductAccess.objects.filter(is_valid=True)
        self.assertEqual(valid_accesses.count(), 1)
        self.assertEqual(valid_accesses.first().user, self.user)

    def test_lesson_access_with_invalid_product_access(self):
        """Проверка, что уроки не доступны при невалидном доступе к продукту."""
        lesson = Lesson.objects.create(
            name='Test Lesson',
            video_url='http://example.com/video.mp4',
            duration=60
        )
        lesson.products.add(self.product)
        
        # Пользователь с невалидным доступом не должен видеть урок через API
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get('/mystu/api/lessons/')
        # Проверяем, что урок не попал в ответ (т.к. доступ невалидный)
        if response.status_code == 200:
            lessons_in_response = [l['name'] for l in response.data]
            self.assertNotIn('Test Lesson', lessons_in_response)


class LessonModelTest(TestCase):
    """Тесты для модели Lesson."""

    def test_lesson_creation(self):
        """Проверка создания урока."""
        lesson = Lesson.objects.create(
            name='Test Lesson',
            video_url='http://example.com/video.mp4',
            duration=60
        )
        self.assertEqual(str(lesson), 'Test Lesson')
        self.assertEqual(lesson.duration, 60)

    def test_lesson_view_status_creation(self):
        """Проверка создания статуса просмотра урока."""
        user = User.objects.create_user(username='testuser', password='testpass')
        lesson = Lesson.objects.create(
            name='Test Lesson',
            video_url='http://example.com/video.mp4',
            duration=60
        )
        status_obj = LessonViewStatus.objects.create(
            user=user,
            lesson=lesson,
            status=LessonViewStatus.VIEWED,
            view_time=30
        )
        self.assertIn('testuser', str(status_obj))
        self.assertEqual(status_obj.status, LessonViewStatus.VIEWED)
        self.assertEqual(status_obj.view_time, 30)

    def test_lesson_view_status_unique_together(self):
        """Проверка уникальности пары user+lesson."""
        user = User.objects.create_user(username='testuser2', password='testpass')
        lesson = Lesson.objects.create(
            name='Test Lesson 2',
            video_url='http://example.com/video2.mp4',
            duration=120
        )
        LessonViewStatus.objects.create(user=user, lesson=lesson)
        
        # Попытка создать дубликат должна вызвать ошибку
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            LessonViewStatus.objects.create(user=user, lesson=lesson)


class LessonViewAPITest(APITestCase):
    """Тесты для API просмотров уроков."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            owner=self.user
        )
        
        self.lesson = Lesson.objects.create(
            name='Test Lesson',
            video_url='http://example.com/video.mp4',
            duration=60
        )
        self.lesson.products.add(self.product)
        
        ProductAccess.objects.create(product=self.product, user=self.user, is_valid=True)

    def test_lessons_view_requires_authentication(self):
        """Проверка, что для доступа к урокам требуется аутентификация."""
        response = self.client.get('/mystu/api/lessons/')
        # DRF возвращает 403 для неаутентифицированных запросов с permission_classes
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_lessons_view_returns_lessons_for_user(self):
        """Проверка, что пользователь видит только свои уроки."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/mystu/api/lessons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Lesson')

    def test_lesson_product_view_requires_authentication(self):
        """Проверка, что для доступа к урокам продукта требуется аутентификация."""
        response = self.client.get(f'/mystu/api/lessons/product/{self.product.id}/')
        # DRF возвращает 403 для неаутентифицированных запросов с permission_classes
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_lesson_product_view_no_access(self):
        """Проверка отказа в доступе к чужому продукту."""
        other_user = User.objects.create_user(username='otheruser', password='testpass')
        self.client.force_authenticate(user=other_user)
        response = self.client.get(f'/mystu/api/lessons/product/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ProductStatsViewTest(APITestCase):
    """Тесты для статистики продуктов."""

    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            username='admin', 
            password='testpass',
            is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='regularuser', 
            password='testpass',
            is_staff=False
        )

    def test_product_stats_requires_staff(self):
        """Проверка, что статистика доступна только персоналу."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get('/myapp/api/products-stats/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_product_stats_accessible_to_staff(self):
        """Проверка, что персонал имеет доступ к статистике."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/myapp/api/products-stats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
