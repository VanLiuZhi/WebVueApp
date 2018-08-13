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
        return u'%s' % self.name

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
    def return_all_children_count(self):
        """
        返回该分类下有多少文章
        :return:
        """
        query_list = self.return_all_children
        id_list = [item.guid for item in query_list if item and item.guid or None]
        count = Article.objects.filter(articleclassify__in=id_list).count()
        return count or 0

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
            for i in range(length):
                current = que.pop(0)  # 出队列的当前节点
                res.append(current)  # 直接把节点加到结果里面
                for child in current.return_children:  # 所有子结点入队列
                    que.append(child)
        return res

    @property
    def return_parents(self):
        """
        返回当前分类的父级信息
        :return:
        """
        parent = ArticleClassify.objects.filter(guid=self.parent).first()
        loop = 5
        res = []
        if parent:
            res.append({'name': parent.name})
        while parent and loop:
            parent = ArticleClassify.objects.filter(guid=parent.parent).first()
            if parent:
                res.append({'name': parent.name})
                loop -= 1
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
    articleclassify = models.CharField(_('所属分类的GUID'), max_length=32)

    def __unicode__(self):
        return u'%s-%s' % (self.title, self.author)

    @property
    def return_article_classify_name(self):  # article_classify_name 名字不能用，和框架冲突了
        ac = ArticleClassify.objects.get(guid=self.articleclassify)
        return ac and ac.name or ''

    @property
    def article_to_article_classify(self):
        return ArticleClassify.objects.filter(guid=self.articleclassify).first()

    @property
    def return_classify_parents(self):
        return self.article_to_article_classify.return_parents

    def update_times(self):
        """
        更新浏览次数
        :return:
        """
        self.times = self.times + 1
        self.save()

    # 由通用方法处理的模型，通过定义add_fields实现字段扩展
    add_fields = ['return_article_classify_name', 'return_classify_parents']

    class Meta:
        verbose_name = _('文章')
        verbose_name_plural = _('文章')
        ordering = ['ordering', 'id']
        app_label = 'vadmin'
