# Date 2018-03-12
# Author VanLiu

from django.db import models
from base.fields import verbose_name as _
from base.models import BaseModel
from django.contrib.auth.hashers import make_password, check_password
import datetime


class User(BaseModel):
    last_name = models.CharField(_('用户名'), max_length=128, null=True, blank=True)
    first_name = models.CharField(_('用户姓'), max_length=64, null=True, blank=True)
    name = models.CharField(_('姓名'), max_length=192, db_index=True, null=True, blank=True)
    code = models.CharField(_('编号'), max_length=64, db_index=True, null=True, blank=True)
    email = models.EmailField(_('邮件'), max_length=256, null=True, blank=True)
    username = models.CharField(_('登录帐号'), max_length=32, db_index=True, null=False, unique=True)
    password = models.CharField(_('加密密码'), max_length=32, null=False)
    icon = models.CharField(_('头像'), max_length=128, null=True, blank=True)
    level = models.SmallIntegerField(_('等级'), default=1)
    role = models.ForeignKey(to='user.Role', verbose_name=_('角色'), null=True, blank=True, on_delete=models.SET_NULL,
                             related_name="%(app_label)s_%(class)s_related")
    group = models.ForeignKey(to='user.UserGroup', verbose_name=_('用户组'), null=True, blank=True,
                              on_delete=models.SET_NULL, related_name="%(app_label)s_%(class)s_related")

    @staticmethod
    def make_password_for_hash(value):
        """
        通过框架加密工具加密密码
        :param value:
        :return:
        """
        return make_password(value)

    def check_password(self, password):
        """
        密码解密验证
        :return:
        """
        return check_password(password, self.password)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('用户')
        verbose_name_plural = _('用户')
        ordering = ['ordering', 'id']
        app_label = 'user'


class Role(BaseModel):
    name = models.CharField(_('角色名'), max_length=64)
    power = models.ManyToManyField(to='user.Power')

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('角色')
        verbose_name_plural = _('角色')
        ordering = ['ordering', 'id']
        app_label = 'user'


class Power(BaseModel):
    name = models.CharField(_('权限名'), max_length=64)
    permissions = models.TextField(_('权限列表'), editable=False)  # 操作权限的集合

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('权限')
        verbose_name_plural = _('权限')
        ordering = ['ordering', 'id']
        app_label = 'user'


class UserGroup(BaseModel):
    name = models.CharField(_('组名'), max_length=64)
    power = models.ManyToManyField(to='user.Power')

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('用户组')
        verbose_name_plural = _('用户组')
        ordering = ['ordering', 'id']
        app_label = 'user'
