from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password

from users.models import User, UserPay


class UserWalletSerializer(serializers.ModelSerializer):
    """
    用户钱包
    """

    class Meta:
        model = User
        fields = ('id', 'wbc_balance','fri_code','pay_code')


class SetPasswordSerializer(serializers.ModelSerializer):
    """
    支付密码
    """
    password = serializers.CharField(label='密码', write_only=True)
    password2 = serializers.CharField(label='确认密码', write_only=True)
    # user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),label='用户id',source='user')


    class Meta:
        model = UserPay
        fields = ('id','password','password2')

    def validate(self, data):
        # 判断两次密码
        if data['password'] != data['password2']:
            raise serializers.ValidationError('两次密码不一致')
        return data




class UpdatePasswordSerializer(serializers.ModelSerializer):
    """
    修改密码
    """
    oldpassword = serializers.CharField(label='密码', write_only=True)
    password = serializers.CharField(label='密码', write_only=True)
    password2 = serializers.CharField(label='确认密码', write_only=True)

    class Meta:
        model = UserPay
        fields = ('id','oldpassword','password', 'password2')

    def validate(self, data):
        # 判断两次密码
        if data['password'] != data['password2']:
            raise serializers.ValidationError('两次密码不一致')
        return data







