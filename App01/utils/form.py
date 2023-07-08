from App01.utils.bootscrap import BootScrapModelForm
from django import forms
from App01.models import UserInfo, PrettyNumber, Admin
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from App01.utils.encrypt import md5


class UserModelForm(BootScrapModelForm):
    password = forms.CharField(min_length=4, label='密码')

    class Meta:
        model = UserInfo
        fields = ['name', 'password', 'age', 'gender', 'account', 'create_time', 'depart']


class NumberModelForm(BootScrapModelForm):
    # 验证输入格式算法正确 1
    phone_number = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^159[0-9]{8}$', '电话号码必须以159开头，并且只能为11位')],
    )

    class Meta:
        model = PrettyNumber
        # 表示所有字段
        # fields = '__all__'
        # 排除某些字段  exclude = ['level']
        fields = ['phone_number', 'price', 'level', 'status']

    def clean_phone_number(self):
        number = self.cleaned_data['phone_number']
        if len(number) != 11:
            # 验证不通过
            raise ValidationError("电话号码必须是11位")
        if PrettyNumber.objects.filter(phone_number=number).exists():
            raise ValidationError("电话号码已存在")
        # 验证通过，返回用户输入的值
        return number


class NumberEditModelForm(BootScrapModelForm):
    # 手机号不能修改
    # phone_number = forms.CharField(disabled=True, label='手机号')
    phone_number = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^159[0-9]{8}$', '电话号码必须以159开头，并且只能为11位')],
    )

    class Meta:
        model = PrettyNumber
        fields = ['phone_number', 'price', 'level', 'status']

    def clean_phone_number(self):
        number = self.cleaned_data['phone_number']
        if len(number) != 11:
            raise ValidationError("手机号只能为11位")
        if PrettyNumber.objects.exclude(id=self.instance.pk).filter(phone_number=number).exists():
            raise ValidationError('手机号已存在')

        return number


class AdminModelForm(BootScrapModelForm):
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    class Meta:
        model = Admin
        fields = ['username', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True)
        }

    # 对密码进行加密
    def clean_password(self):
        password = self.cleaned_data.get('password')
        # 对密码进行加密
        password = md5(password)
        return password

    # 校验两次密码是否一致
    def clean_confirm_password(self):
        print(self.cleaned_data)
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != md5(confirm_password):
            raise ValidationError('两次密码不一致')

        # 通过校验的字段值
        return confirm_password


class AdminEditModelForm(BootScrapModelForm):
    class Meta:
        model = Admin
        fields = ['username']


class AdminResetModelForm(BootScrapModelForm):
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    class Meta:
        model = Admin
        fields = ['password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True)
        }

    # 对密码进行加密
    def clean_password(self):
        password = self.cleaned_data.get('password')
        # 对密码进行加密
        password = md5(password)

        if not Admin.objects.filter(id=self.instance.pk, password=password).filter():
            raise ValidationError("不能和之前的密码一样")
        return password

    # 校验两次密码是否一致
    def clean_confirm_password(self):
        print(self.cleaned_data)
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != md5(confirm_password):
            raise ValidationError('两次密码不一致')

        # 通过校验的字段值
        return confirm_password
