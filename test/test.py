#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/10 18:58
# @Author  : liuzhi
# @File    : test.py

from jinja2 import Template
import re

base_template = """<ul>
            {% for item in data %}
            <li><a href="#{{ item.name }}">{{ item.name }}</a>
                {% if item.children %}
                <ul>
                    {% for i in item.children %}
                    <li><a href="#{{ i.name }}">{{ i.name }}</a></li>
                    {% endfor %}
                </ul>
                {% endif %}
            </li>
            {% endfor %}
        </ul>"""


class ContentHandler:
    Chinese_re = "[\u4E00-\u9FA5]+"
    h2 = '<h2.+</h2>'
    h3 = '<h2.+</h2>|<h3.+</h3>'

    def __init__(self, html_str):
        self.html_str = html_str
        self.raw_html_str = html_str

    def get_chinese(self, _str):
        res = re.findall(self.Chinese_re, _str)[0]
        return res

    def compile_re(self):
        re_h2 = re.compile(self.h2)
        re_h3 = re.compile(self.h3)
        re_h2 = re_h2.findall(self.html_str)
        re_h3 = re_h3.findall(self.html_str)
        self.re_h2 = re_h2
        self.re_h3 = re_h3

    def generate_menu_str(self):
        self.compile_re()
        data = []
        _data = []
        for i in self.re_h2:
            name = self.get_chinese(i)
            self.re_h3.pop(0)
            for j in self.re_h3:
                if 'h2' not in j and 'h3' in j:
                    _name = self.get_chinese(j)
                    _data.append({'name': _name})
                    self.re_h3.pop(0)
                else:
                    break
            data.append({'name': name, 'children': _data})
            _data = []
        template = Template(base_template)
        res = template.render({'data': data})
        return res


if __name__ == '__main__':
    _str = ''
    c = ContentHandler(html_str=_str)
    print(c.generate_menu_str())
