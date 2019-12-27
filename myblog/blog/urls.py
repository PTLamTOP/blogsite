from django.urls import path, include
from .views import about, ArticleListView, ArticleDetailView, \
    ArticleCreateView, ArticleUpdateView, ArticleDeleteView


urlpatterns = [
    path('', ArticleListView.as_view(), name='blog-home'),
    path('about/', about, name='blog-about'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('article/new/', ArticleCreateView.as_view(), name='article-create'),
    path('article/<int:pk>/update', ArticleUpdateView.as_view(), name='article-update'),
    path('article/<int:pk>/delete', ArticleDeleteView.as_view(), name='article-delete'),
]