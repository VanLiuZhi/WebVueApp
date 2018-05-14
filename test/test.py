#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/10 18:58
# @Author  : liuzhi
# @File    : test.py
#
# import asyncio
#
#
# @asyncio.coroutine
# def hello():
#     r = yield from asyncio.sleep(1)
#     print('hello world')
#
#
# # 获取EventLoop:
# loop = asyncio.get_event_loop()
# # 执行coroutine
# loop.run_until_complete(hello())
# loop.close()

a = [['a',2]]
b = [['a',1],['c',1]]

# print(set(a))

c = set(a) & set(b)
#
# print(c)