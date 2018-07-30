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
from vadmin.models import ArticleMenu, Article
from vadmin.api import ApiHandleView
import re

class ArticleView(ApiHandleView):
    """
    文章接口类
    """
    def getArticleForGUID(self, request, models_name):
        """
        通过GUID获取文章详情
        :return:
        """
        data = request_body_to_dict(request)
        guid = data.get('GUID')
        article = Article.objects.get(guid=guid)
        data = article.return_dict
        return self.xml_response_for_json(self.success_response(data=data, msg='获取成功'))


urlpatterns = [
    path('<api_name>', csrf_exempt(ArticleView.as_view())),
]