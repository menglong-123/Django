from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from App01.utils.bootscrap import BootScrapModelForm
from App01.models import Task
from App01.utils.pagination import Pagination

class TaskModelForm(BootScrapModelForm):
    class Meta:
        model = Task
        fields = '__all__'



def task_list(request):
    query_set = Task.objects.all().order_by('level')
    form = TaskModelForm()
    obj = Pagination(request, query_set)
    context = {
        'form': form,
        'query_set': obj.query_set,
        'page_string': obj.html(),
    }

    return render(request, 'task_list.html',context)


@csrf_exempt
def test_ajax(request):
    dict = {"status":True, "data":[1,2,3,4]}

    return JsonResponse(dict)


@csrf_exempt
def task_add(request):
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        dict = {"status": True}
    else:
        dict = {"status": False, 'errors': form.errors}

    return JsonResponse(dict)

def task_delete(request, nid):
    Task.objects.filter(id=nid).delete()
    return redirect('/task/list/')