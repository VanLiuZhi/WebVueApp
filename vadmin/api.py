#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/2 22:46
# @Author  : liuzhi
# @File    : api.py

from django.shortcuts import render, HttpResponse
from base.views import BaseView
from django.views.generic.base import View
from django.urls import path
from base.util import request_body_to_dict, dict_to_object, object_to_dict, get_uuid
from django.views.decorators.csrf import csrf_exempt
from vadmin.models import ArticleClassify, Article
from stats.models import MoneyStats
import re


def return_models(models_name):
    """
    返回model类
    :param models_name:
    :return:
    """
    _dict = {
        'ArticleClassify': ArticleClassify,
        'Article': Article,
        'MoneyStats': MoneyStats
    }
    return _dict.get(models_name)


class ApiHandleView(BaseView):
    """
    通用接口处理视图类
    api说明：list, add, edit, delete + 模型名字
    # ToDo 方法allowed处理
    """
    base_method_str = ['list', 'create', 'edit', 'delete']

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() not in ['post', 'get']:
            return self.xml_response_for_json(self.error_response(msg='Method Not Allowed'))
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request, api_name):
        return self.post(request, api_name)

    def post(self, request, api_name):
        print(api_name)
        r = re.compile('[a-z]+')
        re_match = r.match(api_name)
        action = re_match and re_match[0] or None
        models_name = api_name[len(action):]
        api_object = self.get_api_method(api_name, action)
        if not api_object:
            return self.xml_response_for_json(self.error_response(msg='Method Not Found'))
        res = api_object(request, models_name)
        return res

    def get_api_method(self, api_name, action):
        if action and action in self.base_method_str:
            method_dict = {
                'list': self.api_list_method,
                'create': self.api_create_method,
                'edit': self.api_edit_method,
                'delete': self.api_delete_method,
            }
            return method_dict.get(action)
        else:
            return getattr(self, api_name, None)

    def api_list_method(self, request, models_name):
        """
        获取模型列表数据(分页)
        :return:
        """
        params = request_body_to_dict(request)
        model = return_models(models_name)
        print(params)
        # 分页准备
        page = params.get('page')
        limit = params.get('limit')
        start = (int(page) - 1) * int(limit)
        end = int(page) * int(limit)
        # end分页准备
        model_query = model.objects.filter()
        # 排序处理
        if params and 'orderby' in params:
            model_query = model_query.order_by(*[v.strip() for v in params['orderby'].split(',') if v.strip()])
        # end排序处理
        total = model_query.count()
        fields = model().return_fields
        fields = fields + ['id', 'created', 'updated', 'date']
        hander = lambda item: object_to_dict(fields, item)
        model_query_instance = model_query[start:end]
        res = [hander(item) for item in model_query_instance]
        data = {'item': res, 'total': total}
        return self.xml_response_for_json(self.success_response(data=data, msg='获取成功'))

    def api_create_method(self, request, models_name):
        """
        添加数据到模型
        :param request:
        :param models_name:
        :return:
        """
        data = request_body_to_dict(request)
        model = return_models(models_name)
        model_instance = model()
        model_instance = dict_to_object(data, model_instance)
        model_instance.guid = get_uuid()
        model_instance.save()
        return self.xml_response_for_json(self.success_response(msg='添加成功'))

    def api_edit_method(self, request, models_name):
        """
        编辑模型数据
        :param request:
        :param models_name:
        :return:
        """
        data = request_body_to_dict(request)
        update_object = data.get('object')  # 更新对象的标识，用来查询需要更新的记录
        update = data.get('update')  # 更新数据
        model = return_models(models_name)
        model_instance = model.objects.filter(**update_object).first()
        model_instance = dict_to_object(update, model_instance)
        model_instance.save()
        return self.xml_response_for_json(self.success_response(msg='修改成功'))

    def api_delete_method(self, request, models_name):
        """
        删除模型的数据
        :param request: 参数结构举例 {'data': {'guid': 123}}
        :param models_name:
        :return:
        """
        data = request_body_to_dict(request)
        model = return_models(models_name)
        model_instance = model.objects.filter(**data.get('data')).first()
        model_instance.delete()
        return self.xml_response_for_json(self.success_response(msg='删除成功'))


