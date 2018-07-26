# Date 2018-03-12
# Author VanLiuZhi

from django.db import models
from base.fields import verbose_name as _
from django.utils import timezone
from django.utils.functional import cached_property
import datetime


class BaseModel(models.Model):
    ordering = models.IntegerField(_('排序权值'), default=0, db_index=True, editable=False)
    created = models.DateTimeField(_('创建时间'), auto_now_add=True)
    date = models.DateTimeField(_('创建日期'), default=timezone.now)
    updated = models.DateTimeField(_('修改时间'), auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-ordering', '-id']

    @cached_property
    def base_fields(self):
        """
        基本字段list（BaseModel的字段 + id）
        :return:
        """
        return [item.attname for item in BaseModel()._meta.concrete_fields]

    @cached_property
    def return_fields(self):
        """
        返回模型字典名称的list（不会返回id和基本字段，需要则手动添加）
        :return:
        """
        return [item.attname for item in self._meta.concrete_fields if item not in self.base_fields]

    @property
    def return_dict(self):
        """
        返回模型实例的字典
        :return:
        """
        _dict = {}
        _field = self.return_fields
        for item in _field:
            _dict[item] = getattr(self, item, '')
        return _dict
