# Create your views here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .utils import authenticate_key,get_referalurl
from .serializers import UserSerializers,LoginSerializer
from .models import User,Wallet
from .exceptions import IncorrectData,IncorrectAuthCredentials

class GetUser(APIView):
    """ this api retrives all users and save users  """

    def get(self,request,*args,**kwargs):
        """get method reterive all users"""


        obj = User.objects.all()
        serializer = UserSerializers(obj, many=True)
        return Response(serializer.data)


    def post(self,request,*args,**kwargs):
        """post methods saves the users  either self signup or referal signup"""

        if kwargs['key'] is not None and kwargs['key'] != "":
            refered_user=authenticate_key(kwargs['key'])
            if refered_user:
                serializer = UserSerializers(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    Wallet.objects.create(user_id=refered_user.id,refered_to_id=serializer.data['id'],credits=100)
                    Wallet.objects.create(user_id=serializer.data['id'],credits=100)
                    referal_url = get_referalurl(request, serializer.data['referal_code'])
                    return Response({'referal_url': referal_url,"is_rewarded":True}, status=status.HTTP_200_OK)
                else:
                    raise IncorrectData(detail=serializer.errors, code=400)
            else:
                raise IncorrectData(detail="fake referal code", code=400)
        else:
            serializer = UserSerializers(data=request.data)
            if  serializer.is_valid(raise_exception=True):
                serializer.save()
                referal_url = get_referalurl(request,serializer.data['referal_code'])
                return Response({'referal_url':referal_url}, status=status.HTTP_200_OK)
            else:
                raise IncorrectData(detail=serializer.errors, code=400)

get_user = GetUser.as_view()



class LoginUser(APIView):
    """this api is used to authenticate user and retrive details"""

    def post(self,request,*args,**kwargs):
        """ post method to authenticate the users provided email and password """

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(request, email=(request.data['email']), password=request.data['password'])
        else:
            raise IncorrectData(detail=serializer.errors,code=400)
        if not user:
            raise IncorrectAuthCredentials(detail="Incorrect authentication credentials",code=401)
        url = get_referalurl(request,user.referal_code)
        total_earned = user.get_rewards()
        return Response({'total_earned':total_earned,"referal_url":url}, status=status.HTTP_200_OK)


login_user = LoginUser.as_view()



