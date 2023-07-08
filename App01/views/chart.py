from django.shortcuts import HttpResponse, render, redirect
from django.http import JsonResponse


def chart_list(request):
    return render(request, 'chart_list.html')


def chart_bar(request):
    """ 获取柱状图的数据 """
    series = [
        {
            'name': '去年销量',
            'type': 'bar',
            'data': [5, 20, 36, 10, 10, 20]
        },
        {
            'name': '今年销量',
            'type': 'bar',
            'data': [15, 18, 30, 15, 18, 16]
        }
    ]

    legend_data = ['去年销量', '今年销量']
    xAxis_data = ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']

    result = {
        "status": True,
        "series": series,
        "legend_data": legend_data,
        "xAxis_data": xAxis_data
    }
    return JsonResponse(result)


def chart_pie(requests):
    """ 获取饼状图数据 """
    series_data = [{'value': 1048, 'name': '开发部'},
                   {'value': 735, 'name': '运营部'},
                   {'value': 580, 'name': '算法部'},
                   {'value': 484, 'name': '测试部'},
                   {'value': 300, 'name': '企划部'}
                   ]
    result = {
        'status': True,
        'series_data': series_data
    }
    return JsonResponse(result)


def chart_line(request):
    """ 获取折线图数据 """
    legend_data = ['Email', 'Union Ads', 'Video Ads', 'Direct', 'Search Engine']
    xAxis_data = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    series = [
        {
            'name': 'Email',
            'type': 'line',
            'stack': 'Total',
            'data': [120, 132, 101, 134, 90, 230, 210]
        },
        {
            'name': 'Union Ads',
            'type': 'line',
            'stack': 'Total',
            'data': [220, 182, 191, 234, 290, 330, 310]
        },
        {
            'name': 'Video Ads',
            'type': 'line',
            'stack': 'Total',
            'data': [150, 232, 201, 154, 190, 330, 410]
        },
        {
            'name': 'Direct',
            'type': 'line',
            'stack': 'Total',
            'data': [320, 332, 301, 334, 390, 330, 320]
        },
        {
            'name': 'Search Engine',
            'type': 'line',
            'stack': 'Total',
            'data': [820, 932, 901, 934, 1290, 1330, 1320]
        }
    ]
    result = {
        'status': True,
        'legend': legend_data,
        'xAxis_data': xAxis_data,
        'series': series,
    }
    return JsonResponse(result)
