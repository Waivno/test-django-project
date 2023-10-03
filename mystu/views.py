from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from models import Lesson
from serializers import LessonSerializer
from b_test.myapp.models import Product, ProductAccess
# from myapp.serializers import ProductSerializer
class LessonsView(APIView):#  отображает все уроки, к которым пользователь имеет доступ

    def get(self, request):
        product_accesses = ProductAccess.objects.filter(user=request.user)
        lessons = Lesson.objects.filter(products__in=product_accesses.values_list('product_id', flat=True))
        serializer = LessonSerializer(lessons, many=True, context={'request': request})
        return Response(serializer.data)

class LessonProductView(APIView):#  отображает все уроки по конкретному продукту, к которому пользователь имеет доступ

    def get(self, request, product_id):
        product = Product.objects.filter(id=product_id, accesses__user=request.user).first()
        if not product:
            return Response({'message': 'No access to product or product does not exist'}, status=status.HTTP_403_FORBIDDEN)
        lessons = product.lessons.all().order_by('-lesson_statuses__created_at')
        serializer = LessonSerializer(lessons, many=True, context={'request': request})
        return Response(serializer.data)