# Date 2018-03-12
# Author VanLiu

from django.db import models
from base.fields import verbose_name as _
import datetime


class BaseModel(models.Model):
    ordering = models.IntegerField(_('排序权值'), default=0, db_index=True, editable=False)
    created = models.DateTimeField(_('创建时间'), auto_now_add=True)
    date = models.DateTimeField(_('创建日期'), default=datetime.datetime.today())
    updated = models.DateTimeField(_('修改时间'), auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-ordering', '-id']
