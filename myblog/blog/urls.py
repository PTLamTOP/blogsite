from django.urls import path, include
from .views import about, ArticleListView, article_detail, \
    ArticleCreateView, ArticleUpdateView, ArticleDeleteView


app_name = 'blog'

urlpatterns = [
    path('', ArticleListView.as_view(), name='blog-home'),
    path('about/', about, name='blog-about'),
    path('article/<slug:slug>/', article_detail, name='article-detail'),
    path('article/new/', ArticleCreateView.as_view(), name='article-create'),
    path('article/<slug:slug>/update', ArticleUpdateView.as_view(), name='article-update'),
    path('article/<slug:slug>/delete', ArticleDeleteView.as_view(), name='article-delete'),
]