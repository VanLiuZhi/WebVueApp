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

    def getArticleForGUID(self, request, models_name):
        """
        通过GUID获取文章详情
        :return:
        """
        params = request_body_to_dict(request)
        guid = params.get('GUID')
        article = Article.objects.get(guid=guid)
        data = article.return_dict
        if not params.get('from_to_admin'):
            content_handler = ContentHandler(data['content'])
            data['menu'], data['content'] = content_handler.generate_menu_str()
        return self.xml_response_for_json(self.success_response(data=data, msg='获取成功'))

    def getArticleClassifyList(self, request, models_name):
        """
        获取文章分类（通过关键字来搜索）
        :param request:
        :param models_name:
        :return:
        """
        data = request_body_to_dict(request)
        name = data.get('name', '')
        fields = ArticleClassify().return_fields
        hander = lambda item: object_to_dict(fields, item)
        query = ArticleClassify.objects.filter(name__contains=name)
        res = [hander(item) for item in query]
        data = {'items': res}
        return self.xml_response_for_json(self.success_response(data=data, msg='获取成功'))

    def saveArticle(self, request, models_name):
        """
        保存文章
        :param request:
        :param models_name:
        :return:
        """
        data = request_body_to_dict(request)


urlpatterns = [
    path('<api_name>', csrf_exempt(ArticleView.as_view())),
]
