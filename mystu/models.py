from django.db import models
from django.contrib.auth.models import User

from myapp.models import Product


class Lesson(models.Model):
    name = models.CharField(max_length=250)
    video_url = models.URLField()
    duration = models.IntegerField()
    products = models.ManyToManyField(Product, related_name='lessons')

class LessonViewStatus(models.Model):
    VIEWED = 'V'
    NOT_VIEWED = 'NV'
    STATUS_CHOICES = ((VIEWED, 'VIEWED'), (NOT_VIEWED, 'NOT_VIEWED'))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_statuses')
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=NOT_VIEWED)
    view_time = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'lesson')