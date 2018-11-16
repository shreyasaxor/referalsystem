from rest_framework import serializers
from usermgmt.utils import generate_secretkey
from .models import User
from rest_framework.validators import UniqueValidator

class UserSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True,validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model=User
        fields = ('id','email', 'password','first_name','referal_code')
        extra_kwargs = {'password': {'write_only': True},'first_name':{'required':True}}

    def create(self, validated_data):
        print validated_data
        email = validated_data.pop('email')
        first_name = validated_data.pop('first_name')
        password = validated_data.pop('password')
        user = User.objects.create(email=email, first_name=first_name,referal_code=generate_secretkey())
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """This is the serializer used for logging in user"""
    email = serializers.EmailField(max_length=256, required=True)
    password = serializers.CharField(required=True, min_length=5,  )

    class Meta:
        model = User