class MenuView(BaseView):

    def post(self, request, api_name):
        print(api_name)
        api_name = getattr(self, api_name)
        res = api_name(request)
        return res

    def createMenu(self, request):
        data = request_body_to_dict(request)
        article_menu = ArticleMenu()
        article_menu = dict_to_object(data, article_menu)
        article_menu.uuid = get_uuid()
        article_menu.save()
        return self.xml_response_for_json(self.success_response(msg='添加成功'))

    def getMenuForLive(self, request):
        data = request_body_to_dict(request)
        article_menu = ArticleMenu.objects.filter(parent=data.get('uuid'))
        fields = ArticleMenu().return_fields
        hander = lambda item: object_to_dict(fields, item)
        res = [hander(item) for item in article_menu]
        return self.xml_response_for_json(self.success_response(data=res, msg='获取成功'))

    def getMenuTable(self, request):
        data = request_body_to_dict(request)
        print(data)
        article_menu = ArticleMenu.objects.filter()
        fields = ArticleMenu().return_fields
        fields = fields + ['id', 'created', 'updated']
        hander = lambda item: object_to_dict(fields, item)
        res = [hander(item) for item in article_menu]
        return self.xml_response_for_json(self.success_response(data=res, msg='获取成功'))


class ArticleView(BaseView):

    def post(self, request, api_name):
        print(api_name)
        api_name = getattr(self, api_name)
        res = api_name(request)
        return res

    def createMenu(self, request):
        data = request_body_to_dict(request)
        article_menu = ArticleMenu()
        article_menu = dict_to_object(data, article_menu)
        article_menu.uuid = get_uuid()
        article_menu.save()
        return self.xml_response_for_json(self.success_response(msg='添加成功'))

    def getMenuForLive(self, request):
        data = request_body_to_dict(request)
        article_menu = ArticleMenu.objects.filter(parent=data.get('uuid'))
        fields = ArticleMenu().return_fields
        hander = lambda item: object_to_dict(fields, item)
        res = [hander(item) for item in article_menu]
        return self.xml_response_for_json(self.success_response(data=res, msg='获取成功'))

    def getMenuTable(self, request):
        data = request_body_to_dict(request)
        print(data)
        article_menu = ArticleMenu.objects.filter()
        fields = ArticleMenu().return_fields
        fields = fields + ['id', 'created', 'updated']
        hander = lambda item: object_to_dict(fields, item)
        res = [hander(item) for item in article_menu]
        return self.xml_response_for_json(self.success_response(data=res, msg='获取成功'))


class IndexView(BaseView):
    # @csrf_exempt
    def post(self, request):
        # return self.render("index.html")
        from stats.models import MoneyStats
        data = self.request.POST
        import json
        data = json.loads(bytes.decode(request.body))
        ms = MoneyStats(title=data.get('title'), money=data.get('money'), date=data.get('date'))
        ms.save()
        print(request)
        print(self.request.POST.get('a'))
        return HttpResponse(json.dumps(data))

    def get(self, request):
        print(request)
        return self.render("index2.html")
        # return self.render("123")
        # return HttpResponse(json.dumps({'a': 123}))


class DataAnalysisView(BaseView):
    # @csrf_exempt
    def post(self, request):
        from stats.models import MoneyStats
        import json, decimal
        from django.db.models import Sum
        ms_query = MoneyStats.objects.filter().order_by('title').values('title').annotate(money=Sum('money'))
        # res = [{'date': item.date.strftime('%Y-%m-%d'), 'value': float(item.money), 'title': item.title} for item in ms_query]
        res = [{'cost': float(decimal.Decimal(item['money']).quantize(decimal.Decimal('0.00'))), 'type': item['title'],
                'a': 1} for item in ms_query]
        res.append({'cost': 300.21, 'type': '网购消费', 'a': 1})
        return HttpResponse(json.dumps(res))


def generate_data(query):
    import random, datetime
    start_time_str = '2018-05-01'
    start_time_obj = datetime.datetime.strptime(start_time_str, '%Y-%m-%d')
    title_dict = {1: '早餐', 2: '午餐', 3: '晚餐', 4: '上班地铁', 5: '下班地铁'}
    for index, i in enumerate(query):
        z = random.randint(1, 5)
        if index == 10 or index == 11:
            i.date = start_time_obj + datetime.timedelta(days=10)
        else:
            i.date = start_time_obj + datetime.timedelta(days=index)
        i.money = round(random.random() * 100, 2)
        i.title = title_dict.get(z)
        i.save()


urlpatterns = [
    path('money', csrf_exempt(IndexView.as_view())),
    path('analysis', csrf_exempt(DataAnalysisView.as_view())),
    path('<api_name>', csrf_exempt(ApiHandleView.as_view())),
    path('menu/<api_name>', csrf_exempt(MenuView.as_view())),
    path('article/<api_name>', csrf_exempt(ArticleView.as_view())),
]
