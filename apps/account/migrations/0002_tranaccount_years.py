# Generated by Django 2.1.1 on 2019-08-05 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tranaccount',
            name='years',
            field=models.CharField(blank=True, help_text='年份', max_length=64, null=True, verbose_name='年份'),
        ),
    ]
