from django.urls import path
from .views import ArticleListView, ArticleCreateView, ArticleUpdateView, \
    ArticleDeleteView, AboutView, ArticleDetail, CommentCreateView


app_name = 'blog'

urlpatterns = [
    path('', ArticleListView.as_view(), name='blog-home'),
    path('about/', AboutView.as_view(), name='blog-about'),
    path('article/new/', ArticleCreateView.as_view(), name='article-create'),
    path('article/<int:id>/<slug:slug>/', ArticleDetail.as_view(), name='article-detail'),
    path('article/<int:id>/<slug:slug>/update', ArticleUpdateView.as_view(), name='article-update'),
    path('article/<int:id>/<slug:slug>/delete', ArticleDeleteView.as_view(), name='article-delete'),
    path('comment/create/', CommentCreateView.as_view(), name='comment-create'),
]