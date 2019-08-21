from django.db import models

# Create your models here.

class User(models.Model):
    username=models.CharField(max_length=30,verbose_name='用户名',help_text='用户名')
    photo = models.CharField(max_length=1000, verbose_name='头像', help_text='头像')
    email=models.EmailField(verbose_name='邮箱',help_text='邮箱',null=True,blank=True)
    telphone=models.EmailField(verbose_name='手机号',help_text='手机号',null=True,blank=True)
    # wallet_url = models.CharField(max_length=300, verbose_name='钱包地址', help_text='钱包地址',null=True,blank=True)
    fri_code = models.CharField(max_length=300, verbose_name='我的二维码地址（加好友）', help_text='我的二维码地址（加好友）',null=True,blank=True)
    pay_code = models.CharField(max_length=300, verbose_name='收款二维码地址', help_text='收款二维码地址',null=True,blank=True)
    wbc_balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='网博币余额', help_text='网博币余额',null=True,blank=True)


    class Meta:
        db_table = 'user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class UserPay(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户",help_text='用户')
    password=models.CharField(max_length=300,verbose_name='支付密码',help_text='支付密码',null=True,blank=True)

    class Meta:
        db_table = 'user_pay'
        verbose_name = '用户支付密码表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username





class UserToken(models.Model):

    token=models.CharField(max_length=100,verbose_name='token',help_text='token')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户", help_text='用户')

    class Meta:
        db_table = 'user_token'
        verbose_name = '用户token表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username