# Create your views here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import generate_secretkey,authenticate_key,get_referalurl
from .serializers import UserSerializers
from .models import User,Wallet
from .exceptions import IncorrectData

class GetUser(APIView):


    def get(self,request,*args,**kwargs):
        if kwargs['key'] is not None or kwargs['key'] is  None  :
            obj = User.objects.all()
            serializer = UserSerializers(obj, many=True)
        return Response(serializer.data)


    def post(self,request,*args,**kwargs):
        if kwargs['key'] is not None and kwargs['key'] != "":
            refered_user=authenticate_key(kwargs['key'])
            if refered_user:
                serializer = UserSerializers(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(referal_code=generate_secretkey())
                    Wallet.objects.create(user_id=serializer.data['id'],refered_id=refered_user.id,credits=100)
                    Wallet.objects.create(user_id=refered_user.id,refered_id=serializer.data['id'],credits=100)
                    referal_url = get_referalurl(request, serializer.data)
                    return Response({'data': referal_url,"is_rewardwed":True}, status=status.HTTP_200_OK)
                else:
                    raise IncorrectData(detail=serializer.errors, code=400)
            else:
                print "last falsee"
                return Response({'data': "fake referance id"}, status=status.HTTP_200_OK)

        else:
            serializer = UserSerializers(data=request.data)
            if  serializer.is_valid(raise_exception=True):
                serializer.save(referal_code=generate_secretkey())
                referal_url = get_referalurl(request,serializer.data)
                return Response({'data':referal_url}, status=status.HTTP_200_OK)
            else:
                raise IncorrectData(detail=serializer.errors, code=400)

get_user = GetUser.as_view()



class LoginUser(APIView):


    def post(self,request,*args,**kwargs):
        print request.data['email']
        print request.data['password']
        return Response({'data': request.data}, status=status.HTTP_200_OK)


login_user = LoginUser.as_view()



