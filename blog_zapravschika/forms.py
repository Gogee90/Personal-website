from django import forms
from .models import ArticleModel
from ckeditor.widgets import CKEditorWidget
from django.forms import ModelForm
from django.contrib.auth.models import User


class PostForm(ModelForm):
    class Meta:
        model = ArticleModel
        fields = ['title', 'text', 'upload']
        widgets = {
            'text': CKEditorWidget(),
        }


class Loginform(forms.Form):
    username = forms.CharField(label="Логин", max_length=100)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    username = forms.CharField(label="Логин", max_length=100)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повторноый пароль", widget=forms.PasswordInput)
    email = forms.EmailField(max_length=50)
    first_name = forms.CharField(label="Имя", max_length=30)
    last_name = forms.CharField(label="Фамилия", max_length=50)


class EmailSend(forms.Form):
    topic = forms.CharField(label="Тема")
    text = forms.CharField(widget=CKEditorWidget)
    user_email_list = []
    for num, user_email in enumerate(User.objects.all().values_list('email', flat=True)):
        user_email_tuple = (str(num), user_email)
        user_email_list.append(user_email_tuple)
    recipient_list = forms.MultipleChoiceField(required=False, choices=user_email_list)
    recipient = forms.CharField()

