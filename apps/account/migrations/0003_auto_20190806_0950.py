# Generated by Django 2.1.1 on 2019-08-06 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_tranaccount_years'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tranaccount',
            name='years',
            field=models.CharField(blank=True, help_text='年月份', max_length=64, null=True, verbose_name='年月份'),
        ),
    ]
