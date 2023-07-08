"""EmployeeSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from App01.views import depart, user, number, admin, account, task, order, chart, upload, city

urlpatterns = [
    path('', depart.depart_list),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    # -----部门管理----
    # 部门列表
    path('depart/list/', depart.depart_list),
    # 新建部门
    path('depart/add/', depart.depart_add),
    path('depart/multi/', depart.depart_multi),
    # 删除部门
    path('depart/delete/', depart.depart_delete),
    # 编辑部门
    path('depart/<int:nid>/edit/', depart.depart_edit),

    # ----用户管理----
    # 用户列表
    path('user/list/', user.user_list),
    # 添加用户
    path('user/add/', user.user_add),
    # ModelForm添加用户
    path('user/model/form/add/', user.user_model_form_add),

    # 删除用户
    path('user/<int:nid>/delete/', user.user_delete),
    # 编辑用户
    path('user/<int:nid>/edit/', user.user_edit),

    # ----靓号管理----
    # 靓号列表
    path('number/list/', number.number_list),
    # 删除靓号
    path('number/<int:nid>/delete/', number.number_delete),
    # 添加靓号
    path('number/add/', number.number_add),
    # 编辑靓号
    path('number/<int:nid>/edit/', number.number_edit),

    # ----管理员管理----
    # 管理员列表
    path('admin/list/', admin.admin_list),
    # 添加管理员
    path('admin/add/', admin.admin_add),
    # 删除管理员
    path('admin/<int:nid>/delete/', admin.admin_delete),
    # 管理员编辑
    path('admin/<int:nid>/edit/', admin.admin_edit),
    # 重置密码
    path('admin/<int:nid>/reset/', admin.admin_reset),

    # ----用户登录----
    path('login/', account.login),

    # ----用户注销----
    path('logout/', account.logout),

    # ----生成验证码----
    path('image/code/', account.image_code),

    # ----任务管理----
    path('task/list/', task.task_list),

    path('task/ajax/', task.test_ajax),

    path('task/add/', task.task_add),

    path('task/<int:nid>/delete/', task.task_delete),

    # ----订单管理----
    path('order/list/', order.order_list),
    path('order/add/', order.order_add),
    # path('order/<int:nid>/delete/', order.order_delete),
    path('order/delete/', order.order_delete),
    path('order/detail/', order.order_detail),

    path('order/edit/', order.order_edit),

    # ---- 数据统计 ----
    path('chart/list/', chart.chart_list),
    path('chart/bar/', chart.chart_bar),
    path('chart/pie/', chart.chart_pie),
    path('chart/line/', chart.chart_line),

    # ---- 文件上传 ----
    path('upload/list/', upload.upload_list),
    path('upload/form/', upload.upload_form),
    path('upload/model/form/', upload.upload_model_form),

    # ---- 城市----
    path('city/list/', city.city_list),
    path('city/add/', city.city_add),

































]
