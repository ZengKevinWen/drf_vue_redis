# Generated by Django 2.2.5 on 2022-01-08 07:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20220108_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='luckdraw',
            name='create_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='穿件时间'),
        ),
        migrations.AlterField(
            model_name='luckdraw',
            name='update_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
