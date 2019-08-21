from django.db import models

# Create your models here.
from friends.models import FriendApply, Merchant
from users.models import User


class TranAccount(models.Model):
    trans_status = (
        (0, '收款'),
        (1, '付款'),
        (2, '转账'),
    )
    order_id = models.CharField(max_length=64, verbose_name="订单号", help_text='订单号',null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户", help_text='用户')
    friends = models.ForeignKey(FriendApply, on_delete=models.CASCADE, verbose_name="好友", help_text='好友',null=True,blank=True)
    merchant = models.ForeignKey(Merchant,on_delete=models.CASCADE,verbose_name="商家", help_text='商家',null=True,blank=True)
    wbc_balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='网博币金额', help_text='网博币金额')
    pay_info=models.CharField(max_length=100,verbose_name='付款说明',help_text='付款说明',null=True,blank=True)
    status = models.SmallIntegerField(default=0, choices=trans_status, verbose_name='付款方式', help_text='付款方式')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    years=models.CharField(max_length=64,verbose_name='年月份',help_text='年月份',null=True,blank=True)



    class Meta:
        db_table = 'tran_account'
        verbose_name = '转账表'
        verbose_name_plural = verbose_name




