from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from news.auth import register
from . import views

app_name = 'news'

urlpatterns = [
    # Home page - using the class-based view
    path('', views.HomePageView.as_view(), name='home'),

    # Test view
    path('test/', views.test_view, name='test'),

    # Article list and detail views
    path('articles/', views.ArticleListView.as_view(), name='article_list'),
    path('articles/<int:year>/<int:month>/<int:day>/<slug:slug>/',
         views.ArticleDetailView.as_view(), name='article_detail'),

    # Category view
    path('category/<slug:slug>/', views.CategoryArticleListView.as_view(), name='category'),

    # Article CRUD operations
    path('article/new/', views.ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/edit/', views.ArticleUpdateView.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)