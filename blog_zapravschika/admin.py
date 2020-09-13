from django.contrib import admin
from .models import ArticleModel, SiteNewsModel, FAQModel
from watson.admin import SearchAdmin
from django.core.mail import EmailMessage, get_connection
from blog_zapravschika.forms import EmailSend
from django.shortcuts import render
from django.urls import path
from django.contrib.auth.models import User


# Register your models here.
class SendEmailAdmin(admin.ModelAdmin):
    change_list_template = "blog_zapravschika/redirect_to_email.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('admin/send_email/', self.email_send, name="email_send"),
        ]
        return my_urls + urls

    def email_send(self, request):
        form = EmailSend(request.POST)
        if request.method == "POST" and form.is_valid():
            topic = form.cleaned_data["topic"]
            text = form.cleaned_data["text"]
            sender = request.user.email
            recipients = form.cleaned_data["recipient"]
            conn = get_connection()
            conn.open()
            email = EmailMessage(
                topic,
                text,
                sender,
                [recipients],
            )
            email.content_subtype = "html"
            conn.send_messages([email])
            conn.close()
        return render(request, "blog_zapravschika/email_send.html", {"form": form})
        email_send.short_description = "Рассылка писем"


class SummerModelAdmin(admin.ModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'
    prepopulated_fields = {'slug': ('title',)}


class SearchModelAdmin(SearchAdmin, SummerModelAdmin):
    search_fields = ('title', 'text', 'slug')


my_models = [ArticleModel, SiteNewsModel, FAQModel]

admin.site.register(my_models, SearchModelAdmin)
admin.site.unregister(User)
admin.site.register(User, SendEmailAdmin)
