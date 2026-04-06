from django.contrib.auth.models import User
from django.db.models import Count, Sum, F, Value, Q, DecimalField
from django.db.models.functions import Cast
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from myapp.models import Product, ProductAccess
from myapp.serializers import ProductSerializer
from mystu.models import LessonViewStatus


class ProductStatsView(APIView):
    """Отображает статистику по продуктам. Доступно только авторизованным пользователям."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Только для администраторов или владельцев продуктов
        if not request.user.is_staff:
            return Response(status=403)
        
        total_users = User.objects.count() or 1  # Избегаем деления на ноль
        
        products = Product.objects.annotate(
            students=Count('accesses', filter=Q(accesses__is_valid=True), distinct=True),
            lesson_views=Count('lessons__lesson_statuses', 
                              filter=Q(lessons__lesson_statuses__status=LessonViewStatus.VIEWED),
                              distinct=True),
            total_view_time=Sum('lessons__lesson_statuses__view_time', 
                               filter=Q(lessons__lesson_statuses__status=LessonViewStatus.VIEWED),
                               default=0),
        ).annotate(
            purchase_rate=Cast(F('students') * 100.0 / Value(total_users), output_field=DecimalField(max_digits=10, decimal_places=2))
        )
        
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)