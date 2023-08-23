from django.db import models

from config import settings
from  users.models import User
from users.models import NULLABLE


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(upload_to='course/', **NULLABLE, verbose_name='превью (картинка)')
    description = models.TextField(verbose_name='описание')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='lesson/', **NULLABLE, verbose_name='превью (картинка)')
    video = models.URLField(**NULLABLE, verbose_name='ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, verbose_name='курс')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.name

class Payments(models.Model):
    CASH = 'cash'
    TRANSFER = 'transfer'
    PAYMENT_CHOICES = [
        (CASH, 'наличные'),
        (TRANSFER, 'перевод')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, **NULLABLE, on_delete=models.CASCADE, verbose_name='пользователь')
    payment_date = models.DateField(auto_now_add=True, verbose_name='дата платежа')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, verbose_name='оплаченный курс')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE, verbose_name='оплаченный урок')
    payment_amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    method_payment = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default=CASH, verbose_name='способ оплаты')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f'{self.user}: ({self.paid_course if self.paid_course else self.paid_lesson})'
    

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    status = models.BooleanField(default=True, verbose_name='статус подписки')

    class Meta:
        verbose_name = "подписка"
        verbose_name_plural = "подписки"
    

