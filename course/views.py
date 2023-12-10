from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from course.models import Course, Lesson, Payments, Subscription
from course.paginators import CustomPageNumberPagination
from course.serializers import CourseSerializer, LessonSerializer
from course.validators import YoutubeLinkValidator
from users.serializers import PaymentSerializer
from course.permissions import IsModeratorPermission, IsOwnerOrReadOnly


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CustomPageNumberPagination  # Используем кастомный пагинатор
    validator_class = YoutubeLinkValidator  # Использует валидаор ссылок на YouTube

    def get_permissions(self):
        # В зависимости от роли пользователя, возвращаем соответствующий набор прав доступа
        if self.request.user.groups.filter(name='Модераторы').exists():
            return [IsModeratorPermission()]
        else:
            return [IsOwnerOrReadOnly()]

    def perform_create(self, serializer):
        # Устанавливаем текущего пользователя владельцем курса при создании
        serializer.save(owner=self.request.user)


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = CustomPageNumberPagination  # Используем кастомный пагинатор

    def get_permissions(self):
        # В зависимости от роли пользователя, возвращаем соответствующий набор прав доступа
        if self.request.user.groups.filter(name='Модераторы').exists():
            return [IsModeratorPermission()]
        else:
            return [IsOwnerOrReadOnly()]


class LessonCreateView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    validator_class = YoutubeLinkValidator

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


class SubscribeToCourseView(generics.GenericAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        course = Course.objects.get(pk=pk)
        user = request.user

        if not Subscription.objects.filter(user=user, course=course).exists():
            subscription = Subscription(user=user, course=course)
            subscription.save()
            return Response({'message': 'Successfully subscribed.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Already subscribed.'}, status=status.HTTP_200_OK)


class UnsubscribeFromCourseView(generics.GenericAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        course = Course.objects.get(pk=pk)
        user = request.user

        try:
            subscription = Subscription.objects.get(user=user, course=course)
            subscription.delete()
            return Response({'message': 'Successfully unsubscribed.'}, status=status.HTTP_204_NO_CONTENT)
        except Subscription.DoesNotExist:
            return Response({'message': 'Not subscribed.'}, status=status.HTTP_200_OK)
