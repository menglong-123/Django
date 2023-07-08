# Generated by Django 3.2.5 on 2022-12-27 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App01', '0007_auto_20221225_1406'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boss',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='姓名')),
                ('age', models.IntegerField(verbose_name='年龄')),
                ('img', models.CharField(max_length=128, verbose_name='头像')),
            ],
        ),
    ]
