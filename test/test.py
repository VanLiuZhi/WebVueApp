#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/10 18:58
# @Author  : liuzhi
# @File    : test.py

import random, datetime
from stats.models import MoneyStats


def creat_test_data():
    for i in range(1, 10):
        # now = datetime.datetime.now()
        ms = MoneyStats(title=i, money=round(random.random(), 2))
        ms.save()


if __name__ == '__main__':
    creat_test_data()
