# Date 2018-03-12
# Author VanLiu

from django.db import models
from base.fields import verbose_name as _
from base.models import BaseModel
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
import datetime


class MoneyStats(BaseModel):
    """
    money stats
    """
    title = models.CharField(_('标题'), max_length=64)
    money = models.CharField(_('金额'), max_length=64)
    date = models.DateField(_('日期'), default=timezone.now)

    def __unicode__(self):
        return u'%s' % self.title

    class Meta:
        verbose_name = _('金额统计')
        verbose_name_plural = _('金额统计')
        ordering = ['ordering', 'id']
        app_label = 'stats'

