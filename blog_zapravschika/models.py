from django.db import models
from django.utils import timezone
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class BaseModel(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.Model)
    title = models.CharField(max_length=200)
    slug = models.SlugField(verbose_name='Identifier')
    text = RichTextUploadingField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    upload = models.ImageField(null=True, blank=True, upload_to='media')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class SiteNewsModel(BaseModel):
    def get_absolute_url(self):
        return reverse('detailed_news', kwargs={'id':self.id, 'slug': self.slug})


class ArticleModel(BaseModel):
    def get_absolute_url(self):
        return reverse('detailed_article', kwargs={'id':self.id, 'slug': self.slug})


class FAQModel(BaseModel):
    def get_absolute_url(self):
        return reverse('faq_page', kwargs={'id':self.id, 'slug': self.slug})
