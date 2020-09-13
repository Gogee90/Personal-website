from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.utils import timezone
from blog_zapravschika.models import ArticleModel, SiteNewsModel, FAQModel
from blog_zapravschika.forms import Loginform, PostForm, RegistrationForm, EmailSend
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.views.generic import TemplateView, DetailView, View
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView


# Create your views here.

class MainPageView(TemplateView):
    template_name = 'blog_zapravschika/welcome_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MainPageView, self).get_context_data(*args, **kwargs)
        posts = ArticleModel.objects.filter(published_date__lte=timezone.now()).order_by('published_date')[::-1]
        news = SiteNewsModel.objects.filter().order_by('created_date')
        faq = FAQModel.objects.all()
        title = "Ремонт копировальной техники, заправка и восстановление картриджей"
        variables = {
            'posts': posts,
            'news': news,
            'faq': faq,
            'title': title,
        }
        context.update(variables)
        return context


class ArticlesView(ListView):
    template_name = 'blog_zapravschika/posts.html'
    context_object_name = 'page_obj'
    paginate_by = 10
    ordering = ['-created_date']


class DetailedArticleView(DetailView):
    template_name = 'blog_zapravschika/detailed_post.html'
    context_object_name = 'post'


def coordinates(request):
    return render(request, "blog_zapravschika/coordinates.html")


class LoginView(View):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return HttpResponseRedirect('/admin')
        if user is not None and not user.is_staff:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/login')
        return render(request, "registration/login.html")

    def get(self, request):
        return render(request, "registration/login.html")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post.title)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('detailed_article', id=post.pk, slug=post.slug)
    else:
        form = PostForm()
    return render(request, "blog_zapravschika/create_post.html", {"form": form})


class PostEdit(UpdateView):
    fields = ['title', 'text', 'upload']
    context_object_name = 'post'
    template_name = "blog_zapravschika/post_edit.html"
    query_pk_and_slug = True


"""def post_edit(request, id, slug):
    post = ArticleModel.objects.get(pk=id, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('detailed_article', id=post.pk, slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, "blog_zapravschika/post_edit.html", {
        "form": form,
        "post": post,
    }
                  )"""


def user_create(request):
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            username = registration_form.cleaned_data['username']
            password = registration_form.cleaned_data['password']
            first_name = registration_form.cleaned_data['first_name']
            last_name = registration_form.cleaned_data['last_name']
            email = registration_form.cleaned_data['email']
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.password2 = password
            user.save()
            return redirect('main_page')
    else:
        registration_form = RegistrationForm()
    return render(request, 'blog_zapravschika/registration_form.html', {
        'registration_form': registration_form,
    })
