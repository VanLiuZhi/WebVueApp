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
    path('analysis', csrf_exempt(DataAnalysisView.as_view()))
]
