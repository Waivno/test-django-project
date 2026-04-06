from django.contrib.auth.models import User
from django.db.models import Count, Sum, F, Case, When, IntegerField, ExpressionWrapper, Value
from rest_framework.response import Response
from rest_framework.views import APIView

from myapp.models import Product
from myapp.serializers import ProductSerializer
from mystu.models import LessonViewStatus


class ProductStatsView(APIView):  # отображает статистику по продуктам

    def get(self, request):
        total_users = User.objects.count()
        if total_users == 0:
            purchase_rate_value = Value(0)
        else:
            purchase_rate_value = F('students') / total_users * 100
        
        products = Product.objects.all().annotate(
            students=Count('accesses'),
            lesson_views=Sum(Case(When(lessons__lesson_statuses__status=LessonViewStatus.VIEWED, then=1), default=0, output_field=IntegerField())),
            total_view_time=Sum('lessons__lesson_statuses__view_time'),
        ).annotate(
            purchase_rate=ExpressionWrapper(purchase_rate_value, output_field=IntegerField()),
        )
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)