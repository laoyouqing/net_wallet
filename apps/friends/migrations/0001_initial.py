# Generated by Django 2.1.1 on 2019-08-05 00:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendApply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(help_text='用户名', max_length=30, verbose_name='用户名')),
                ('photo', models.CharField(help_text='头像', max_length=1000, verbose_name='头像')),
                ('wallet_url', models.CharField(blank=True, help_text='钱包地址', max_length=300, null=True, verbose_name='钱包地址')),
                ('email', models.EmailField(blank=True, help_text='邮箱', max_length=254, null=True, verbose_name='邮箱')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('user', models.ForeignKey(blank=True, help_text='用户', null=True, on_delete=django.db.models.deletion.CASCADE, to='users.User', verbose_name='用户')),
            ],
            options={
                'verbose_name': '好友申请表',
                'verbose_name_plural': '好友申请表',
                'db_table': 'friend_apply',
            },
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(help_text='商家用户名', max_length=30, verbose_name='商家用户名')),
                ('photo', models.CharField(help_text='头像', max_length=1000, verbose_name='头像')),
                ('wallet_url', models.CharField(blank=True, help_text='钱包地址', max_length=300, null=True, verbose_name='钱包地址')),
            ],
            options={
                'verbose_name': '商家表',
                'verbose_name_plural': '商家表',
                'db_table': 'merchant',
            },
        ),
        migrations.CreateModel(
            name='my_friends',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(choices=[(0, '未接受'), (1, '已接受'), (2, '已拒绝')], default=0, help_text='好友申请状态', verbose_name='好友申请状态')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('friends', models.ForeignKey(help_text='好友', on_delete=django.db.models.deletion.CASCADE, to='friends.FriendApply', verbose_name='好友')),
                ('user', models.ForeignKey(help_text='用户', on_delete=django.db.models.deletion.CASCADE, to='users.User', verbose_name='用户')),
            ],
            options={
                'verbose_name': '我的好友表',
                'verbose_name_plural': '我的好友表',
                'db_table': 'my_friends',
            },
        ),
    ]
