from .models import Article, Comment
from .forms import CommentForm

from django.views.generic import ListView, CreateView, UpdateView,\
    DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.shortcuts import get_object_or_404
from django.shortcuts import redirect


class ArticleListView(ListView):
    model = Article
    paginate_by = 5
    template_name = 'blog/article/article_list.html'
    extra_context = {'title': 'Home'}
    context_object_name = 'articles'


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['title', 'content']
    template_name = 'blog/article/article_form.html'
    extra_context = {'title': 'New Article'}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ['title', 'content']
    template_name = 'blog/article/article_form.html'
    extra_context = {'title': 'Update Article'}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        article = self.get_object()
        if self.request.user == article.author:
            return True
        return False


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    success_url = '/'
    template_name = 'blog/article/article_confirm_delete.html'
    extra_context = {'title': 'Delete Article'}
    login_url = 'users:login'

    def test_func(self):
        article = self.get_object()
        if self.request.user == article.author:
            return True
        return False


class AboutView(TemplateView):
    template_name = 'blog/article/about.html'
    extra_context = {'title': 'About'}


class CommentCreateView(CreateView):
    form_class = CommentForm

    def form_valid(self, form):
        article_id = self.request.POST.get('article_id')
        parent_id = self.request.POST.get('parent_id')
        if parent_id:
            parent = Comment.objects.get(id=parent_id)
            form.instance.parent = parent
        form.instance.author = self.request.user
        article = Article.objects.get(id=article_id)
        form.instance.article = article
        form.save()
        return redirect(article.get_absolute_url())


class ArticleDetail(ListView):
    model = Comment
    context_object_name = 'comments'
    paginate_by = 5
    template_name = 'blog/article/article_detail.html'
    extra_context = {'title': 'Article Detail'}
    article_id = None

    def get(self, request, *args, **kwargs):
        self.article_id = kwargs['id']
        return super().get(request, *args, **kwargs)

    def get_context_data(self, object_list=None, **kwargs):
        article = get_object_or_404(Article, id=self.article_id)
        context = super().get_context_data(object_list=None, **kwargs)
        context.update({'article': article,
                        'comment_form': CommentForm, })
        return context
