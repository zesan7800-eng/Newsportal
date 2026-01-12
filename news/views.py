from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Category, Article
from .forms import ArticleForm


# ----------------------
# HOME PAGE
# ----------------------
def home(request):
    categories = Category.objects.all()
    latest_news = Article.objects.filter(
        is_published=True
    ).order_by('-created_at')[:5]

    category_sections = {}
    for cat in categories:
        category_sections[cat] = Article.objects.filter(
            category=cat,
            is_published=True
        )[:4]

    return render(request, 'news/home.html', {
        'latest_news': latest_news,
        'category_sections': category_sections,
        'categories': categories
    })


# ----------------------
# CATEGORY PAGE
# ----------------------
def category_articles(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(
        category=category,
        is_published=True
    )

    return render(request, 'news/category.html', {
        'category': category,
        'articles': articles,
        'categories': Category.objects.all()
    })


# ----------------------
# ARTICLE DETAIL
# ----------------------
def article_detail(request, slug):
    article = get_object_or_404(
        Article,
        slug=slug,
        is_published=True
    )

    related_articles = Article.objects.filter(
        category=article.category,
        is_published=True
    ).exclude(id=article.id)[:5]

    return render(request, 'news/article_detail.html', {
        'article': article,
        'related_articles': related_articles,
        'categories': Category.objects.all()
    })


# ----------------------
# CREATE ARTICLE
# ----------------------
@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.is_published = True   # publish immediately
            article.save()
            return redirect(article.get_absolute_url())
    else:
        form = ArticleForm()

    return render(request, 'news/article_form.html', {
        'form': form,
        'categories': Category.objects.all()
    })


# ----------------------
# EDIT ARTICLE
# ----------------------
@login_required
def edit_article(request, pk):
    article = get_object_or_404(
        Article,
        pk=pk,
        author=request.user
    )

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('my_articles')
    else:
        form = ArticleForm(instance=article)

    return render(request, 'news/article_form.html', {
        'form': form,
        'categories': Category.objects.all()
    })


# ----------------------
# DELETE ARTICLE
# ----------------------
@login_required
def delete_article(request, pk):
    article = get_object_or_404(
        Article,
        pk=pk,
        author=request.user
    )

    if request.method == 'POST':
        article.delete()
        return redirect('my_articles')

    return render(request, 'news/delete_confirm.html', {
        'article': article,
        'categories': Category.objects.all()
    })


# ----------------------
# JOURNALIST DASHBOARD
# ----------------------
@login_required
def my_articles(request):
    articles = Article.objects.filter(author=request.user)

    return render(request, 'news/my_articles.html', {
        'articles': articles,
        'categories': Category.objects.all()
    })


# ----------------------
# REGISTER
# ----------------------
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('my_articles')
    else:
        form = UserCreationForm()

    return render(request, 'news/register.html', {
        'form': form,
        'categories': Category.objects.all()
    })
