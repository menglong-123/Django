from django.shortcuts import redirect, render, HttpResponse
from django import forms
from App01.models import Admin
from App01.utils.bootscrap import BootScrapForm
from App01.utils.encrypt import md5
from App01.utils.code import check_code
from io import BytesIO


# 用Form的方式
class LoginForm(BootScrapForm):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}, render_value=True),
                               required=True)

    code = forms.CharField(label='验证码',
                           widget=forms.TextInput(attrs={'class': 'form-control'}),
                           required=True)

    def clean_password(self):
        return md5(self.cleaned_data.get('password'))


# 用ModelForm的方式
# class LoginForm(forms.ModelForm):
#     class Meta:
#         model = Admin
#         fields = ['username', 'password']

def login(request):
    if request.method == 'GET':
        form = LoginForm()
        content = {
            'form': form
        }
        return render(request, 'login.html', content)
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            print(form.cleaned_data)

            # 验证码的校验
            user_input_code = form.cleaned_data.pop('code')
            image_code = request.session.get('image_code', '')
            if user_input_code.upper() != image_code.upper():
                form.add_error('code', '验证码错误')

            # 校验用户名和密码是否正确
            # obj = Admin.objects.filter(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password')).first()
            obj = Admin.objects.filter(**form.cleaned_data).first()
            # 用户名或密码错误
            if not obj:
                form.add_error('password', '用户名或密码错误')
                content = {'form': form}
                return render(request, 'login.html', content)
            # 用户名和密码正确
            else:
                # 网站生成随机字符串，写到用户浏览器的Cookie中，再写入Session中
                request.session['info'] = {'id': obj.id, 'username': obj.username}
                # 7天免登录
                request.session.set_expiry(60 * 60 * 24 * 7)
                return redirect('/admin/list/')

        else:
            content = {'form': form}
            return render(request, 'login.html', content)


def logout(request):
    request.session.clear()
    return redirect('/login/')


def image_code(request):
    image, code = check_code()
    print(code)

    # 写入到session中，以便后续获取验证码进行校验
    request.session['image_code'] = code
    # 给session设置60s超时
    request.session.set_expiry(60)

    stream = BytesIO()
    image.save(stream, 'png')
    return HttpResponse(stream.getvalue())
