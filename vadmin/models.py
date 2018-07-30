# Date 2018-03-12
# Author VanLiuZhi

from django.db import models
from base.models import BaseModel
from base.fields import verbose_name as _

MENU_TYPE = []


class ArticleMenu(BaseModel):
    """
    菜单模型
    """
    name = models.CharField(_('菜单名称'), max_length=32)
    parent = models.CharField(_('所属菜单'), max_length=32)  # 存储菜单上级的GUID
    guid = models.CharField(_('GUID'), max_length=32)
    type = models.SmallIntegerField(_('类型'), default=1)
    level = models.SmallIntegerField(_('级别'), default=1)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('菜单类别')
        verbose_name_plural = _('菜单类别')
        ordering = ['ordering', 'id']
        app_label = 'vadmin'

    @property
    def return_children(self):
        """
        返回属于这个菜单的子项（只返回子项，不返回子项的子项）
        :return:
        """
        query = ArticleMenu.objects.filter(parent=self.guid)
        return [{'name': item.name, 'guid': item.guid} for item in query]


class Article(BaseModel):
    """
    文章模型
    """
    title = models.CharField(_('标题'), max_length=16)
    auther = models.CharField(_('作者'), max_length=16)
    abstract = models.TextField(_('摘要'))
    cover = models.CharField(_('封面img对应url'), max_length=256)
    content = models.TextField(_('内容'))
    times = models.SmallIntegerField(_('浏览次数'))
    guid = models.CharField(_('GUID'), max_length=32)
    articlemenu = models.CharField(_('所属菜单的GUID'), max_length=32)

    def __unicode__(self):
        return u'%s-%s' % (self.title, self.auther)

    class Meta:
        verbose_name = _('文章')
        verbose_name_plural = _('文章')
        ordering = ['ordering', 'id']
        app_label = 'vadmin'
