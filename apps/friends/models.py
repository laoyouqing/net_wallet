from django.db import models

# Create your models here.
from users.models import User


class FriendApply(models.Model):

    username = models.CharField(max_length=30, verbose_name='用户名', help_text='用户名')
    photo = models.CharField(max_length=1000, verbose_name='头像', help_text='头像')
    telphone=models.EmailField(verbose_name='手机号',help_text='手机号',null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户",help_text='用户',null=True,blank=True)
    wallet_url = models.CharField(max_length=300, verbose_name='钱包地址', help_text='钱包地址',null=True,blank=True)
    email=models.EmailField(verbose_name='邮箱',help_text='邮箱',null=True,blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    fri_code = models.CharField(max_length=300, verbose_name='我的二维码地址（加好友）', help_text='我的二维码地址（加好友）', null=True,
                                blank=True)
    pay_code = models.CharField(max_length=300, verbose_name='收款二维码地址', help_text='收款二维码地址', null=True, blank=True)

    class Meta:
        db_table = 'friend_apply'
        verbose_name = '好友申请表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class my_friends(models.Model):
    apply_status = (
        (0, '未接受'),
        (1, '已接受'),
        (2, '已拒绝'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="用户",help_text='用户')
    friends = models.ForeignKey(FriendApply,on_delete=models.CASCADE,verbose_name="好友",help_text='好友')
    status = models.SmallIntegerField(default=0, choices=apply_status, verbose_name='好友申请状态', help_text='好友申请状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'my_friends'
        verbose_name = '我的好友表'
        verbose_name_plural = verbose_name



class Merchant(models.Model):
    username = models.CharField(max_length=30, verbose_name='商家用户名', help_text='商家用户名')
    photo = models.CharField(max_length=1000, verbose_name='头像', help_text='头像')
    wallet_url = models.CharField(max_length=300, verbose_name='钱包地址', help_text='钱包地址',null=True,blank=True)

    class Meta:
        db_table = 'merchant'
        verbose_name = '商家表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username





