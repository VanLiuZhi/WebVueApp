#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/21 13:55
# @Author  : liuzhi
# @File    : api.py

from django.shortcuts import render, HttpResponse
from base.views import BaseView, SessionMinx
from django.views.generic.base import View
from django.urls import path
from base.util import request_body_to_dict, dict_to_object, object_to_dict, get_uuid
from django.views.decorators.csrf import csrf_exempt
from vadmin.models import ArticleClassify, Article
from vadmin.api import ApiHandleView
from user.models import User
from django.conf import settings
import re
from vadmin.rich_text_utils import ContentHandler


class LoginApiView(ApiHandleView, SessionMinx):
    """
    登陆鉴权相关Api
    """

    def Login(self, request, *args):
        """
        登陆接口
        :param args:
        :return:
        """
        params = request_body_to_dict(request)
        username = params.get('username', '')
        password = params.get('password', '')
        user = User.objects.filter(username=username).first()
        if not user or not user.check_password(password):
            return self.xml_response_for_json(self.error_response(msg='用户名或密码错误'))
        self.request.session['me'] = username
        print(self.request.COOKIES)
        # data = {'token': self.request.COOKIES.get(settings.SESSION_COOKIE_NAME)}
        data = {'token': self.request.COOKIES}
        # data = {}
        return self.xml_response_for_json(self.success_response(data=data, msg='登陆成功'))

    def getUserInfo(self, request, *args):
        """
        获取用户信息
        :param request:
        :param args:
        :return:
        """
        # params = request_body_to_dict(request)
        data = self.session_get('me')
        data = {'roles': data, 'name': 'admin'}
        return self.xml_response_for_json(self.success_response(data=data))


    def Register(self, *args):
        """
        仅测试使用
        :param args:
        :return:
        """
        a = User(username='admin')
        password = User.make_password_for_hash('123456')
        print(password)
        a.password = password
        a.save()

    def checkPassword(self, *args):
        """
        验证加密密码
        :param args:
        :return:
        """
        user = User.objects.get(id=1)
        password = User.make_password_for_hash('123456')
        print(password)
        print(user.password)
        res = user.check_password('123456')
        print(res)
        return self.xml_response_for_json('')


urlpatterns = [
    path('<api_name>', csrf_exempt(LoginApiView.as_view())),
]
