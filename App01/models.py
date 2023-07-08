from django.db import models


# Create your models here.

class Department(models.Model):
    """ 部门表 """

    title = models.CharField(verbose_name='部门名称', max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """ 员工表 """

    name = models.CharField(verbose_name='名字', max_length=16)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')

    # 在Django中做的约束
    gender_choices = (
        (0, '女'),
        (1, '男')
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)

    # 数值最多10位，小数最多2位
    account = models.DecimalField(verbose_name='账户余额', max_digits=10, decimal_places=2, default=0)
    # 年月日时分秒
    # create_time = models.DateTimeField(verbose_name='入职时间')
    # 年月日
    create_time = models.DateField(verbose_name='入职时间')
    # 无约束
    # depart_id = models.BigIntegerField(verbose_name='部门ID')

    # 有约束 to表示与哪个表关联  to_field表示与哪个列关联
    # Django生成数据库表的时候会自动 在列名后加_id
    # on_delete=models.CASCADE 级联删除，如果部门被删除，与此关联的用户信息也删除
    # null=True blank=True, on_delete=models.SET_NULL 若部门被删除，则当前部门置空
    depart = models.ForeignKey(verbose_name='部门', to='Department', to_field='id', on_delete=models.CASCADE)


class PrettyNumber(models.Model):
    """ 靓号表 """
    phone_number = models.CharField(verbose_name='手机号', max_length=11)
    # 想要允许为空  null=True, blank=True
    price = models.IntegerField(verbose_name='价格')

    level_choices = (
        (1, '1级'),
        (2, '2级'),
        (3, '3级'),
        (4, '4级'),
    )
    level = models.SmallIntegerField(verbose_name='级别', choices=level_choices, default=1)

    status_choices = (
        (0, '已占用'),
        (1, '未占用')
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices, default=1)


""" 管理员"""


class Admin(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)

    def __str__(self):
        return self.username


# 任务
class Task(models.Model):
    title = models.CharField(verbose_name='任务', max_length=64)
    detail = models.CharField(verbose_name='详细信息', max_length=64)

    level_choice = (
        (1, '紧急'),
        (2, '重要'),
        (3, '临时'),
    )

    level = models.SmallIntegerField(verbose_name='级别', choices=level_choice, default=1)
    user = models.ForeignKey(verbose_name='负责人', to='Admin', on_delete=models.CASCADE)


# 订单

class Order(models.Model):
    oid = models.CharField(verbose_name='订单号', max_length=20, null=False, blank=False)
    title = models.CharField(verbose_name='商品名称', max_length=64)
    price = models.IntegerField(verbose_name='价格')
    status_choice = (
        (1, '未支付'),
        (2, '已支付'),
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choice,default=1)
    user = models.ForeignKey(verbose_name='用户ID', to='Admin', on_delete=models.CASCADE)

class Boss(models.Model):
    name = models.CharField(verbose_name='姓名', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    img = models.CharField(verbose_name='头像', max_length=128)


class City(models.Model):
    name = models.CharField(verbose_name='名称', max_length=64)
    count = models.IntegerField(verbose_name='人口')
    # 本质上数据库中也是CharField， 自动保存文件数据
    img = models.FileField(verbose_name='LOGO', max_length=128, upload_to='city')