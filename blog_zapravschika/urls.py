from django.urls import path, include
from . import views
from django.utils import timezone
from blog_zapravschika.models import ArticleModel, SiteNewsModel, FAQModel
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from .sitemaps import ArticleSiteMap, NewsSiteMap, FaqSiteMap

sitemaps = {
    'articles': ArticleSiteMap,
    'news': NewsSiteMap,
    'faq': FaqSiteMap,
}

urlpatterns = [
    path('', views.MainPageView.as_view(), name="main_page"),
    path('articles/', views.ArticlesView.as_view(queryset=ArticleModel.objects.all()), name="articles"),
    path('news/', views.ArticlesView.as_view(queryset=SiteNewsModel.objects.all()), name="news"),
    path('faq/', views.ArticlesView.as_view(model=FAQModel), name="faq"),
    path('news/<int:id>/<slug:slug>', views.DetailedArticleView.as_view(model=SiteNewsModel), name="detailed_news"),
    path('articles/<int:id>/<slug:slug>', views.DetailedArticleView.as_view(model=ArticleModel),
         name="detailed_article"),
    path('faq/<int:id>/<slug:slug>', views.DetailedArticleView.as_view(model=FAQModel), name="faq_page"),
    path('coordinates', views.coordinates, name="coordinates"),
    path('login/', views.LoginView.as_view(), name="login_page"),
    path('logout/', views.logout_user, name="logout_user"),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('post/', views.create_post, name="create_post"),
    path('registration/', views.user_create, name="user_create"),
    path('articles/<int:id>,<slug:slug>/post_edit', views.PostEdit.as_view(model=ArticleModel), name="post_edit"),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('search/', include("watson.urls", namespace="watson"), {
        "template_name": "blog_zapravschika/search_results.html",
    }),
]
