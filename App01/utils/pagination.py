"""
自定义分页组件
"""

import math
from django.utils.safestring import mark_safe


class Pagination(object):
    def __init__(self, request, query_set, page_param="page", page_size=10, plus=4):
        from django.http.request import QueryDict
        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        self.page_param = page_param

        self.page = request.GET.get(page_param, '1')
        if self.page.isdecimal():
            self.page = int(self.page)
        else:
            self.page = 1


        max_value = len(query_set)
        self.page_count = math.ceil(max_value / page_size)  # 总页数

        # 防止页数越界
        if self.page > self.page_count:
            self.page = self.page_count
        elif self.page < 1:
            self.page = 1

        self.min_page = max(1, self.page - plus)
        self.max_page = min(self.page + plus, self.page_count)

        if self.page < plus + 1:
            self.max_page = min(self.page_count, 2 * plus + 1)
        if self.page > self.max_page - plus:
            self.min_page = max(1, self.page_count - 2 * plus)

        if max_value == 0:
            self.query_set = []
        else:
            self.query_set = query_set[(self.page - 1) * page_size: min(self.page * page_size, max_value)]

        self.pre_page = max(1, self.page - 1)
        self.post_page = min(self.page_count, self.page + 1)

    def html(self):
        self.query_dict.setlist(self.page_param, [1])
        first = '<li><a href="?{}" aria-label="Previous"><span aria-hidden="true">首页</span></a></li>'.format(
            self.query_dict.urlencode())
        self.query_dict.setlist(self.page_param, [self.pre_page])
        pre = '<li><a href="?{}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(
            self.query_dict.urlencode())
        page_list = []
        page_list.append(first)
        page_list.append(pre)
        for i in range(self.min_page, self.max_page + 1):
            if i == self.page:
                self.query_dict.setlist(self.page_param, [i])
                eme = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                self.query_dict.setlist(self.page_param, [i])
                eme = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_list.append(eme)

        self.query_dict.setlist(self.page_param, [self.post_page])
        post = '<li><a href="?{}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'.format(
            self.query_dict.urlencode())
        self.query_dict.setlist(self.page_param, [self.page_count])
        end = '<li><a href="?{}" aria-label="Previous"><span aria-hidden="true">尾页</span></a></li>'.format(
            self.query_dict.urlencode())
        page_list.append(post)
        page_list.append(end)

        search = '''
        <li style="float: left"><form method="get"><div class="input-group" style="width: 150px"><input type="text" class="form-control" placeholder="页码" name="page">
        <span class="input-group-btn"><button class="btn btn-default" type="submit">跳转</button>
         </span></div></form></li>
         '''
        page_list.append(search)
        page_string = ''.join(page_list)
        page_string = mark_safe(page_string)

        return page_string
