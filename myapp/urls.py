from django.urls import path

from b_test.myapp.views import ProductStatsView

urlpatterns = [

    path('api/products-stats/', ProductStatsView.as_view(), name='product_stats_view'),

]