#!/usr/bin/env python
# Date 2018-03-20
# Author VanLiu

from django.shortcuts import render, HttpResponse
from base.views import BaseView
from django.urls import path
import json
from django.views.decorators.csrf import csrf_exempt


class IndexView(BaseView):
    # @csrf_exempt
    def post(self, request):
        # return self.render("index.html")
        print(request)
        print(self.request.POST.get('a'))
        return HttpResponse(json.dumps({'a': 123}))

    def get(self, request):
        print(request)
        return self.render("index2.html")
        # return self.render("123")
        # return HttpResponse(json.dumps({'a': 123}))


urlpatterns = [
    path('a/', csrf_exempt(IndexView.as_view()))
]
