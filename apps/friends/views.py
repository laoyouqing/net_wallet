import json
from urllib.parse import urlencode

import requests
from django.shortcuts import render

# Create your views here.
from rest_framework import status, mixins, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from friends.models import FriendApply, my_friends
from friends.serializers import FriendInfoSerializer, MyFriendSerializer, NewFriendSerializer, MyCodeSerializer, \
    ReceiptCodeSerializer
from users.models import User
from users.utils import has_exist


class FriendInfoView(GenericAPIView):
    '''好友申请'''
    serializer_class = FriendInfoSerializer
    queryset = FriendApply.objects.all()

    def get(self,request):
        fri_code=request.query_params.get('fri_code')
        token=self.request.query_params.get('token')
        user = has_exist(token)
        if user:
            params={
                'token':fri_code,
                'api':'user_info',
            }
            str_param = urlencode(params)
            resp = requests.post('http://wangbo.ie1e.com/ifs/interface.ashx', data=str_param, headers={'Content-Type': 'application/x-www-form-urlencoded'})
            resp=json.loads(resp.content)
            if resp['resultcode']=='0':
                id = resp['data']['user']['id']
                is_friend=False
                friend = my_friends.objects.filter(user=user, friends_id=id,status=1)
                if friend:
                    is_friend = True
                try:
                    friend_apply = FriendApply.objects.get(id=id)
                except:
                    name = resp['data']['user']['name']
                    if name == '':
                        name = resp['data']['user']['nickname']
                    username = name
                    photo=resp['data']['user']['headimg']
                    email=resp['data']['user']['email']
                    fri_code = resp['data']['user']['FrinQCode']
                    pay_code = resp['data']['user']['PayQCode']
                    telphone = resp['data']['user']['phone']
                    friend_apply=FriendApply.objects.create(id=id,username=username,photo=photo,email=email,pay_code=pay_code,fri_code=fri_code,telphone=telphone)
                try:
                    FriendApply.objects.get(id=user.id)
                except:
                    FriendApply.objects.create(id=user.id, username=user.username, photo=user.photo, email=user.email,pay_code=user.pay_code,fri_code=user.fri_code,telphone=user.telphone)
                dict={}
                dict['is_friend']=is_friend
                serializer = self.get_serializer(friend_apply)
                dict['friend_info'] = serializer.data
                return Response(dict)
            else:
                return Response({'msg':'fri_code无效'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg': 'token无效'}, status=status.HTTP_401_UNAUTHORIZED)



    def post(self,request):
        '''加为好友'''
        token=self.request.query_params.get('token')
        friend_id = request.data.get('friend_id')
        user=has_exist(token)
        if user:
            if not (token and friend_id):
                return Response({'msg':'参数不完整'},status=status.HTTP_400_BAD_REQUEST)
            try:
                my_friends.objects.get(user=user,friends_id=friend_id)
            except:
                my_friends.objects.create(user=user, friends_id=friend_id)
                my_friends.objects.create(user_id=friend_id, friends_id=user.id)
            return Response({'msg': '等待对方确认接受'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'token无效'}, status=status.HTTP_401_UNAUTHORIZED)




    def patch(self,request,pk):
        '''更新好友申请状态'''
        sta = request.data.get('status')
        # friend_id = request.data.get('friend_id')
        token=request.query_params.get('token')
        user = has_exist(token)
        if user:
            friend1=my_friends.objects.get(user=user,friends_id=pk)
            friend2=my_friends.objects.get(user_id=pk,friends_id=user.id)
            friend1.status=sta
            friend2.status=sta
            friend1.save()
            friend2.save()
            return Response({'msg':'操作成功'},status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'token无效'}, status=status.HTTP_401_UNAUTHORIZED)




class MyFriendView(mixins.ListModelMixin,viewsets.GenericViewSet):
    '''我的好友'''

    serializer_class = MyFriendSerializer
    queryset = my_friends.objects.all()

    def list(self, request, *args, **kwargs):
        token = self.request.query_params.get('token')
        user = has_exist(token)
        if user:
            friends=my_friends.objects.filter(user=user,status=1)
            ser=self.get_serializer(friends,many=True)
            return Response(ser.data)
        else:
            return Response({'msg': 'token无效'}, status=status.HTTP_401_UNAUTHORIZED)




class NewFriendView(mixins.ListModelMixin,viewsets.GenericViewSet):
    '''新的朋友'''

    serializer_class = NewFriendSerializer
    queryset = my_friends.objects.all()

    def list(self, request, *args, **kwargs):
        token = self.request.query_params.get('token')
        user = has_exist(token)
        if user:
            friends = my_friends.objects.filter(user=user)
            ser = self.get_serializer(friends, many=True)
            return Response(ser.data)
        else:
            return Response({'msg': 'token无效'}, status=status.HTTP_401_UNAUTHORIZED)





class MyCodeView(GenericAPIView):
    '''添加好友-我的二维码'''

    serializer_class = MyCodeSerializer

    def get(self,request):
        token = self.request.query_params.get('token')
        user = has_exist(token)
        if user:
            ser=self.get_serializer(user)
            return Response(ser.data)
        else:
            return Response({'msg': 'token无效'}, status=status.HTTP_401_UNAUTHORIZED)



class ReceiptCodeView(GenericAPIView):
    '''收款二维码'''

    serializer_class = ReceiptCodeSerializer

    def get(self,request):
        token = self.request.query_params.get('token')
        user = has_exist(token)
        if user:
            ser=self.get_serializer(user)
            return Response(ser.data)
        else:
            return Response({'msg': 'token无效'}, status=status.HTTP_401_UNAUTHORIZED)
