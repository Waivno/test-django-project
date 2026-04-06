from django.contrib import admin
from mystu.models import Lesson, LessonViewStatus


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration', 'get_products_count', 'created_at']
    search_fields = ['name']
    filter_horizontal = ['products']
    readonly_fields = ['created_at', 'updated_at']

    def get_products_count(self, obj):
        return obj.products.count()
    get_products_count.short_description = 'Продукты'


@admin.register(LessonViewStatus)
class LessonViewStatusAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'status', 'view_time', 'created_at']
    list_filter = ['status', 'lesson']
    search_fields = ['user__username', 'lesson__name']
    raw_id_fields = ['user', 'lesson']
    readonly_fields = ['created_at', 'updated_at']
