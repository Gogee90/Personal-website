from django.apps import AppConfig
from watson import search as watson


class BlogZapravschikaConfig(AppConfig):
    name = 'blog_zapravschika'

    def ready(self):
        models = ["SiteNewsModel", "ArticleModel", "FAQModel"]
        for model in models:
            article = self.get_model(model)
            watson.register(article)
