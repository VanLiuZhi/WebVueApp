# Date 2018-03-20
# Author VanLiu

# from django.shortcuts import render
from django.template import loader
from django.views.generic.base import View
from django.http import (
    Http404, HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect,
)
from django.conf import settings
# from mongodbmanage.base import mongo_connection


class BaseView(View):
    template_name = None

    def render(self, template_name, context=None, request=None, content_type=None, status=None, using=None):
        """
        render extend, request is optional
        """
        if context is None or not isinstance(context, dict):
            context = {}
        context['view'] = self.__class__.__name__
        context['view_path'] = getattr(self, 'file_path', '')
        context['STATIC_URL'] = settings.STATIC_URL
        context['IS_DEBUG'] = settings.DEBUG
        content = loader.render_to_string(template_name, context, request=request, using=using)
        return HttpResponse(content, content_type, status)


