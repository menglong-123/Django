from django.shortcuts import HttpResponse, render, redirect
from App01 import models
from App01.utils.bootscrap import BootScrapModelForm


def city_list(request):
    query_set = models.City.objects.all()

    return render(request, 'city_list.html', {'query_set': query_set})


class cityModelForm(BootScrapModelForm):
    bootstrap_exclude_fields = ['img']

    class Meta:
        model = models.City
        fields = '__all__'


def city_add(request):
    title = '添加城市'
    if request.method == 'GET':
        form = cityModelForm()
        return render(request, 'upload_model_form.html', {'title': title, 'form': form})
    else:
        form = cityModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            # 对于文件：自动保存  upload_to='city'   数据库中文件路径为  city/filename
            # 字段 + 上传路径写入到数据库
            form.save()
            return redirect('/city/list/')
        else:
            return render(request, 'upload_model_form.html', {'title': title, 'form': form})
