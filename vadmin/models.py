# Date 2018-03-12
# Author VanLiuZhi

from django.db import models
from base.models import BaseModel
from base.fields import verbose_name as _
from django.utils.functional import cached_property

MENU_TYPE = []


class ArticleClassify(BaseModel):
    """
    文章分类模型
    """
    name = models.CharField(_('分类名称'), max_length=32)
    parent = models.CharField(_('所属分类'), max_length=32)  # 存储分类上级的GUID
    guid = models.CharField(_('GUID'), max_length=32)
    # type = models.SmallIntegerField(_('类型'), default=1)
    level = models.SmallIntegerField(_('级别'), default=1)  # 最大到三级（没有做限制）

    def __unicode__(self):
        return u'%s' % self.name

    def __repr__(self):
        return u'%s-%s' % (self.name, self.id)

    class Meta:
        verbose_name = _('文章分类')
        verbose_name_plural = _('文章分类')
        ordering = ['ordering', 'id']
        app_label = 'vadmin'

    @property
    def return_children(self):
        """
        返回属于这个分类的子项（只返回子项，不返回子项的子项）
        :return:
        """
        query = ArticleClassify.objects.filter(parent=self.guid)
        return query

    @staticmethod
    def get_children(guid):
        """
        获取parent为guid的子项
        :param guid:
        :return: guid list
        """
        return ArticleClassify.objects.filter(parent=guid).values_list('guid', flat=True)

    @property
    def return_all_children(self):
        """
        返回所有的子项（利用N叉树遍历方法
        ）
        :return:
        """
        root = self
        if not root:
            return []
        que = []  # 保存节点的队列
        res = []  # 保存结果的列表
        que.append(root)  #
        while len(que):  # 判断队列不为空
            length = len(que)
            # sub = []  # 保存每层的节点的值
            for i in range(length):
                current = que.pop(0)  # 出队列的当前节点
                # sub.append(current)
                res.append(current)  # 直接把节点加到结果里面
                for child in current.return_children:  # 所有子结点入队列
                    que.append(child)
            # res.append(sub)  # 把每层的节点的值加入结果列表
        return res


class Article(BaseModel):
    """
    文章模型
    """
    title = models.CharField(_('标题'), max_length=16)
    author = models.CharField(_('作者'), max_length=16)
    abstract = models.TextField(_('摘要'))
    cover = models.CharField(_('封面img对应url'), max_length=256)
    content = models.TextField(_('内容'))
    times = models.SmallIntegerField(_('浏览次数'))
    guid = models.CharField(_('GUID'), max_length=32)
    articlemenu = models.CharField(_('所属菜单的GUID'), max_length=32)

    def __unicode__(self):
        return u'%s-%s' % (self.title, self.author)

    @property
    def article_menu_name(self):
        ac = ArticleClassify.objects.get(guid=self.articlemenu)
        return ac and ac.name or ''

    class Meta:
        verbose_name = _('文章')
        verbose_name_plural = _('文章')
        ordering = ['ordering', 'id']
        app_label = 'vadmin'
