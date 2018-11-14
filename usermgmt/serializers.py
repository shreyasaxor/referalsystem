from rest_framework import serializers
from .models import User

class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model=User
        fields = ('id', 'email', 'password','first_name','referal_code')
        extra_kwargs = {'password': {'write_only': True},}

        def create(self, validated_data):
            email = validated_data.pop('email')
            first_name = validated_data.pop('first_name')
            password = validated_data.pop('password')
            user = User.objects.create(email=email, first_name=first_name)
            user.set_password(password)
            user.save()
            return user


