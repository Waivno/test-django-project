from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from mystu.models import Lesson
from mystu.serializers import LessonSerializer
from myapp.models import Product, ProductAccess


class LessonsView(APIView):
    """Отображает все уроки, к которым пользователь имеет доступ."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        product_accesses = ProductAccess.objects.filter(
            user=request.user, 
            is_valid=True
        ).select_related('product')
        
        lessons = Lesson.objects.filter(
            products__in=product_accesses.values_list('product_id', flat=True)
        ).prefetch_related('lesson_statuses').distinct()
        
        serializer = LessonSerializer(lessons, many=True, context={'request': request})
        return Response(serializer.data)


class LessonProductView(APIView):
    """Отображает все уроки по конкретному продукту, к которому пользователь имеет доступ."""
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        product = Product.objects.filter(
            id=product_id, 
            accesses__user=request.user,
            accesses__is_valid=True
        ).select_related('owner').first()
        
        if not product:
            return Response(
                {'message': 'No access to product or product does not exist'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        lessons = product.lessons.all().prefetch_related('lesson_statuses')
        serializer = LessonSerializer(lessons, many=True, context={'request': request})
        return Response(serializer.data)