from rest_framework import serializers
from models import Lesson, LessonViewStatus

class LessonViewStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonViewStatus
        fields = ['status', 'view_time', 'user', 'lesson'] # можно добавить другие поля

class LessonSerializer(serializers.ModelSerializer):
    view_status = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['name', 'video_url', 'duration', 'products', 'view_status']

    def get_view_status(self, obj):
        view_status = LessonViewStatus.objects.filter(lesson=obj, user=self.context['request'].user)
        if view_status.exists():
            return LessonViewStatusSerializer(view_status.first()).data
        return None