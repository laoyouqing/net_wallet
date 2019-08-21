from rest_framework import serializers

from friends.models import FriendApply, my_friends
from users.models import User


class FriendInfoSerializer(serializers.ModelSerializer):
    """
    好友信息
    """

    class Meta:
        model = FriendApply
        fields = ('id', 'username','photo','wallet_url','email','fri_code','pay_code','telphone')



class MyFriendSerializer(serializers.ModelSerializer):
    """
    好友列表
    """
    friend_id=serializers.IntegerField(label='好友ID',source='friends.id')
    username=serializers.CharField(label='好友用户名',source='friends.username')
    photo=serializers.CharField(label='头像',source='friends.photo')
    fri_code=serializers.CharField(label='我的二维码地址（加好友）',source='friends.fri_code')
    pay_code=serializers.CharField(label='收款二维码地址',source='friends.pay_code')

    class Meta:
        model = my_friends
        fields = ('friend_id','username','photo','fri_code','pay_code')
        # fields=('friends',)
        # depth=1


class  NewFriendSerializer(serializers.ModelSerializer):
    """
    好友信息
    """
    friend_id = serializers.IntegerField(label='好友ID', source='friends.id')
    username = serializers.CharField(label='好友用户名', source='friends.username')
    photo = serializers.CharField(label='头像', source='friends.photo')

    class Meta:
        model = my_friends
        fields = ('friend_id','username','photo','status')




class  MyCodeSerializer(serializers.ModelSerializer):
    """
    添加好友-我的二维码
    """

    class Meta:
        model = User
        fields = ('id','fri_code')



class  ReceiptCodeSerializer(serializers.ModelSerializer):
    """
    添加好友-我的二维码
    """

    class Meta:
        model = User
        fields = ('id','pay_code')