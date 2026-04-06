from rest_framework import serializers
from mystu.models import Lesson, LessonViewStatus


class LessonViewStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonViewStatus
        fields = ['status', 'view_time']


class LessonSerializer(serializers.ModelSerializer):
    view_status = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'video_url', 'duration', 'products', 'view_status']

    def get_view_status(self, obj):
        # Используем prefetch_related данные для оптимизации
        if hasattr(obj, '_prefetched_objects_cache') and 'lesson_statuses' in obj._prefetched_objects_cache:
            view_status = next(
                (ls for ls in obj.lesson_statuses.all() 
                 if ls.user_id == self.context['request'].user.id), 
                None
            )
        else:
            view_status = LessonViewStatus.objects.filter(
                lesson=obj, 
                user=self.context['request'].user
            ).first()
            
        if view_status:
            return {
                'status': view_status.status,
                'view_time': view_status.view_time,
            }
        return None