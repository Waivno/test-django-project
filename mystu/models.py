from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from myapp.models import Product


class Lesson(models.Model):
    name = models.CharField(max_length=250)
    video_url = models.URLField()
    duration = models.IntegerField(validators=[MinValueValidator(0)])
    products = models.ManyToManyField(Product, related_name='lessons')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['created_at']


class LessonViewStatus(models.Model):
    VIEWED = 'V'
    NOT_VIEWED = 'NV'
    STATUS_CHOICES = ((VIEWED, 'VIEWED'), (NOT_VIEWED, 'NOT_VIEWED'))

    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_statuses', db_index=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=NOT_VIEWED)
    view_time = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.lesson.name} ({self.status})"

    class Meta:
        unique_together = ('user', 'lesson')
        verbose_name = 'Статус просмотра урока'
        verbose_name_plural = 'Статусы просмотра уроков'
        indexes = [
            models.Index(fields=['user', 'lesson']),
            models.Index(fields=['lesson', 'status']),
        ]
        ordering = ['-created_at']