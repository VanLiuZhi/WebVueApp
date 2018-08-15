#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/24 14:09
# @Author  : liuzhi
# @File    : article_api.py

from django.shortcuts import render, HttpResponse
from base.views import BaseView
from django.views.generic.base import View
from django.urls import path
from base.util import request_body_to_dict, dict_to_object, object_to_dict, get_uuid
from django.views.decorators.csrf import csrf_exempt
from vadmin.models import ArticleClassify, Article
from vadmin.api import ApiHandleView
import re
from vadmin.rich_text_utils import ContentHandler


class ArticleView(ApiHandleView):
    """
    文章接口类
    """

    def getArticleForGUID(self, request, *args):
        """
        通过GUID获取文章详情
        :return:
        """
        params = request_body_to_dict(request)
        guid = params.get('GUID')
        article = Article.objects.get(guid=guid)
        article.update_times()  # 更新浏览次数
        data = {}
        if params.get('from_to_admin'):
            data = article.get_dict()
        if not params.get('from_to_admin'):
            data = article.get_dict(not_add_fields=False)
            content_handler = ContentHandler(data['content'])
            data['menu'], data['content'] = content_handler.generate_menu_str()
        data['article_menu_label'] = article.return_article_classify_name
        return self.xml_response_for_json(self.success_response(data=data, msg='获取成功'))

    def getArticleClassifyList(self, request, *args):
        """
        获取文章分类（通过关键字来搜索）
        :param request:
        :param models_name:
        :return:
        """
        data = request_body_to_dict(request)
        name = data.get('name', '')
        fields = ArticleClassify().get_fields()
        hander = lambda item: object_to_dict(fields, item)
        query = ArticleClassify.objects.filter(name__contains=name)
        res = [hander(item) for item in query]
        data = {'items': res, 'count': query.count()}
        return self.xml_response_for_json(self.success_response(data=data, msg='获取成功'))

    def getTopLevelArticleClassify(self, request, *args):
        """
        获取文章分类的顶级分类（level为1的）
        :param request:
        :param args:
        :return:
        """
        query = ArticleClassify.objects.filter(level=1)
        fields = ['name', 'guid', 'return_all_children_count', 'isLeaf']
        hander = lambda item: object_to_dict(fields, item)
        res = [hander(item) for item in query]
        data = {'items': res}
        return self.xml_response_for_json(self.success_response(data=data, msg='获取成功'))

    def getArticleClassifyForGUID(self, request, *args):
        """
        通过GUID获取当前分类下的子分类（不返回子分类的子分类）
        :param request:
        :param args:
        :return:
        """
        params = request_body_to_dict(request)
        parent = params.get('parent')
        query = ArticleClassify.objects.filter(parent=parent)
        fields = ['name', 'guid', 'return_parents', 'return_all_children_count', 'isLeaf']
        hander = lambda item: object_to_dict(fields, item)
        res = [hander(item) for item in query]
        data = {'items': res}
        return self.xml_response_for_json(self.success_response(data=data, msg='获取成功'))

    def getCommonClassifyTag(self, *args):
        """
        获取常用标签（随机返回10个）
        :return:
        """
        # ArticleClassify.Meta.ordering = ['?']
        query = ArticleClassify.objects.filter()[:10]
        fields = ['name', 'guid']
        hander = lambda item: object_to_dict(fields, item)
        res = [hander(item) for item in query]
        data = {'items': res}
        return self.xml_response_for_json(self.success_response(data=data, msg='获取成功'))


urlpatterns = [
    path('<api_name>', csrf_exempt(ArticleView.as_view())),
]