from django.utils import timezone
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import ArticleModel, SiteNewsModel, FAQModel


class BaseSiteMap(Sitemap):
    def __init__(self, model):
        self.model = model

    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return self.model.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()



ArticleSiteMap = BaseSiteMap(ArticleModel)
NewsSiteMap = BaseSiteMap(SiteNewsModel)
FaqSiteMap = BaseSiteMap(FAQModel)
