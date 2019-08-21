import datetime
import json
from urllib.parse import urlencode
import requests
from django.db.models import Q, Count, Sum
from django.utils import timezone
from rest_framework import status, mixins, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from account.models import TranAccount
from friends.models import Merchant, FriendApply
from account.serializers import PaySerializer, AccountInfoSerializer, AccountDetailSerializer, \
    AccountSerializer
from users.models import UserPay, User
from django.contrib.auth.hashers import make_password, check_password
from decimal import Decimal

from users.utils import has_exist, check_year, payapi


class PayView(GenericAPIView):
    '''收付款'''
    serializer_class = PaySerializer

    def get(self,request):
        pay_code=request.query_params.get('pay_code')
        token = request.query_params.get('token')
        if not (pay_code and token):
            return Response({'msg': '参数不完整'}, status=status.HTTP_400_BAD_REQUEST)
        user=has_exist(token)
        if user:
            params = {
                'token': pay_code,
                'api': 'user_info',
            }
            #拼接参数
            str_param = urlencode(params)
            #请求获取商家信息
            resp = requests.post('http://wangbo.ie1e.com/ifs/interface.ashx', data=str_param,headers={'Content-Type': 'application/x-www-form-urlencoded'})
            resp = json.loads(resp.content)

            if resp['resultcode']=='0':
                id = resp['data']['user']['id']
                try:
                    merchat=FriendApply.objects.get(id=id)
                except:
                    username=resp['data']['user']['name']
                    photo=resp['data']['user']['headimg']
                    merchat=FriendApply.objects.create(id=id,username=username,photo=photo)
                try:
                    #判断当前用户是否在FriendApply表中，为后续反查起作用
                    FriendApply.objects.get(id=user.id)
                except:
                    FriendApply.objects.create(id=user.id, username=user.username, photo=user.photo)
                serializer = self.get_serializer(merchat)
                return Response(serializer.data)
            else:
                return Response({'msg':'pay_code无效'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg': 'token无效'}, status=status.HTTP_401_UNAUTHORIZED)


    def post(self,request):
        '''转账 ,收付款'''
        #好友id
        friend_id = request.data.get('friend_id')
        price=request.data.get('price')
        #付款说明
        pay_info=request.data.get('pay_info','')
        password=request.data.get('password')
        sta=request.data.get('status','')
        print(sta)
        token = request.query_params.get('token')
        if not (friend_id and token and price and password):
            return Response({'msg': '参数不完整'}, status=status.HTTP_400_BAD_REQUEST)
        user = has_exist(token)
        print(user)
        if user:
            # try:
            user_pay=UserPay.objects.get(user=user)
            if check_password(password,user_pay.password):

                #更新网博币余额
                user=user_pay.user
                price = Decimal(price)
                if user.wbc_balance>price:
                    # user.wbc_balance-=price
                    # user.save()
                    # 请求api接口
                    friend=FriendApply.objects.get(id=friend_id)
                    resp=payapi(user.pay_code,friend.pay_code,price)
                    print(resp)
                    if resp['resultcode']=='0':
                        curr_time = timezone.now()
                        curr = curr_time.strftime("%Y")
                        print(curr)
                        #创建转账记录
                        if sta=='1':
                            # 创建付款记录
                            uorder_id = datetime.datetime.today().strftime('%Y%m%d%H%M%S') + str(user.id)
                            TranAccount.objects.create(user=user, friends_id=friend_id, wbc_balance=-price,
                                                       pay_info=pay_info, status=1, order_id=uorder_id, years=curr)
                            # 创建收款记录
                            morder_id = datetime.datetime.today().strftime('%Y%m%d%H%M%S') + str(friend_id)
                            TranAccount.objects.create(user_id=friend_id, friends_id=user.id, wbc_balance=price,
                                                       pay_info=pay_info, status=0, order_id=morder_id, years=curr)
                            return Response({'msg': '付款成功', 'wbc_balance': -price}, status=status.HTTP_200_OK)
                        else:
                            uorder_id = datetime.datetime.today().strftime('%Y%m%d%H%M%S') + str(user.id)
                            TranAccount.objects.create(user=user, friends_id=friend_id, wbc_balance=-price,
                                                       pay_info=pay_info, status=2, order_id=uorder_id, years=curr)
                            # 创建对方转账记录
                            forder_id = datetime.datetime.today().strftime('%Y%m%d%H%M%S') + str(friend_id)
                            TranAccount.objects.create(user_id=friend_id, friends_id=user.id, wbc_balance=price,
                                                       pay_info=pay_info, status=0, order_id=forder_id, years=curr)
                            return Response({'msg': '转账成功', 'wbc_balance': -price}, status=status.HTTP_200_OK)
                    else:
                        return Response({'msg': '转账失败'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'msg': '网博币不足'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'msg':'支付密码错误'}, status=status.HTTP_400_BAD_REQUEST)
            # except:
            #     return Response({'msg': 'user_id无效'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg': 'token无效'}, status=status.HTTP_401_UNAUTHORIZED)




class GoPay(APIView):
    '''判断是否设置支付密码'''

    def get(self,request):
        token = request.query_params.get('token')
        user=has_exist(token)
        if user:
            try:
                UserPay.objects.get(user=user)
            except:
                return Response({'msg':'未设置密码','status':0})
            return Response({'msg': '已设置密码', 'status': 1})
        else:
            return Response({'msg': 'token无效'}, status=status.HTTP_401_UNAUTHORIZED)




class TranAccountView(GenericAPIView):
    '''转账'''
    serializer_class = PaySerializer

    def get(self,request):
        pay_code = request.query_params.get('pay_code')
        if not pay_code:
            return Response({'msg': '缺少pay_code'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            friend_apply=FriendApply.objects.get(pay_code=pay_code)
            serializer = self.get_serializer(friend_apply)
            return Response(serializer.data)
        except:
            return Response({'msg':'pay_code无效'},status=status.HTTP_400_BAD_REQUEST)


    # def post(self,request):
    #     '''转账'''
    #     #好友id
    #     friend_id = request.data.get('friend_id')
    #     price=request.data.get('price')
    #     #付款说明
    #     pay_info=request.data.get('pay_info','')
    #     password=request.data.get('password')
    #     token = request.query_params.get('token')
    #     if not (friend_id and token and price and password):
    #         return Response({'msg': '参数不完整'}, status=status.HTTP_400_BAD_REQUEST)
    #     user = has_exist(token)
    #     if user:
    #         try:
    #             user_pay=UserPay.objects.get(user=user)
    #             if check_password(password,user_pay.password):
    #                 #请求api接口
    #                 # pass
    #                 #更新网博币余额
    #                 user=user_pay.user
    #                 price = Decimal(price)
    #                 if user.wbc_balance>price:
    #                     user.wbc_balance-=price
    #                     user.save()
    #                     curr_time = timezone.now()
    #                     curr = curr_time.strftime("%Y")
    #                     print(curr)
    #                     #创建转账记录
    #                     uorder_id = datetime.datetime.today().strftime('%Y%m%d%H%M%S') + str(user.id)
    #                     TranAccount.objects.create(user=user,friends_id=friend_id,wbc_balance=-price,pay_info=pay_info,status=2,order_id=uorder_id,years=curr)
    #                     #创建对方转账记录
    #                     forder_id = datetime.datetime.today().strftime('%Y%m%d%H%M%S') + str(friend_id)
    #                     TranAccount.objects.create(user_id=friend_id,friends_id=user.id,wbc_balance=price,pay_info=pay_info,status=2,order_id=forder_id,years=curr)
    #                     return Response({'msg': '转账成功','wbc_balance':-price}, status=status.HTTP_200_OK)
    #                 else:
    #                     return Response({'msg': '网博币不足'}, status=status.HTTP_400_BAD_REQUEST)
    #             else:
    #                 return Response({'msg':'支付密码错误'}, status=status.HTTP_400_BAD_REQUEST)
    #         except:
    #             return Response({'msg': 'user_id无效'}, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         return Response({'msg': 'token无效'}, status=status.HTTP_401_UNAUTHORIZED)



class AccountInfoView(ReadOnlyModelViewSet):
    '''转账信息,账单详情'''
    queryset = TranAccount.objects.all()
    lookup_field = 'order_id'

    def get_serializer_class(self):
        if self.action == 'list':
            return AccountInfoSerializer
        else:
            return AccountDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        token = request.query_params.get('token')
        user=has_exist(token)
        if user:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            dict = {}
            dict['user_id'] = user.id
            dict['record'] = serializer.data
            return Response(dict)
        else:
            return Response({'msg': 'token无效'}, status=status.HTTP_401_UNAUTHORIZED)


    def list(self, request, *args, **kwargs):
        #好友id
        friend_id = request.query_params.get('friend_id')
        # 用户token
        token = request.query_params.get('token')
        user = has_exist(token)
        if not friend_id or not token:
            return Response({'msg': '参数不完整'}, status=status.HTTP_400_BAD_REQUEST)
        if user:
            tran_accounts=TranAccount.objects.filter(Q(user=user,friends_id=friend_id,status=2)|Q(user_id=friend_id,friends_id=user.id,status=2)).order_by('create_time')
            ser=self.get_serializer(tran_accounts,many=True)
            dict={}
            dict['user_id']=user.id
            dict['record']=ser.data
            return Response(dict)
        else:
            return Response({'msg': 'token无效'}, status=status.HTTP_401_UNAUTHORIZED)



class LastSaleView(mixins.ListModelMixin,viewsets.GenericViewSet):
    '''最近交易'''
    serializer_class = AccountDetailSerializer
    def list(self,request,*args, **kwargs):
        token = request.query_params.get('token')
        user = has_exist(token)
        if user:
            #通过好友分组
            tran_accounts=TranAccount.objects.filter(user=user).values('friends_id').annotate(fri=Count('friends_id'))
            li=[]
            #循环取每个好友最新交易记录
            for tran_account in tran_accounts:
                tran=TranAccount.objects.filter(user=user,friends_id=tran_account['friends_id']).order_by('-create_time').first()
                ser=self.get_serializer(tran)
                li.append(ser.data)
            return Response(li)
        else:
            return Response({'msg': 'token无效'}, status=status.HTTP_401_UNAUTHORIZED)





class AccountView(GenericAPIView):
    '''账单'''
    serializer_class = AccountSerializer

    def get(self,request):
        token = request.query_params.get('token')
        sta = request.query_params.get('status','')
        print(sta)
        if not token:
            return Response({'msg': '缺少token'}, status=status.HTTP_400_BAD_REQUEST)
        user=has_exist(token)
        if user:
            #用来求和
            li1=[]
            #当前时间
            curr_time = timezone.now()
            #当前时间
            year = curr_time.year
            # 一年十二个月每个月天数
            li=check_year(int(year))
            #当前月
            month = curr_time.month
            #获取当前月的天数
            delta = timezone.timedelta(days=li[month])
            #当月最后一天
            curr_time=curr_time+delta
            curr = curr_time.strftime("%Y-%m")
            curr = timezone.datetime.strptime(curr, '%Y-%m')
            lis=[]
            for month in li:
                #过去的总天数
                li1.append(month)
                delta = timezone.timedelta(days=sum(li1))
                #当月的第一天
                next = curr_time-delta
                next1 = next.strftime("%Y-%m")
                next = timezone.datetime.strptime(next1, '%Y-%m')
                if sta:
                    tran_accounts = TranAccount.objects.filter(user=user, create_time__gte=next,create_time__lte=curr,status=sta).order_by('-create_time')
                else:
                    tran_accounts = TranAccount.objects.filter(user=user,create_time__gte=next,create_time__lte=curr).order_by('-create_time')
                #当前月等于上一个月
                curr = next
                if tran_accounts:
                    pay_out=tran_accounts.filter(wbc_balance__lte=0).aggregate(Sum('wbc_balance'))
                    pay_in=tran_accounts.filter(wbc_balance__gt=0).aggregate(Sum('wbc_balance'))
                    pay_out=pay_out['wbc_balance__sum']
                    pay_in = pay_in['wbc_balance__sum']
                    if pay_out==None:
                        pay_out=0
                    if pay_in==None:
                        pay_in=0
                    ser=self.get_serializer(tran_accounts,many=True)
                    dict={}
                    dict['month']=next1
                    dict['record']=ser.data
                    dict['pay_out']=pay_out
                    dict['pay_in']=pay_in
                    lis.append(dict)
            return Response(lis)
        else:
            return Response({'msg': 'token无效'}, status=status.HTTP_401_UNAUTHORIZED)

