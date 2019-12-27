from django.shortcuts import render
from .models import Article
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


"""
The custom class ListView is responsible for showing articles in the home page.
"""
class ArticleListView(ListView):
    model = Article
    ordering = ['-date_posted']
    paginate_by = 5


"""
The custom class DetailView is responsible for showing data of a article.
"""
class ArticleDetailView(DetailView):
    model = Article


"""
The custom class CreateView is responsible for creating a new article and saving it to the DB.

Additional class parent 'LoginRequiredMixin' gives access to create a new article if a user is logged in.
"""
class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['title', 'intro', 'content']

    def form_valid(self, form):
        # set a current logged in user as an author of a new article
        form.instance.author = self.request.user
        # call parent's form_valid method to check data from a form
        return super().form_valid(form)


"""
The custom class UpdateView is responsible for changing data of existing articles in the DB.

Additional class parent 'UserPassesTestMixin' gives access to save new data in the DB 
if logged in user is author of article.
"""
class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ['title', 'intro', 'content']

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


"""
The custom class DeleteView is responsible for deleting an existing article from the DB.
"""
class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    # redirect to home page if a article was deleted successfully
    success_url = '/'

    def test_func(self):
        article = self.get_object()
        if self.request.user == article.author:
            return True
        return False


def about(request, pk=None):
    return render(request, 'blog/about.html', {'pk': pk})


