from django.shortcuts import redirect, render, HttpResponse
from django.http import JsonResponse
from App01.models import Order
from App01.utils.bootscrap import BootScrapModelForm
from django.views.decorators.csrf import csrf_exempt
import random
from datetime import datetime
from App01.utils.pagination import Pagination


class OrderForm(BootScrapModelForm):
    class Meta:
        model = Order
        # fields = '__all__'
        # fields = ['title', 'price', 'status' ,'user']
        exclude = ['oid', 'user']


def order_list(request):
    query_set = Order.objects.all()
    form = OrderForm()
    obj = Pagination(request, query_set)
    content = {
        'query_set': obj.query_set,
        'form': form,
        'page_string': obj.html(),
    }
    return render(request, 'order_list.html', content)


@csrf_exempt
def order_add(request):
    form = OrderForm(data=request.POST)
    if form.is_valid():
        # 加入oid
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        # 加入管理员
        form.instance.user_id = request.session['info']['id']
        # 保存在数据库
        form.save()
        return JsonResponse({'status': True})
    else:
        return JsonResponse({'status': False, 'errors': form.errors})


# def order_delete(request, nid):
#     Order.objects.filter(id=nid).delete()
#     return redirect('/order/list/')

@csrf_exempt
def order_delete(request):
    nid = request.POST.get('nid')
    if not Order.objects.filter(id=nid).exists():
        return JsonResponse({'status': False, 'error': '数据不存在'})
    else:
        Order.objects.filter(id=nid).delete()
        return JsonResponse({'status': True})


@csrf_exempt
def order_detail(request):
    """ 弹出编辑框 """
    nid = request.POST.get('nid')
    if not Order.objects.filter(id=nid).exists():
        return JsonResponse({'status': False, 'error': '数据不存在'})
    else:
        order_dict = Order.objects.filter(id=nid).values('title', 'price', 'status').first()
        result = {
            'status': True,
            'data': order_dict,
        }
        return JsonResponse(result)


@csrf_exempt
def order_edit(request):
    """ 进行编辑 """
    nid = request.GET.get('uid')
    row_object = Order.objects.filter(id=nid).first()
    if not row_object:
        return JsonResponse({"status": False, 'msg': '数据不存在'})
    form = OrderForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    else:
        return JsonResponse({'status': False, 'error': form.errors})
