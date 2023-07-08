from django.shortcuts import render, HttpResponse, redirect
from App01.models import UserInfo, Department, PrettyNumber
from App01.utils.pagination import Pagination
from App01.utils.form import UserModelForm

# Create your views here.

""" 用户列表 """


def user_list(request):

    # 获取所有用户信息
    user_list = UserInfo.objects.all()

    object = Pagination(request, user_list)

    content = {
        'list': object.query_set,
        'page_string': object.html()
    }
    print(content)
    return render(request, 'user_list.html', content)


""" 添加用户 """


def user_add(request):
    if request.method == 'GET':

        content = {'gender_choices': UserInfo.gender_choices,
                   'depart': Department.objects.all()}

        return render(request, 'user_add.html', content)
    else:
        name = request.POST.get('name')
        password = request.POST.get('password')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        account = request.POST.get('account')
        create_time = request.POST.get('create_time')
        depart_id = request.POST.get('department')

        UserInfo.objects.create(name=name, password=password, age=age, gender=gender, account=account,
                                create_time=create_time, depart_id=depart_id)

        return redirect('/user/list/')


""" ModelForm 添加用户 """


def user_model_form_add(request):
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {'form': form})
    else:
        # 用户POST提交的数据，数据需要校验
        form = UserModelForm(data=request.POST)
        # 校验成功
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('/user/list/')
        else:
            # 校验失败
            return render(request, 'user_model_form_add.html', {'form': form})


""" 删除用户 """


def user_delete(request, nid):
    UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')


""" 编辑用户 """


def user_edit(request, nid):
    user = UserInfo.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = UserModelForm(instance=user)
        return render(request, 'user_edit.html', {'form': form})
    else:
        form = UserModelForm(data=request.POST, instance=user)
        if form.is_valid():
            # 默认保存用户输入的数据
            # 如果要保持另外的数据可以 form.instance.字段名 = 值
            form.save()
            return redirect('/user/list/')
        else:
            return render(request, 'user_edit.html', {'form': form})

