from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import Article, Category, Comment
from .forms import CommentForm, ArticleForm


def test_view(request):
    return HttpResponse("This is a test view")


class HomePageView(ListView):
    model = Article
    template_name = 'news/home.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(status='published')[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add featured and latest articles
        context['featured_article'] = Article.objects.filter(
            status='published'
        ).order_by('-views').first()

        context['latest_articles'] = Article.objects.filter(
            status='published'
        ).order_by('-publish_date')[:5]

        # Add categories for navigation
        context['categories'] = Category.objects.all()

        return context


class ArticleListView(ListView):
    model = Article
    template_name = 'news/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.filter(status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/article_detail.html'
    context_object_name = 'article'

    def get_object(self):
        # Get the article object
        article = super().get_object()
        # Increment view count
        article.views += 1
        article.save()
        return article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add comment form to context
        context['comment_form'] = CommentForm()

        # Add related articles
        category = self.object.category
        context['related_articles'] = Article.objects.filter(
            category=category,
            status='published'
        ).exclude(id=self.object.id)[:5]

        # Add categories for navigation
        context['categories'] = Category.objects.all()

        return context

    def post(self, request, *args, **kwargs):
        # Handle comment submission
        article = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            return redirect(article.get_absolute_url())

        # If form is invalid, render the page again with form errors
        context = self.get_context_data(object=article)
        context['comment_form'] = form
        return self.render_to_response(context)


class CategoryArticleListView(ListView):
    template_name = 'news/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Article.objects.filter(category=self.category, status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.all()
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'news/article_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'news/article_form.html'

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'news/article_form.html'
    success_url = reverse_lazy('news:article_list')

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context