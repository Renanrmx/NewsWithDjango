from django.shortcuts import render
from django.shortcuts import redirect
from .models import *
from .forms import DateRangeFilterForm

from datetime import timedelta


def home(request, category=None, tag=None):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    art_tags = ArticleTag.objects.all()

    if category:
        articles = Article.objects.filter(fk_category=category)
    elif tag:
        articles = Article.objects.prefetch_related('article_tags').filter(article_tags__fk_tag__id=tag)
    else:
        articles = Article.objects.all()

    filter_form = DateRangeFilterForm(request.POST or None)
    if filter_form.is_valid():
        form = filter_form.cleaned_data
        articles = Article.objects.filter(publish_datetime__lte=form['end_range']+timedelta(days=1),
                                          publish_datetime__gte=form['start_range'])

    return render(request, 'index.html', {'categories': categories, 'art_tags': art_tags, 'tags': tags, 'articles': articles,
                                          'filter_name': filter_name(articles, category, tag), 'filter_form': filter_form})


def details(request, article):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    art_tags = ArticleTag.objects.filter(fk_article=article)
    article = Article.objects.get(id=article)
    return render(request, 'single.html', {'categories': categories, 'art_tags': art_tags, 'tags': tags, 'article': article})


def filter_name(articles, category=None, tag=None):
    if articles:
        if category:
            return Category.objects.get(id=category)
        elif tag:
            return Tag.objects.get(id=tag)
        else:
            return 'Geral'
    return False


