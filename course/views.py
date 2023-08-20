from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter

from course.models import Course, Lesson, Payments
from course.serializers import CourseSerializer, LessonSerializer
from users.serializers import PaymentSerializer
from course.permissions import IsModeratorPermission, IsOwnerOrReadOnly


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    
    def get_permissions(self):
        #В зависимости от роли пользователя, возвращаем соответствующий набор прав доступа
        if self.request.user.groups.filter(name='Модераторы').exists():
            return [IsModeratorPermission()]
        else:
            return [IsOwnerOrReadOnly()]

    def perform_create(self, serializer):
        #Устанавливаем текущего пользователя владельцем курса при создании
        serializer.save(owner=self.request.user)


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_permissions(self):
        # В зависимости от роли пользователя, возвращаем соответствующий набор прав доступа
        if self.request.user.groups.filter(name='Модераторы').exists():
            return [IsModeratorPermission()]
        else:
            return [IsOwnerOrReadOnly()]

class LessonCreateView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def perform_create(self, serializer):
        # Устанавливаем текущего пользователя владельцем урока при создании
        serializer.save(owner=self.request.user)

class LessonDeleteView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_permissions(self):
        # В зависимости от роли пользователя, возвращаем соответствующий набор прав доступа
        if self.request.user.groups.filter(name='Модераторы').exists():
            return [IsModeratorPermission()]
        else:
            return [IsOwnerOrReadOnly()]

class LessonDetailView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_permissions(self):
        # В зависимости от роли пользователя, возвращаем соответствующий набор прав доступа
        if self.request.user.groups.filter(name='Модераторы').exists():
            return [IsModeratorPermission()]
        else:
            return [IsOwnerOrReadOnly()]

class LessonUpdateView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_permissions(self):
        # В зависимости от роли пользователя, возвращаем соответствующий набор прав доступа
        if self.request.user.groups.filter(name='Модераторы').exists():
            return [IsModeratorPermission()]
        else:
            return [IsOwnerOrReadOnly()]


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'method_payment']
    ordering_fields = ['payment_date']


class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()


class PaymentDeleteView(generics.DestroyAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()


class PaymentDetailView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()


class PaymentUpdateView(generics.UpdateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()

