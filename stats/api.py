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


urlpatterns = [
    path('money', csrf_exempt(IndexView.as_view()))
]
