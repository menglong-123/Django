from django.shortcuts import redirect, render, HttpResponse
from django import forms
from App01.utils.bootscrap import BootScrapForm, BootScrapModelForm
import os
import random
from App01 import models
from django.conf import settings


def upload_list(request):
    if request.method == 'GET':
        return render(request, 'upload_list.html')
    else:
        print(request.POST)
        print(request.FILES)
        file_object = request.FILES.get('avatar')
        f = open(file_object.name, mode='wb')
        for chunk in file_object.chunks():
            f.write(chunk)
        f.close()
        return HttpResponse("上传成功")


class UploadForm(BootScrapForm):
    bootstrap_exclude_fields = ['img']
    name = forms.CharField(label='姓名')
    age = forms.IntegerField(label='年龄')
    img = forms.FileField(label='头像')


def upload_form(request):
    title = 'Form上传'
    if request.method == "GET":
        form = UploadForm()
        return render(request, 'upload_form.html', {'form': form, 'title': title})
    else:
        form = UploadForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            # print(form.cleaned_data)
            # 读取到数据，自己去处理
            image_object = form.cleaned_data.get('img')
            image_class = image_object.name.split('.')[-1]
            # print(image_class)

            file_name = str(random.randint(0, 999999)) + '.' + image_class
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            while os.path.exists(file_path):
                file_name = str(random.randint(0, 999999)) + '.' + image_class
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)

            f = open(file_path, mode='wb')
            for chunk in image_object.chunks():
                f.write(chunk)
            f.close()

            models.Boss.objects.create(
                name=form.cleaned_data['name'],
                age=form.cleaned_data['age'],
                img='media/' + file_name,
            )
            return HttpResponse("上传成功")
        else:
            return render(request, 'upload_form.html', {'form': form, 'title': title})


class uploadModelForm(BootScrapModelForm):
    bootstrap_exclude_fields = ['img']
    class Meta:
        model = models.City
        fields = '__all__'


def upload_model_form(request):
    title = 'ModelForm上传'
    if request.method == 'GET':
        form = uploadModelForm()
        return render(request, 'upload_model_form.html', {'title': title, 'form': form})
    else:
        form = uploadModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            # 对于文件：自动保存  upload_to='city'   数据库中文件路径为  city/filename
            # 字段 + 上传路径写入到数据库
            form.save()
            return HttpResponse("成功")
        else:
            return render(request, 'upload_model_form.html', {'title': title, 'form': form})
