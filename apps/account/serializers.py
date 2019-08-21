from rest_framework import serializers

from account.models import TranAccount
from friends.models import Merchant, FriendApply
from users.models import User


class PaySerializer(serializers.ModelSerializer):
    """
    收付款
    """
    class Meta:
        model = FriendApply
        fields = ('id','username','photo')




class AccountInfoSerializer(serializers.ModelSerializer):
    """
    转账信息
    """
    create_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = TranAccount
        fields = ('user','friends','wbc_balance','create_time','order_id')
        depth=1




class UserInfoSerializer(serializers.ModelSerializer):
    """
    用户信息
    """
    class Meta:
        model = User
        fields = ('id','username','photo')



class FriendInfoSerializer(serializers.ModelSerializer):
    """
    好友信息
    """
    class Meta:
        model = FriendApply
        fields = ('id','username','photo')




class AccountDetailSerializer(serializers.ModelSerializer):
    """
    账单详情
    """

    create_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = TranAccount
        fields = ('user','friends','wbc_balance','pay_info','status','create_time')
        depth=1



class AccountSerializer(serializers.ModelSerializer):
    """
    账单
    """
    username = serializers.CharField(source='friends.username')
    photo = serializers.CharField(source='friends.photo')
    create_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = TranAccount
        fields = ('username','photo','wbc_balance','order_id','status','create_time')

