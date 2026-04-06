from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from mystu.models import Lesson, LessonViewStatus
from myapp.models import Product, ProductAccess


class MystuModelTest(TestCase):
    """Тесты для моделей mystu."""

    def test_lesson_str(self):
        """Проверка строкового представления урока."""
        lesson = Lesson.objects.create(
            name='Test Lesson',
            video_url='http://example.com/video.mp4',
            duration=60
        )
        self.assertEqual(str(lesson), 'Test Lesson')

    def test_lesson_view_status_str(self):
        """Проверка строкового представления статуса просмотра."""
        user = User.objects.create_user(username='testuser', password='testpass')
        lesson = Lesson.objects.create(
            name='Test Lesson',
            video_url='http://example.com/video.mp4',
            duration=60
        )
        view_status = LessonViewStatus.objects.create(
            user=user,
            lesson=lesson,
            status=LessonViewStatus.VIEWED,
            view_time=30
        )
        self.assertIn('testuser', str(view_status))
        self.assertIn('Test Lesson', str(view_status))

    def test_lesson_duration_validation(self):
        """Проверка валидации duration (не может быть отрицательным)."""
        from django.core.exceptions import ValidationError
        
        lesson = Lesson(
            name='Test Lesson',
            video_url='http://example.com/video.mp4',
            duration=-10
        )
        with self.assertRaises(ValidationError):
            lesson.full_clean()

    def test_lesson_view_time_validation(self):
        """Проверка валидации view_time (не может быть отрицательным)."""
        from django.core.exceptions import ValidationError
        
        user = User.objects.create_user(username='testuser', password='testpass')
        lesson = Lesson.objects.create(
            name='Test Lesson',
            video_url='http://example.com/video.mp4',
            duration=60
        )
        view_status = LessonViewStatus(
            user=user,
            lesson=lesson,
            view_time=-5
        )
        with self.assertRaises(ValidationError):
            view_status.full_clean()
