"""net_wallet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from account.views import PayView, GoPay, TranAccountView, AccountInfoView, LastSaleView, AccountView
from apps.users.views import UserWallet, SetPassword, UpdatePassword
from friends.views import FriendInfoView, MyFriendView, NewFriendView, MyCodeView, ReceiptCodeView
from net_wallet.settings import MEDIA_ROOT

router = DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    re_path('media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    path("api-docs/", include_docs_urls("API文档")),

    path('', include(router.urls)),

    path('wallet/', UserWallet.as_view()),  #钱包
    path('payinfo/', PayView.as_view()),    #收付款
    path('is_set_password/', GoPay.as_view()),   #是否设置支付密码
    path('set_password/', SetPassword.as_view({'post':'create'})),  #设置密码
    path('update_password/', UpdatePassword.as_view({'put':'update'})),   #修改密码
    path('friend_info/', FriendInfoView.as_view()),   #扫码获取好友信息
    path('friend_info/<int:pk>/', FriendInfoView.as_view()),   #更新好友状态
    path('my_friend/', MyFriendView.as_view({'get':'list'})),   #我的好友列表
    path('new_friend/', NewFriendView.as_view({'get':'list'})),   #新的朋友
    path('tran_account/', TranAccountView.as_view()),   #转账
    path('account_info/', AccountInfoView.as_view({'get':'list'})),   #转账信息
    path('account_info/<int:order_id>/', AccountInfoView.as_view({'get':'retrieve'})),   #账单详情
    path('last_sale/', LastSaleView.as_view({'get':'list'})),   #最近交易
    path('account/', AccountView.as_view()),  #账单
    path('my_code/', MyCodeView.as_view()),  #添加好友-我的二维码
    path('receipt_code/', ReceiptCodeView.as_view()),  #收款二维码
]
