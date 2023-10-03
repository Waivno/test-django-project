from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.db import models
from rest_framework.response import Response
from rest_framework.views import APIView

from b_test.myapp.models import Product
from b_test.myapp.serializers import ProductSerializer
from b_test.mystu.models import LessonViewStatus





class ProductStatsView(APIView):# отображает статистику по продуктам

    def get(self, request):
        products = Product.objects.all().annotate(
            students=Count('accesses'),
            lesson_views=Sum(models.Case(models.When(lessons__lesson_statuses__status=LessonViewStatus.VIEWED, then=1), default=0, output_field=models.IntegerField())),
            total_view_time=Sum('lessons__lesson_statuses__view_time'),
        ).annotate(
            purchase_rate=models.ExpressionWrapper(models.F('students') / User.objects.count() * 100, output_field=models.DecimalField()),
        )
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)