from rest_framework import serializers
from .validators import YoutubeLinkValidator
from .models import Subscription


from course.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = serializers.URLField(validators=[YoutubeLinkValidator()])


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    subscription_status = serializers.SerializerMethodField()

    def get_lessons_count(self, instance):
        lessons = Lesson.objects.filter(course=instance).all()
        if lessons:
            return lessons.count()
        return 0

    def get_subscription_status(self, instance):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                subscription = Subscription.objects.get(user=request.user, course=instance)
                return True
            except Subscription.DoesNotExist:
                return False
        return False

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "preview",
            "description",
            "lessons_count",
            "lessons",
            "subscription_status",  
        )
