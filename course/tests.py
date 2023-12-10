from rest_framework import status
from django.urls import reverse
from course.models import Lesson
from users.models import User
from rest_framework.test import APITestCase, APIClient


class LessonTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='user@mail.ru',
            first_name='test',
            last_name='test',
            is_staff=False,
            is_superuser=False
        )

        self.user.set_password('123')
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_get_list(self):
        """Проверка получения списка модулей"""

        data = {'name': 'Test Lesson', 'description': 'Test Description'}
        response = self.client.post('lesson_list', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(Lesson.objects.get().name, 'Test Lesson')
