from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Comment
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CommentForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist


class ArticleListView(ListView):
    """
    The custom class ListView is responsible for showing articles in the home page.
    """
    model = Article
    ordering = ['-date_posted']
    paginate_by = 5
    template_name = 'blog/article/article_list.html'
    extra_context = {'title': 'Home'}
    context_object_name = 'articles'


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """
    The custom class CreateView is responsible for creating a new article and saving it to the DB.

    Additional class parent 'LoginRequiredMixin' gives access to create a new article if a user is logged in.
    """
    model = Article
    fields = ['title', 'slug', 'content']
    template_name = 'blog/article/article_form.html'
    extra_context = {'title': 'New Article'}

    def form_valid(self, form):
        # set a current logged in user as an author of a new article
        form.instance.author = self.request.user
        # call parent's form_valid method to check data from a form
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    The custom class UpdateView is responsible for changing data of existing articles in the DB.

    Additional class parent 'UserPassesTestMixin' gives access to save new data in the DB
    if logged in user is author of article.
    """
    model = Article
    fields = ['title', 'slug', 'content']
    template_name = 'blog/article/article_form.html'
    extra_context = {'title': 'Update Article'}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        # get a new created article as a instance of class Article
        article = self.get_object()
        # check if current logged in user is author of a new article:
            # YES - give access to the update page
            # NO - deny access to the update page
        if self.request.user == article.author:
            return True
        return False


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    The custom class DeleteView is responsible for deleting an existing article from the DB.
    """
    model = Article
    # redirect to home page if a article was deleted successfully
    success_url = '/'
    template_name = 'blog/article/article_confirm_delete.html'
    extra_context = {'title': 'Delete Article'}

    def test_func(self):
        article = self.get_object()
        if self.request.user == article.author:
            return True
        return False


class AboutView(TemplateView):
    template_name = 'blog/article/about.html'
    extra_context = {'title': 'About'}


def article_detail(request,  id=None, slug=''):
    """
    The view is responsible for showing data of a article.
    """
    template_name = 'blog/article/article_detail.html'
    # get article and user object according to request
    article = get_object_or_404(Article, id=id, slug=slug)
    user = request.user
    # get all comments which: 1) are active, 2) is Parent (because field parent is null, no foreignkey to parent)
    comments_list = article.comments.filter(active=True)

    # comment's pagination
    paginator = Paginator(comments_list, 5)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        comments = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        comments = paginator.page(paginator.num_pages)

    # If HTTP method is POST (post new comment/reply)
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            # check if we have parent_id data from request. If yes - it is a reply, not- it is a new comment.
            try:
                parent_id = int(request.POST.get('parent_id'))
                parent_obj = Comment.objects.get(id=parent_id)
                reply_comment = form.save(commit=False)
                reply_comment.level = parent_obj.level + 1
                reply_comment.parent = parent_obj
                # Changed
                reply_comment.article = article
                reply_comment.author = user
                reply_comment.save()
            except (ObjectDoesNotExist, MultipleObjectsReturned, TypeError):
                new_comment = form.save(commit=False)
                new_comment.article = article
                new_comment.author = user
                new_comment.save()
            return redirect(request.get_full_path())

    else:
        form = CommentForm()

    return render(request, template_name, {'article': article,
                                           'comments_list': comments_list,
                                           'comments': comments,
                                           'form': form})



# Class based Article Detail View. I am testing it.
class ArticleDetail(ListView, FormView):
    """
        The custom class ListView is responsible for showing comments and article detail in one page.
    """
    model = Comment
    ordering = ['-created_on']
    paginate_by = 5
    template_name = 'blog/article/article_detail.html'
    extra_context = {'title': 'Article Detail'}
    context_object_name = 'comments'
    form_class = CommentForm

    def __init__(self, **kwargs):
        self.article = None
        self.comment_parent = None
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        self.article = get_object_or_404(Article, id=kwargs['id'], slug=kwargs['slug'])
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = self.article
        return context

    def post(self, request, *args, **kwargs):
        try:
            parent_id = int(request.POST.get('parent_id'))
            self.comment_parent = Comment.objects.get(id=parent_id)
        except TypeError:
            self.comment_parent = None
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        # set a current logged in user as an author of a new article
        form.instance.author = self.request.user
        form.instance.article = self.article
        if self.comment_parent:
            form.instance.parent = self.comment_parent
            form.instance.level = self.comment_parent.level + 1
        form.save()
        return redirect(self.article.get_absolute_url())


