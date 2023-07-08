from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 如果processes_request没有返回值（返回None），则可以继续往后走
        # 如果有返回值 返回HttpResponse, render, redirect

        # 排除不需要中间件校验登录的页面
        if request.path_info in ['/login/', '/image/code/'] :
            return
        info = request.session.get('info')
        # 如果没有登录信息
        if not info:
            return redirect('/login/')

    def process_response(self, request, response):
        return response
