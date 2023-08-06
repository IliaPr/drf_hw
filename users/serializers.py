from rest_framework import serializers

from course.models import Payments
from users.models import User


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(source='payments_set', many=True)

    def create(self, validated_data):
        payment = validated_data.pop('payment_set')
        user = User.objects.create(**validated_data)

        for pay in payment:
            Payments.objects.create(user=user, **pay)

        return user

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'phone',
            'city',
            'avatar',
            'payment',
        )

