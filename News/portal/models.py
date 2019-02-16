from django.db import models

from django.contrib.auth.models import User
from django.conf import settings


class Position(models.Model):
    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        permissions = (
            ("change_from_another_author", "Can change contents of other authors"),
            ("change_authorship", "Can change authorship"),
        )

    name = models.CharField(max_length=30, unique=True, verbose_name='Cargo')

    def __str__(self):
        return self.name


class Author(models.Model):
    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'

    about = models.TextField(null=True, blank=True, verbose_name='Sobre')

    user = models.OneToOneField(User, models.CASCADE, related_name='author', verbose_name='Usuário')
    fk_position = models.ForeignKey(Position, models.PROTECT, related_name='positions', verbose_name='Cargo')

    def __str__(self):
        return self.user.username

    def email(self):
        return self.user.email

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def position(self):
        return self.fk_position.name

    email.short_description = 'Email'
    first_name.short_description = 'Nome'
    last_name.short_description = 'Sobrenome'
    position.short_description = 'Cargo'


class Category(models.Model):
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    name = models.CharField(max_length=20, unique=True, verbose_name='Categoria')
    description = models.TextField(null=True, blank=True, verbose_name='Descrição')

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name='Termo Chave')

    def __str__(self):
        return self.name


class Article(models.Model):
    class Meta:
        verbose_name = 'Artigo'
        ordering = ['-publish_datetime']

    def default_content():
        with open(settings.BASE_DIR + '/portal/templates/' + "article_default_content.html", "rt") as in_file:
            return in_file.read()

    title = models.CharField(max_length=80, verbose_name='Titulo')
    description = models.TextField(verbose_name='Descrição')
    illustration = models.ImageField(upload_to='articles-illustrations/%Y/%m/%d/', null=True, blank=True, verbose_name='Ilustração')  # proporção 400x270
    content = models.TextField(verbose_name='Conteúdo', default=default_content())
    event_datetime = models.DateTimeField(null=True, blank=True, verbose_name='Data do Ocorrido')
    publish_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Data da Publicação')
    update_datetime = models.DateTimeField(auto_now=True, verbose_name='Data de Alteração')

    fk_author = models.ForeignKey(Author, models.PROTECT, related_name='articles', verbose_name='Autor')
    fk_category = models.ForeignKey(Category, models.PROTECT, related_name='articles', verbose_name='Categoria')

    def __str__(self):
        return self.title

    def author(self):
        return self.fk_author.user.first_name + ' ' + self.fk_author.user.last_name

    def category(self):
        return self.fk_category.name

    author.short_description = 'Autor'
    category.short_description = 'Categoria'


class ArticleTag(models.Model):
    class Meta:
        verbose_name = 'Tag do Artigo'
        verbose_name_plural = 'Tags dos Artigos'

    fk_article = models.ForeignKey(Article, models.CASCADE, related_name='article_tags', verbose_name='Artigo')
    fk_tag = models.ForeignKey(Tag, models.PROTECT, related_name='article_tags', verbose_name='Tag')

    def article(self):
        return self.fk_article.title

    def tag(self):
        return self.fk_tag.name

    article.short_description = 'Artigo'
    tag.short_description = 'Termo Chave'



