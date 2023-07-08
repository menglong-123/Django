from django.shortcuts import render, HttpResponse, redirect
from App01.models import Admin
from App01.utils.pagination import Pagination
from App01.utils.form import AdminModelForm, AdminEditModelForm, AdminResetModelForm


def admin_list(request):
    # 检查用户是否已经登录，已登录可以查看，未登录跳转到登录页面
    # 用户发来请求，获取Cookie的随机字符串，拿着随机字符串看看Session中有没有
    # 若info为None，说明用户没有登录
    # 中间件实现了登录校验
    # info = request.session.get('info')
    # if not info:
    #     return redirect('/login/')

    # 搜索
    data_dict = {}
    value = request.GET.get('q', '')
    # 如果链接中有q，那么就筛选包含value的靓号
    if value:
        data_dict['username__contains'] = value
    # 否则就查询所有数据
    query_set = Admin.objects.filter(**data_dict)

    # 分页
    object = Pagination(request, query_set)
    content = {
        'list': object.query_set,
        'page_string': object.html(),
        'value': value
    }
    return render(request, 'admin_list.html', content)


def admin_add(request):
    if request.method == 'GET':
        form = AdminModelForm()
        content = {
            'form': form,
            'title': '添加管理员'
        }
        return render(request, 'admin_add_and_edit.html', content)
    else:
        form = AdminModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin/list/')
        else:
            content = {
                'form': form,
                'title': '添加管理员'
            }
            return render(request, 'admin_add_and_edit.html', content)


def admin_delete(request, nid):
    Admin.objects.filter(id=nid).first().delete()

    return redirect('/admin/list/')


def admin_edit(request, nid):
    obj = Admin.objects.filter(id=nid).first()
    if not obj:
        return redirect('/admin/list/')
    else:
        title = '添加管理员'
        if request.method == 'GET':
            form = AdminEditModelForm(instance=obj)
            content = {
                'form': form,
                'title': title
            }
            return render(request, 'admin_add_and_edit.html', content)
        else:
            form = AdminEditModelForm(data=request.POST, instance=obj)
            if form.is_valid():
                form.save()
                return redirect('/admin/list/')
            else:
                content = {
                    'form': form,
                    'title': title
                }
                return render(request, 'admin_add_and_edit.html', content)


def admin_reset(request, nid):
    obj = Admin.objects.filter(id=nid).first()
    if not obj:
        return redirect('/admin/list/')
    else:
        title = '重置密码--{}'.format(obj.username)
        if request.method == 'GET':
            form = AdminResetModelForm()
            content = {
                'form': form,
                'title': title
            }
            return render(request, 'admin_add_and_edit.html', content)
        else:
            form = AdminResetModelForm(data=request.POST, instance=obj)
            if form.is_valid():
                form.save()
                return redirect('/admin/list/')
            else:
                content = {
                    'form': form,
                    'title': title
                }
                return render(request, 'admin_add_and_edit.html', content)