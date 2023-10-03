from django.urls import path
from views import LessonsView, LessonProductView

urlpatterns = [
    path('api/lessons/', LessonsView.as_view(), name='lessons_view'),
    path('api/lessons/product/<int:product_id>/', LessonProductView.as_view(), name='lessons_product_view'),
]