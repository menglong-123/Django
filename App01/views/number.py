from django.shortcuts import render, HttpResponse, redirect
from App01.models import UserInfo, Department, PrettyNumber
from App01.utils.pagination import Pagination
from App01.utils.form import UserModelForm, NumberModelForm, NumberEditModelForm

# Create your views here.

""" 靓号列表 """


def number_list(request):

    data_dict = {}
    value = request.GET.get('q', '')
    # 如果链接中有q，那么就筛选包含value的靓号
    if value:
        data_dict['phone_number__contains'] = value
    # 否则就查询所有数据
    number_list = PrettyNumber.objects.filter(**data_dict).order_by("-level")

    object = Pagination(request, number_list)

    content = {
        'value': value,
        'list': object.query_set,  # 当前页的number列表
        'page_string': object.html(),  # 生成分页的html
    }

    return render(request, 'number_list.html', content)


""" 靓号删除 """


def number_delete(request, nid):
    PrettyNumber.objects.filter(id=nid).delete()
    return redirect('/number/list/')


""" 靓号添加 """


def number_add(request):
    if request.method == 'GET':
        form = NumberModelForm()
        return render(request, 'number_add.html', {'form': form})
    else:
        form = NumberModelForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('/number/list/')
        else:
            return render(request, 'number_add.html', {'form': form})



""" 靓号编辑 """


def number_edit(request, nid):
    number = PrettyNumber.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = NumberEditModelForm(instance=number)
        return render(request, 'number_edit.html', {'form': form})
    else:
        form = NumberEditModelForm(data=request.POST, instance=number)
        if form.is_valid():
            form.save()
            return redirect('/number/list/')
        else:
            return render(request, 'number_edit.html', {'form': form})
