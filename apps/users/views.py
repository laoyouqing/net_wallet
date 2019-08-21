import json
from urllib.parse import urlencode

import requests
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render

# Create your views here.
from rest_framework import status, mixins, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from users.models import User, UserPay
from users.serializers import UserWalletSerializer, SetPasswordSerializer, UpdatePasswordSerializer
from users.utils import has_exist


class UserWallet(GenericAPIView):

    serializer_class = UserWalletSerializer

    def get(self,request):
        token=request.query_params.get('token')
        user=has_exist(token)
        if user:
        # params={
        #     'token':token,
        #     'api':'user_info',
        # }
        # str_param = urlencode(params)
        # resp = requests.post('http://192.168.1.12/ifs/interface.ashx', data=str_param, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        # resp=json.loads(resp.content)
        # if resp['resultcode']=='0':

            # id = resp['data']['user']['id']
            # user_token=UserToken.objects.filter(token=token,user_id=id)
            # if not user_token:
            #     UserToken.objects.create(token=token,user_id=id)
            # try:
            #     user=User.objects.get(id=id)
            # except:
            #     username=resp['data']['user']['name']
            #     photo=resp['data']['user']['headimg']
            #     email=resp['data']['user']['email']
            #     fri_code=resp['data']['user']['FrinQCode']
            #     pay_code=resp['data']['user']['PayQCode']
            #     wbc_balance=resp['data']['user']['point']
            #     user=User.objects.create(id=id,username=username,photo=photo,email=email,fri_code=fri_code,pay_code=pay_code,wbc_balance=wbc_balance)
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        else:
            return Response({'msg':'token无效'},status=status.HTTP_401_UNAUTHORIZED)





class SetPassword(mixins.CreateModelMixin,viewsets.GenericViewSet):
    '''设置密码'''

    queryset = UserPay.objects.all()
    serializer_class = SetPasswordSerializer

    def create(self, request, *args, **kwargs):
        '''设置密码'''
        token = request.query_params.get('token')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = has_exist(token)
        if user:
            password = make_password(serializer.validated_data['password'])
            UserPay.objects.create(user=user,password=password)
            return Response({'msg':'设置成功'})
        else:
            return Response({'msg': 'token无效'}, status=status.HTTP_401_UNAUTHORIZED)






class UpdatePassword(mixins.UpdateModelMixin,viewsets.GenericViewSet):
    '''修改密码'''

    queryset = UserPay.objects.all()
    serializer_class =  UpdatePasswordSerializer

    def update(self, request, *args, **kwargs):
        '''修改密码'''
        token = request.query_params.get('token')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = has_exist(token)
        if user:
            user_pay=UserPay.objects.get(user=user)
            if not check_password(serializer.validated_data['oldpassword'], user_pay.password):
                return Response({'msg':'原密码错误'},status=status.HTTP_400_BAD_REQUEST)
            password = make_password(serializer.validated_data['password'])
            user_pay.password=password
            user_pay.save()
            return Response({'msg':'修改成功'})
        else:
            return Response({'msg': 'token无效'}, status=status.HTTP_401_UNAUTHORIZED)

